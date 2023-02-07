from aiogram.utils import executor

from create import dp
from handlers import client, admin
from database import sqlite_db

async def on_startup(_):
    print('Bot is online')
    sqlite_db.sq_start()

if __name__ == '__main__':
    client.reg_handlers(dp)
    admin.reg_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)