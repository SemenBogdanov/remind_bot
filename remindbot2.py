"""
This is a echo bot.
It echoes any incoming text messages.git
"""
import asyncio
import logging
import datetime

import typing
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from key import token
from BotDB import BotDB
from aiogram import Bot, Dispatcher, executor, types
from answers import answers

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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("""Добрый день!\n"""
                        """Выбирайте самый сложный путь - там не конкурентов!\n\n"""
                        """Ниже есть кнопка, чтоб увидеть ответы на часто задаваемые вопросы. """,
                        reply_markup=keyboard2())
    # await message.answer('This is your chat.id = ' + str(message.chat.id))


@dp.message_handler(commands=['getall'])
async def get_records(message: types.Message):
    reply_text = botDatabase.get_all_records()
    await message.answer(reply_text)


call_data1 = CallbackData('data', 'num')
call_data2 = CallbackData('wantAsk', 'wantAsk')


def get_keyboard():
    return InlineKeyboardMarkup().row(
        KeyboardButton('Пора ли звонить?', callback_data=call_data1.new(num='1')),
    ).row(
        KeyboardButton('Услуги и цены', callback_data=call_data1.new(num='2')),
        KeyboardButton('Алгоритм работы', callback_data=call_data1.new(num='3')),
    ).row(
        KeyboardButton('Команда', callback_data=call_data1.new(num='4')),
        KeyboardButton('Контакты', callback_data=call_data1.new(num='5')),
        KeyboardButton('Об авторе...', callback_data=call_data1.new(num='6')),
    ).row(
        InlineKeyboardButton(text='Оставить заявку и получить бонус!', url='https://big-career.ru/', callback_data=call_data1.new(num='7')),
    )


def keyboard2():
    return ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton('---Задать вопрос!---')
    )


@dp.message_handler(text=['---Задать вопрос!---'])
async def addnewbirth(message: types.Message):
    await message.reply('Выберите вопрос и нажмите кнопку:\n', reply_markup=get_keyboard())


@dp.callback_query_handler(call_data1.filter(num=['1', '2', '3', '4', '5', '6', '7']))
async def callback_reply(query: types.CallbackQuery, callback_data):
    await query.answer()
    # logging.info('This what we have got %r', callback_data)
    # logging.info('This is calldata1 %r', call_data1)
    ans = answers[int(callback_data['num']) - 1]
    await bot.send_message(query.from_user.id, ans, parse_mode='html')


@dp.message_handler(text=['chatid'])
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer('This is your chat.id = ' + str(message.chat.id))


@dp.message_handler(text=['hello', 'привет', 'как дела'])
async def reply_welcome(message: types.Message):
    await message.reply('Привет! Я Аля - бот-помощник! Скоро будет база данных!')


async def remind_me(wait_time=20):
    today = str(datetime.datetime.today().date())

    while True:
        await asyncio.sleep(wait_time)
        try:
            # Получаем списко друзей из БД в виде списка с кортежами внутри
            friends = botDatabase.get_friends()
            # Убираем год рождения, чтоб понять у кого сегодня день рождения
            format_date = '%d.%m'
            # Получаем текущую дату
            today = datetime.datetime.strftime(datetime.datetime.now().date(), format_date)
            remind_list = (x[0] for x in friends if x[1].strftime(format_date) == today)
            celebrants = ' \n'.join(remind_list)

            if bool(len(celebrants)):
                remind_msg = 'Сегодня праздник у друзей: \n{}'.format(celebrants)
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
        delay = 60 ** 2 * 8
        loop.create_task(remind_me(delay))
        executor.start_polling(dp, skip_updates=True)

    except Exception as error:
        print('except \n' + error)
        botDatabase.conn.close()
        loop.stop()
