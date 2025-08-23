from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Bot
from .telegram_handler import telegram_handler

@receiver(post_save, sender=Bot)
def init_bot_on_save(sender, instance, created, **kwargs):
    telegram_handler.init_bot(instance)

@receiver(post_delete, sender=Bot)
def remove_bot_on_delete(sender, instance, **kwargs):
    if instance.id in telegram_handler.bots:
        del telegram_handler.bots[instance.id]
    if instance.id in telegram_handler.dispatchers:
        del telegram_handler.dispatchers[instance.id]