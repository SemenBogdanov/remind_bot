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


# drop line
async def del_by_id(message: types.Message):
    text = message.text
    # logging.info(text)
    regex = r"^удалить \d+$"
    check = re.match(regex, text)
    if check:
        logging.info("Проверка регулярного выражения прошла успешно!")
        reply_text = botDatabase.del_by_id(int(re.sub(r"удалить ", "", text)))
        if reply_text:
            await message.reply('Запись успешно удалена!')
        else:
            await message.reply('Ошибка при удалении записи')
    else:
        await message.reply("Запрос на удаление не соответствует шаблону!")


# find by surname
async def find_by_surname(message: types.Message):
    text = message.text
    # logging.info(text)
    regex = r"найти \w+\b"
    check = re.match(regex, text)
    reply_text = ""
    if check:
        logging.info("Проверка регулярного выражения прошла успешно!")
        surname = "%" + re.sub(r"найти ", "", text) + "%"
        res = botDatabase.find_by_surname(surname)
        logging.info(surname)
        if res:
            for r in res:
                reply_text += "ID: {}, Name: {}, Birthday: {}\n".format(r[0], r[1], r[2])
            await message.reply(reply_text)
        else:
            print(res)
            await message.reply('Ошибка при выполнении запроса!\n')
    else:
        await message.reply("Запрос не соответствует шаблону!")


# register handlers
def register_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(get_all_records, text_contains=['все др'])
    dp.register_message_handler(add_birthday, text_contains=['добавить др'])
    dp.register_message_handler(del_by_id, text_contains=['удалить '])
    dp.register_message_handler(find_by_surname, text_contains=['найти '])
