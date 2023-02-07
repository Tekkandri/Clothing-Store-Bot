from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create import bot
import keyboards
import database

WELCOME_MESSAGE = """*Добро пожаловать* _в главное меню чат\-бота онлайн\-магазина_ ["RILL SHOP"](https://t.me/stuffrilldance)\. \
Здесь мы можете ознакомиться со всем ассортиментом товаров и сделать заказ\. Просто воспользуйтесь кнопками _*меню*_, \
чтобы взаимодействовать с функциями бота\."""

BRENDS_MESSAGE = "В *Брендах* можете посмотреть список брендов\."
CATALOG_MESSGAE = "В _*Каталоге*_ вы можете посмотреть основные категории товаров\."
SUBCATALOG_MESSGAE = "В _*Полкаталоге*_ вы можете посмотреть все категории товаров\."

class FSMclient(StatesGroup):
    brends = State()
    catalog = State()
    subcatalog = State()
    item = State()

#-----------start-----------
async def start_command(msg: types.Message):
    await bot.send_message(msg.from_user.id, WELCOME_MESSAGE, reply_markup=keyboards.client_kb.major_menu_client_kb, parse_mode="MarkdownV2")
    await msg.answer("")
#----------------------

#-----------general methods-----------
async def cancel_command(cb: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await start_command(cb)
    await cb.answer('Ok')

async def back_command(cb: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "FSMclient:brends":
        await state.reset_state()
        await start_command(cb)
    elif current_state == "FSMclient:catalog":
        await brends_command(cb)
    elif current_state == "FSMclient:subcatalog":
        await catalog_command(cb, state)
    elif current_state == "FSMclient:item":
        await subcatalog_command(cb, state)
#----------------------

#-----------brends-----------
async def brends_command(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, BRENDS_MESSAGE, reply_markup=keyboards.gen_brend_mark(), parse_mode="MarkdownV2")
    await FSMclient.brends.set()
    await cb.answer("")
#----------------------

#-----------catalog-----------

async def catalog_command(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back":
                data["brends"] = cb.data
        await bot.send_message(cb.from_user.id, CATALOG_MESSGAE,
                               reply_markup=keyboards.admin_kb.gen_catalog_mark(data["brends"]),
                               parse_mode="MarkdownV2")
        await FSMclient.catalog.set()
        await cb.answer("")
    except:
        await bot.send_message(cb.from_user.id, CATALOG_MESSGAE,
                               reply_markup=keyboards.admin_kb.gen_catalog_mark(data["brends"]),
                               parse_mode="MarkdownV2")
        await FSMclient.catalog.set()
        await cb.answer("")

#----------------------

#-----------catalog-----------

async def subcatalog_command(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back":
                data["catalog"] = cb.data
        await bot.send_message(cb.from_user.id, CATALOG_MESSGAE,
                               reply_markup=keyboards.admin_kb.gen_subcatalog_mark(data["catalog"], data["brends"]),
                               parse_mode="MarkdownV2")
        await FSMclient.subcatalog.set()
        await cb.answer("")
    except:
        await bot.send_message(cb.from_user.id, CATALOG_MESSGAE,
                               reply_markup=keyboards.admin_kb.gen_subcatalog_mark(data["catalog"], data["brends"]),
                               parse_mode="MarkdownV2")
        await FSMclient.subcatalog.set()
        await cb.answer("")

#----------------------

#-----------item-----------

async def item_command(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back":
                data["subcatalog"] = cb.data
                data["items"] = database.sqlite_db.get_item_id_for_client(data["subcatalog"],data["catalog"],data["brends"])
                data["number"] = 0
        await bot.send_message(cb.from_user.id, database.sqlite_db.gen_item_msg(data["items"][0]),
                               reply_markup=keyboards.admin_kb.gen_item_mark(data["items"][0]),
                               parse_mode="MarkdownV2")
        await FSMclient.item.set()
        await cb.answer("")
    except:
        await bot.send_message(cb.from_user.id,database.sqlite_db.gen_item_msg(data["items"][0]),
                               reply_markup=keyboards.admin_kb.gen_item_mark(data["items"][0]),
                               parse_mode="MarkdownV2")
        await FSMclient.item.set()
        await cb.answer("")

async def next_command(cb: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data["number"] += 1
        await cb.message.edit_text(
                                   database.sqlite_db.gen_item_msg(data["items"][data["number"]]),
                                   parse_mode="MarkdownV2",
                                   reply_markup=keyboards.admin_kb.gen_item_mark(data["items"][data["number"]]))
        await cb.answer("")


async def prev_command(cb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data["number"] != 0:
            data["number"] -= 1
    await cb.message.edit_text(
                               database.sqlite_db.gen_item_msg(data["items"][data["number"]]),
                               parse_mode="MarkdownV2",
                               reply_markup=keyboards.admin_kb.gen_item_mark(data["items"][data["number"]]))
    await cb.answer("")

#----------------------

def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_callback_query_handler(cancel_command, text="exit", state="*")
    dp.register_callback_query_handler(back_command, text="back", state="*")

    dp.register_callback_query_handler(brends_command, text=["open_brends", "back"])
    dp.register_callback_query_handler(catalog_command, lambda cb: True, state=FSMclient.brends)
    dp.register_callback_query_handler(subcatalog_command, lambda cb: True, state=FSMclient.catalog)
    dp.register_callback_query_handler(item_command, lambda cb: True, state=FSMclient.subcatalog)

    dp.register_callback_query_handler(next_command, text="next", state=FSMclient.item)
    dp.register_callback_query_handler(prev_command, text="prev", state=FSMclient.item)