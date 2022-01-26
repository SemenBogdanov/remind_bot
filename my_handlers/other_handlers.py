import asyncio
import logging
from datetime import datetime as dt
from datetime import timedelta as td
from aiogram import types, Dispatcher

# handlers
from create_bot import botDatabase, bot


async def get_my_chat_id(message: types.Message):
    await message.answer('This is your chat.id = ' + str(message.chat.id))


async def help(message: types.Message):
    await message.answer('Помощь:\n'
                         '<b>др цнп</b> - вывод списка всех дней рождений, ранее записанных в базу данных\n'
                         '<b>добавить др</b> - добавляет новую запись о дне рождении в базу данных '
                         'по соответствующему шаблону'
                         '\n<b>найти (Фамилия)</b> - регистрозависимый поиск конкретной записи по фамилии сотрудника'
                         '\n<b>удалить (ID)</b> - удаляет запись с указанным номером'
                         '\n<b>/mychatid</b> - показать ID текущего чата'
                         '\n<b>/myuserid</b> - показать ID пользователя', parse_mode=types.ParseMode.HTML)


async def get_my_user_id(message: types.Message):
    await message.answer('This is your chat.id = ' + str(message.from_user))


async def reply_welcome(message: types.Message):
    await message.reply('Привет! Я могу напоминать тебе про дни рождения')


async def remind_next_week(message: types.Message):
    try:
        friends = botDatabase.get_colleagues()
        format_date = '%d.%m'
        today = dt.strptime(dt.strftime(dt.now() + td(days=10), format_date), '%d.%m')

        remind_list = (x[0] + " " + x[1].strftime(format_date)
                       for x in friends if today >
                       dt.strptime(x[1].strftime(format_date), "%d.%m") >
                       dt.strptime(dt.now().strftime(format_date), "%d.%m"))
        celebrants = ' \n'.join(remind_list)
        logging.info(celebrants)
        chats = ['-1001781029794']
        if bool(len(celebrants)):
            remind_msg = 'Именинники на следующей неделе!: \n{}'.format(celebrants)
            for x in chats:
                await bot.send_message(chat_id=x, text=remind_msg)
        else:
            print("Проверка на дни рождения выполнена успешно")
    except Exception as e:
        print("не удалось доставить напоминание")
        print(e)


# register handlers
def register_other_functions(dp: Dispatcher):
    dp.register_message_handler(get_my_chat_id, commands=['mychatid'])
    welcome_keywords = ['Hello', 'hello', 'привет', 'как дела']
    dp.register_message_handler(reply_welcome, text=welcome_keywords)
    dp.register_message_handler(get_my_user_id, commands=['myuserid'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(remind_next_week, text_contains=['др след'])

# There is no use functions and handlers below:

# async def send_welcome(message: types.Message):
#     await message.reply("""Добрый день!\n"""
#                         """Выбирайте самый сложный путь - там не конкурентов!\n\n"""
#                         """Ниже есть кнопка, чтоб увидеть ответы на часто задаваемые вопросы. """)
#     # await message.answer('This is your chat.id = ' + str(message.chat.id))
#
#
# # @dp.message_handler(text=['---Задать вопрос!---'])
# async def addnewbirth(message: types.Message):
#     await message.reply('Выберите вопрос и нажмите кнопку:\n', reply_markup=keyboards.get_keyboard())


# @dp.callback_query_handler(keyboards.call_data1.filter(num1=['1', '2', '3', '4', '5', '6', '7']))
# async def callback_reply(query: types.CallbackQuery, callback_data):
#     await query.answer()
#     if callback_data['num1'] == '2':
#         await bot.send_message(query.from_user.id, 'Выберите вариант:',
#                                reply_markup=keyboards.keyboard3())
#     else:
#         ans = answers[int(callback_data['num1']) - 1]
#         await bot.send_message(query.from_user.id, ans, parse_mode='html')
#     # logging.info('This what we have got %r', callback_data)
#     # logging.info('This is calldata1 %r', call_data1)


# @dp.callback_query_handler(keyboards.call_data3.filter(num2=['0', '1', '2', '3']))
# async def callback_reply(query: types.CallbackQuery, callback_data):
#     await query.answer()
#     ans = answers2[int(callback_data['num2'])]
#     await bot.send_message(query.from_user.id, ans, parse_mode='html')
