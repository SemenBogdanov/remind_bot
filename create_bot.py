import logging
from aiogram import Bot, Dispatcher
from key import token
from BotDB import BotDB


API_TOKEN = token

# Подключаем соответствующую конфигурацию логгирования документа
logging.basicConfig(level=logging.INFO)

# Создаем экземпляры классов Bot и Dispatcher, которые мы заранее ипортировали
# из библиотеки aiogram на строке 2
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

try:
    botDatabase = BotDB()
except Exception as e:
    print(e)



