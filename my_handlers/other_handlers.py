from aiogram import types, Dispatcher


# handlers
async def get_my_chat_id(message: types.Message):
    await message.answer('This is your chat.id = ' + str(message.chat.id))


async def reply_welcome(message: types.Message):
    await message.reply('Привет! Я Аля - бот-помощник! Скоро будет база данных!')


# register handlers
def register_other_functions(dp: Dispatcher):
    dp.register_message_handler(get_my_chat_id, commands=['mychatid'])
    dp.register_message_handler(reply_welcome, text=['hello', 'привет', 'как дела'])

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
