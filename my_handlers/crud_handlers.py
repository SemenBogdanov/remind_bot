from aiogram import types, Dispatcher
from create_bot import botDatabase


# handlers
# select * from people
async def get_all_records(message: types.Message):
    reply_text = botDatabase.get_all_records()
    await message.answer(reply_text)


# register handlers
def register_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(get_all_records, commands=['getall'])
