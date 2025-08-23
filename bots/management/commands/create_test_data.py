from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bots.models import Bot, Scenario, Step

class Command(BaseCommand):
    help = 'Create test data for the application'
    
    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com', 'password': 'testpass123'}
        )
        
        bot, created = Bot.objects.get_or_create(
            name='Тестовый бот',
            owner=user,
            defaults={
                'token': 'your-telegram-bot-token-here',
                'gpt_settings': {'model': 'gpt-3.5-turbo', 'temperature': 0.7}
            }
        )
        
        if created:
            self.stdout.write(f"Created bot: {bot.name}")
            
            scenario = Scenario.objects.create(
                name='Ознакомительный сценарий',
                bot=bot
            )
            
            step1 = Step.objects.create(
                scenario=scenario,
                name='Приветствие',
                screen_type='text',
                message='Добро пожаловать! Я ваш помощник по бизнес-обучению.'
            )
            
            step2 = Step.objects.create(
                scenario=scenario,
                name='Имя пользователя',
                screen_type='input',
                message='Как вас зовут?',
                previous_step=step1
            )
            
            step3 = Step.objects.create(
                scenario=scenario,
                name='Выбор темы',
                screen_type='choice',
                message='Выберите интересующую вас тему:',
                options=['Маркетинг', 'Управление', 'Финансы'],
                previous_step=step2
            )
            
            step1.next_step = step2
            step1.save()
            
            step2.next_step = step3
            step2.save()
            
            scenario.initial_step = step1
            scenario.save()
            
            self.stdout.write("Test data created successfully!")
        else:
            self.stdout.write("Test data already exists")