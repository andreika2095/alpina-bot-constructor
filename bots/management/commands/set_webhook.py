from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError
from ...models import Bot as BotModel

class Command(BaseCommand):
    help = 'Set webhook for Telegram bots'
    
    def add_arguments(self, parser):
        parser.add_argument('--bot-id', type=int, help='Specific bot ID')
        parser.add_argument('--remove', action='store_true', help='Remove webhook')
    
    def handle(self, *args, **options):
        bots = BotModel.objects.all()
        if options['bot_id']:
            bots = bots.filter(id=options['bot_id'])
        
        for bot_model in bots:
            try:
                bot = Bot(token=bot_model.token)
                
                if options['remove']:
                    result = bot.delete_webhook()
                    self.stdout.write(f"Webhook removed for bot {bot_model.name}")
                else:
                    webhook_url = f"https://your-domain.com/api/telegram/webhook/{bot_model.id}/"
                    result = bot.set_webhook(webhook_url)
                    self.stdout.write(f"Webhook set for bot {bot_model.name}: {result}")
            
            except TelegramError as e:
                self.stderr.write(f"Error for bot {bot_model.name}: {e}")