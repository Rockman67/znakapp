from django.conf import settings
from django.core.management.base import BaseCommand
from service.bot import Bot
class Command(BaseCommand):
    help = 'Запускает вашего Telegram бота'

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        bot = Bot(token)
        bot.run()