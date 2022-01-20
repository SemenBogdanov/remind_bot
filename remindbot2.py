import asyncio
import logging

from aiogram.utils import executor

import my_functions
import my_handlers
from create_bot import dp, botDatabase


async def on_startup(_):
    logging.info("Bot was started")


# register handlers from my_handlers_pocket
my_handlers.crud_handlers.register_crud_handlers(dp)
my_handlers.other_handlers.register_other_functions(dp)

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        delay = 60 ** 2 * 12
        loop.create_task(my_functions.other_functions.remind_me(delay))
        loop.create_task(my_functions.other_functions.remind_cnp(delay))
        loop.create_task(my_functions.other_functions.remind_week_cnp(delay))
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    except Exception as error:
        print('except \n' + str(error))
        botDatabase.conn.close()
