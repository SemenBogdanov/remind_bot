import logging
import re

from aiogram import types, Dispatcher

from create_bot import botDatabase


# handlers
# select * from people
async def get_all_records(message: types.Message):
    res = botDatabase.get_all_records()
    # logging.info(res)
    reply_text = ''
    for r in res:
        reply_text += "ID: {}, Name: {}, Birthday: {}\n".format(r[0], r[1], r[2])

    await message.answer(reply_text)


# insert into people(x,y) values (x,y)
async def add_birthday(message: types.Message):
    text = message.text
    # logging.info(text)
    regex = r"^добавить др \w{2,} \w{2,} \d{2}.(\d{2}).\d{4}"
    check = re.match(regex, text)
    if check:
        logging.info("Проверка регулярного выражения прошла успешно!")
        text = text.split(' ')
        name = text[2] + ' ' + text[3]
        date = text[4][6:10] + '-' + text[4][3:5] + '-' + text[4][0:2]
        logging.info("Name: {}, Date: {}".format(name, date))
        reply_text = botDatabase.add_birthday(p_name=name, p_date=date)
        if reply_text:
            await message.reply('Запись успешно добавлена в базу')
    else:
        await message.reply('Строка для записи не соответствует шаблону: \n"добавить др ИМЯ ДАТА')


# register handlers
def register_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(get_all_records, text_contains=['все др'])
    dp.register_message_handler(add_birthday, text_contains=['добавить др'])
