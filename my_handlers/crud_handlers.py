import logging
import re
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

import my_functions.other_functions
from create_bot import botDatabase

Admins = ['287994530']
'''
Кайшева Вероника - 386649114,
Семён Богданов - 287994530,
Екатерина Белякова - 163348459,
Полина Агалакова - 421596044
'''
AcceptedUsersForRead = ['287994530', '163348459', '386649114', '421596044']
AcceptedUsersForAdd = ['287994530', '163348459', '386649114', '421596044']


# handlers
# select * from people
async def get_all_records(message: types.Message):
    res = botDatabase.get_all_records()
    isAdmins = [x for x in Admins if x == str(message.from_user.id)]
    if any(isAdmins):
        # logging.info(res)
        reply_text = ''
        for r in res:
            reply_text += "ID: {}, Name: {}, Birthday: {}, Type:{}\n".format(r[0], r[1], r[2], r[3])
            if len(reply_text)>3900:
                await message.answer(reply_text)
                reply_text = ''
        await message.answer(reply_text)
    else:
        await message.answer('Нет доступа!')


async def get_all_colleagues(message: types.Message):
    res = botDatabase.get_colleagues()
    isAcceptedUsersForRead = [x for x in AcceptedUsersForRead if x == str(message.from_user.id)]
    if any(isAcceptedUsersForRead):
        # logging.info(res)
        reply_text = ''
        for r in res:
            reply_text += "Name: {}, Birthday: {}\n".format(r[0], r[1])

        await message.answer(reply_text)
        await message.answer(f'Всего сотрудников: {len(res)}')
    else:
        await message.answer('Нет доступа!')


# insert into people(x,y) values (x,y)
async def add_birthday(message: types.Message):
    text = message.text
    # logging.info(text)
    regex = r"^.обавить др \w{2,} \w{2,} \d{2}.(\d{2}).\d{4} \d{1}"
    check = re.match(regex, text)
    isAcceptedUsersForAdd = [x for x in AcceptedUsersForAdd if x == str(message.from_user.id)]
    if check and any(isAcceptedUsersForAdd):
        # logging.info("Проверка регулярного выражения прошла успешно!")
        text = text.split(' ')
        name = text[2] + ' ' + text[3]
        date = text[4][6:10] + '-' + text[4][3:5] + '-' + text[4][0:2]
        type_pers = text[len(text) - 1:len(text) - 2:-1][0]
        # logging.info("Name: {}, Date: {}, Type: {}".format(name, date, type_pers))
        reply_text = botDatabase.add_birthday(p_name=name, p_date=date, p_type=type_pers)
        if reply_text:
            await message.reply('Запись успешно добавлена в базу')
    else:
        await message.reply('Строка для записи не соответствует шаблону: \n'
                            'добавить др ИМЯ ФАМИЛИЯ ДАТА(дд.мм.гггг) ГРУППА(2-ЦНП) ')


# drop line
async def del_by_id(message: types.Message):
    text = message.text
    # logging.info(text)
    isAdmins = [x for x in Admins if x == str(message.from_user.id)]
    if any(isAdmins):
        regex = r"^.далить \d+$"
        check = re.match(regex, text)
        if check:
            # logging.info("Проверка регулярного выражения прошла успешно!")
            reply_text = botDatabase.del_by_id(int(re.sub(r"удалить ", "", text)))
            if reply_text:
                await message.reply('Запись успешно удалена!')
            else:
                await message.reply('Ошибка при удалении записи')
        else:
            await message.reply("Запрос на удаление не соответствует шаблону!")
    else:
        await message.reply("Нет доступа!")


# find by surname
async def find_by_surname(message: types.Message):
    res = ''
    text = message.text
    # logging.info(text)
    regex = r".айти \w+\b"
    check = re.match(regex, text)
    # logging.info(check)
    isAcceptedUsersForRead = [x for x in AcceptedUsersForRead if x == str(message.from_user.id)]
    isAdmins = [x for x in Admins if x == str(message.from_user.id)]
    reply_text = ""
    if check and any(isAcceptedUsersForRead) and str(message.chat.id) == '-1001781029794':
        surname = "%" + re.sub(r".айти ", "", text) + "%"
        # logging.info(surname)

        try:
            res = botDatabase.find_by_surname(surname, 2)
        except:
            # print(res)
            await message.reply('Ошибка при поиске в базе данных!\n')
            botDatabase.rolllback()

        if res:
            for r in res:
                reply_text += "ID: {}, Name: {}, Birthday: {}\n".format(r[0], r[1], r[2])
            await message.reply(reply_text)
        else:
            # print(res)
            await message.reply('Ошибка при выполнении запроса!\n')
            botDatabase.rolllback()

    if check and str(message.chat.id) != '-1001781029794':
        if any(isAdmins):
            surname = "%" + re.sub(r".айти ", "", text) + "%"
            try:
                res = botDatabase.find_by_surname(surname, 1)
            except Exception as e:
                # print(res)
                await message.reply(f'Ошибка при поиске в базе данных: {e}')
                await message.reply(f'Переменная res: {res}\n')

            for r in res:
                reply_text += "ID: {}, Name: {}, Birthday: {}\n".format(r[0], r[1], r[2])
            await message.reply(reply_text)
        else:
            await message.reply('Данный запрос необходимо выполнять только в общем чате.\n')


# register handlers
def register_crud_handlers(dp: Dispatcher):
    dp.register_message_handler(get_all_records, Text(equals='все др', ignore_case=True))
    dp.register_message_handler(add_birthday, Text(contains='добавить др', ignore_case=True))
    dp.register_message_handler(del_by_id, Text(contains='удалить', ignore_case=True))
    dp.register_message_handler(find_by_surname, Text(contains='найти', ignore_case=True))
    dp.register_message_handler(get_all_colleagues, Text(equals='др цнп', ignore_case=True))
