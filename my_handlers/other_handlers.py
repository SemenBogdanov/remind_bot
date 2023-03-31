import asyncio
import logging
from datetime import datetime as dt
from datetime import timedelta as td
from my_functions.other_functions import remind_week_cnp
import emoji
from aiogram import types, Dispatcher

# handlers
from create_bot import botDatabase, bot


async def formal_checklist(message: types.Message):
    await message.answer('''
1. Поток данных заведен в реестр потоков
2. Кодировка потоков соответствует стандартам
3. МИРО: 
3.1. Поток данных нанесен на доску
3.2. Указаны контакты со стороны поставщика данных
3.3. Указан формат поставки данных: "Вручную" или "Автоматически"
3.4. Указан логин SFTP, под которым происходит выкладка данных
3.5. Указана частота поставки данных, время, приходят ли данные в выходные
3.6. Указана ссылка на настройку в Ni-Fi
3.7. Указано название python-скриптов, участвующих в ETL
4. База данных:
4.1. Название таблицы созданов в сооветствии с соглашением о наименовании таблиц
4.2. Таблица и поля описаны через область комментариев 
4.3. Если есть поле "Регион": имя поля "region_name" varchar(2) с alpha
4.3. Если есть поле "Дата": имя поля "date" varchar(2) с alpha
5. Поток занесен в контрольное представление (КВ)
6. В КВ корректно идентифицируется контентная дата
7. Поток в Ni-Fi выходит в магистраль (запись ведется в журнал загрузок)''', parse_mode=types.ParseMode.HTML)


async def flow_do_checklist(message: types.Message):
    await message.answer('''
1. Завести задачу в PM-Bitrix24 <a href="https://pm.ac.gov.ru/company/personal/user/">LINK</a>
2. Добавить новый поток в таблицу потоков дата-офиса  <a href="https://sn.ac.gov.ru:5001/d/s/np57v5uvm1UbCvKC16JOBa
    nJKiTdpkHg/FFj5J87mBJd6eYxIx6rLpFJZ2fZ_OxbH-9LogldE6XAk">LINK</a>
3. PG_DEV: Создать таблицу и добавить описание полей, плюс комментарий
4. Python_DEV: Написать скрипт для последующего добавления в Ni-Fi
5. Python_DEV: Сделать деплой в ветку DEV в GitLab <a href="http://10.101.16.41/root/py_scr">LINK</a>
6. Ni-Fi_DEV: Сделать Pipiline, указать скрипт, указать таблицу в PG_DEV
7. Описать поток на доске MIRO проекта в группе датаофиса <a href="https://miro.com/app/dashboard/">LINK</a>
8. Протестировать поток
9. Сделать скриншоты из п.3, п.5, п.6 и прикрепить в задачу
10. Написать в соответстующие группы в ТГ: перенос из DEV в PROD. Обязательно прикрепить MIRO-link + PM_task_link

ps.: не забыть выключить процессоры в Ni-Fi_DEV''', parse_mode=types.ParseMode.HTML)


async def get_my_chat_id(message: types.Message):
    await message.answer('This is your chat.id = ' + str(message.chat.id))


async def help(message: types.Message):
    await message.answer('Помощь:\n'
                         '<b>др цнп</b> - вывод списка всех дней рождений, ранее записанных в базу данных\n'
                         '<b>добавить др</b> - добавляет новую запись о дне рождении в базу данных '
                         'по соответствующему шаблону'
                         '\n<b>найти (Фамилия)</b> - регистрозависимый поиск конкретной записи по фамилии сотрудника'
                         '\n<b>удалить (ID)</b> - удаляет запись с указанным номером'
                         '\n<b>др след</b> - вывод списка дней рождений, на следующей неделе'
                         '\n<b>/mychatid</b> - показать ID текущего чата'
                         '\n<b>/myuserid</b> - показать ID пользователя'
                         '\n<b>/flow_do_checklist</b> - чек-лист создания потока данных по стандартам до'
                         '\n<b>/formal_checklist</b> - формальный чек-лист создания потока данных по стандартам до'
                         '\n', parse_mode=types.ParseMode.HTML)


async def get_my_user_id(message: types.Message):
    await message.answer('This is your chat.id = ' + str(message.from_user))


async def reply_welcome(message: types.Message):
    await message.reply('Привет! Я могу напоминать тебе про дни рождения')


async def remind_next_week(message: types.Message):
    try:
        friends = botDatabase.get_colleagues()
        format_date = '%d.%m'
        today = dt.strptime(dt.strftime(dt.now() + td(days=10), format_date), '%d.%m')
        heart = emoji.emojize(":red_heart:", variant="emoji_type")

        remind_list = (x[0] + " " + x[1].strftime(format_date)
                       for x in friends if today >
                       dt.strptime(x[1].strftime(format_date), "%d.%m") >
                       dt.strptime(dt.now().strftime(format_date), "%d.%m"))
        celebrants = ' \n'.join(remind_list)

        chats = ['-1001781029794']
        if bool(len(celebrants)):
            remind_msg = '{}ДЕНЬ РОЖДЕНИЯ ДАЛЕЕ{}: \n{}'.format(heart, heart, celebrants)
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
    dp.register_message_handler(flow_do_checklist, commands=['flow_do_checklist'])
    dp.register_message_handler(formal_checklist, commands=['formal_flow_checklist'])
    # dp.register_message_handler(get_file_id, commands=['get_file_id'])

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
