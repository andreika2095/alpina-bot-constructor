import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from django.conf import settings
from .models import Bot, UserSession, Step
from .services import gpt_service
import json

class TelegramBotHandler:
    def __init__(self):
        self.bots = {}
        self.dispatchers = {}
    
    def init_bot(self, bot_model):
        try:
            bot = telegram.Bot(token=bot_model.token)
            dispatcher = Dispatcher(bot, None, workers=0)
            
            dispatcher.add_handler(CommandHandler("start", self.start_command))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
            
            self.bots[bot_model.id] = bot
            self.dispatchers[bot_model.id] = dispatcher
            
            return True
        except Exception as e:
            print(f"Error initializing bot {bot_model.id}: {e}")
            return False
    
    async def start_command(self, update, context):
        user_id = update.effective_chat.id
        bot_model = Bot.objects.get(token=context.bot.token)
        
        session, created = UserSession.objects.get_or_create(
            user_id=str(user_id),
            bot=bot_model,
            defaults={'data': {}}
        )
        
        if created or not session.current_step:
            first_scenario = bot_model.scenarios.first()
            if first_scenario and first_scenario.initial_step:
                session.current_step = first_scenario.initial_step
                session.save()
                
                await update.message.reply_text(session.current_step.message)
            else:
                await update.message.reply_text("Добро пожаловать! Чем могу помочь?")
        else:
            await update.message.reply_text("С возвращением! Продолжим наш разговор.")
    
    async def handle_message(self, update, context):
        user_id = update.effective_chat.id
        message_text = update.message.text
        
        try:
            bot_model = Bot.objects.get(token=context.bot.token)
            session = UserSession.objects.get(user_id=str(user_id), bot=bot_model)
            
            if session.current_step:
                response = await self._handle_scenario_step(session, message_text)
            else:
                response = gpt_service.generate_response(message_text, session.data)
            
            await update.message.reply_text(response)
            
        except UserSession.DoesNotExist:
            await update.message.reply_text("Пожалуйста, начните с команды /start")
        except Exception as e:
            print(f"Error handling message: {e}")
            await update.message.reply_text("Извините, произошла ошибка.")
    
    async def _handle_scenario_step(self, session, user_input):
        current_step = session.current_step
        step_type = current_step.screen_type
        
        if step_type == 'input':
            session.data[current_step.name] = user_input
            session.save()
        
        if current_step.next_step:
            session.current_step = current_step.next_step
            session.save()
            return session.current_step.message
        else:
            session.current_step = None
            session.save()
            
            context = {
                "collected_data": session.data,
                "scenario": current_step.scenario.name
            }
            
            prompt = f"Пользователь завершил сценарий {current_step.scenario.name}. Данные: {session.data}. Подведи итоги и предложи дальнейшие действия."
            return gpt_service.generate_response(prompt, context)

telegram_handler = TelegramBotHandler()