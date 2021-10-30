"""
This is a echo bot.
It echoes any incoming text messages.git
"""
import asyncio
import logging
import datetime
from key import token

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = token

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")
    await message.answer('This is your chat.id = ' + str(message.chat.id))


@dp.message_handler(text=['chatid'])
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer('This is your chat.id = ' + str(message.chat.id))


@dp.message_handler(text=['hello','привет','как дела'])
async def reply_welcome(message: types.Message):
    await message.reply('Привет! Я Аля - бот-помощник!')


async def remindMe(wait_time=20):
    today = str(datetime.datetime.today().date())

    while True:
        await asyncio.sleep(wait_time)
        try:
            # Получаем списко друзей из БД в виде списка с кортежами внутри
            friends = ({'name': 'Джигурда',
                        'birthday': '17.10.1985',
                        'workplace': 'sberbank'},
                       {'name': 'Оганез',
                        'birthday': '29.10.2021',
                        'workplace': 'Жесть corporation'})
            # Убираем год рождения, чтоб понять у кого сегодня день рождения
            format_date = '%d.%m'
            # Получаем текущую дату
            today = datetime.datetime.strftime((datetime.datetime.now().date()), format_date)
            remind_list = (x['name'] for x in friends if x['birthday'][0:5] == today[0:5])
            celebrants = ', '.join(remind_list)
            if celebrants:
                remind_msg = 'Сегодня праздник у друзей: {}'.format(celebrants)
                await bot.send_message(chat_id='287994530', text=remind_msg)
                # chat_id='-1001716787365'
            else:
                await bot.send_message(chat_id='287994530', text='Именинников сегодня нет')
            print("---Проверка на дни рождения выполнена успешно")
        except Exception as e:
            print("не удалось доставить напоминание")
            print(e)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        delay = 60 ** 2 * 3
        loop.create_task(remindMe(delay))
        executor.start_polling(dp, skip_updates=True)

    except:
        print('except')
        loop.stop()
