import asyncio
from datetime import datetime as dt
from datetime import timedelta as td

import emoji

from create_bot import botDatabase, bot
import logging


async def remind_me(wait_time=20):
    # today = str(datetime.datetime.today().date())

    while True:
        await asyncio.sleep(wait_time)
        try:
            # Получаем список друзей из БД в виде списка с кортежами внутри
            friends = botDatabase.get_friends()
            # Убираем год рождения, чтоб понять у кого сегодня день рождения
            format_date = '%d.%m'
            # Получаем текущую дату
            today = dt.strftime(dt.now(), format_date)
            remind_list = (x[0] for x in friends if x[1].strftime(format_date) == today)
            celebrants = ' \n'.join(remind_list)

            if bool(len(celebrants)):
                remind_msg = 'Сегодня праздник у друзей: \n{}'.format(celebrants)
                await bot.send_message(chat_id='287994530', text=remind_msg)
                # chat_id='-1001716787365'
            else:
                await bot.send_message(chat_id='287994530', text='Именинников сегодня нет')
            # print("---Проверка на дни рождения выполнена успешно")
        except Exception as e:
            pass
            # print("не удалось доставить напоминание")
            # print(e)


async def remind_cnp(wait_time=20):
    # today = str(datetime.datetime.today().date())

    while True:
        await asyncio.sleep(wait_time)
        try:
            # Получаем список друзей из БД в виде списка с кортежами внутри
            friends = botDatabase.get_colleagues()
            # Убираем год рождения, чтоб понять у кого сегодня день рождения
            format_date = '%d.%m'
            # Получаем текущую дату
            today = dt.strftime(dt.now(), format_date)
            remind_list = (x[0] for x in friends if x[1].strftime(format_date) == today)
            celebrants = ' \n'.join(remind_list)

            if bool(len(celebrants)):
                remind_msg = 'Сегодня праздник у коллег: \n{}'.format(celebrants)
                await bot.send_message(chat_id='-1001781029794', text=remind_msg)
                # chat_id='-1001716787365'
            else:
                # await bot.send_message(chat_id='-1001781029794', text='Именинников сегодня нет')
                print("Проверка на дни рождения выполнена успешно")
        except Exception as e:
            print("не удалось доставить напоминание")
            print(e)


async def remind_week_cnp(wait_time=20):
    while True:
        await asyncio.sleep(wait_time)
        try:
            # Получаем список друзей из БД в виде списка с кортежами внутри
            friends = botDatabase.get_colleagues()
            # logging.info(friends)
            # Убираем год рождения, чтоб понять у кого сегодня день рождения
            format_date = '%d.%m'
            # Получаем текущую дату
            today = dt.strptime(dt.strftime(dt.now() + td(days=14), format_date), '%d.%m')

            remind_list = (x[0] for x in friends if today >
                           dt.strptime(x[1].strftime(format_date), "%d.%m") >
                           dt.strptime(dt.now().strftime(format_date), "%d.%m"))
            celebrants = ' \n'.join(remind_list)

            # print(f'дата now: \n', dt.now())
            # print(f'дата today: \n', today)
            # print(f'список: \n', celebrants)
            heart = emoji.emojize(":red_heart:", variant="emoji_type")
            chats = ['-1001781029794']
            if bool(len(celebrants)):
                remind_msg = '{}ДЕНЬ РОЖДЕНИЯ ВПЕРЕДИ{}: \n{}'.format(heart, heart, celebrants)
                for x in chats:
                    logging.info(x)
                    await bot.send_message(chat_id=x, text=remind_msg)
                # chat_id='-1001716787365'
            else:
                pass
                # await bot.send_message(chat_id='-1001781029794', text='Именинников сегодня нет')
                # print("Проверка на дни рождения выполнена успешно")
        except Exception as e:
            # print("не удалось доставить напоминание")
            print(e)
