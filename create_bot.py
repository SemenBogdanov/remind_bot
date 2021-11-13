import logging
from aiogram import Bot, Dispatcher
from key import token
from BotDB import BotDB


API_TOKEN = token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

try:
    botDatabase = BotDB()
except Exception as e:
    print(e)



