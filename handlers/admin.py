from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from create import bot

import handlers

import keyboards

import database

ADMIN_ID = *

ADMIN_WELCOME_MESSAGE = """*Здравствуйте \!* _Это ваш покорный слуга_\. 
Чтобы вы хотели во мне изменить \?"""

BRENDS_MESSAGE = """_Здесь вы можете просмотреть и изменить все имеющиеся_ *бренды*\.
Что хотите сделать\?"""
ADD_BRENDS_MESSAGE = """Введите название *бренда* ,который хотите добавить\."""

CATALOG_MESSAGE = """_Здесь вы можете просмотреть и изменить все имеющиеся_ *каталоги* бренда\.
Что хотите сделать\?"""
ADD_CATALOG_MESSAGE = "Введите название *каталога* ,который хотите добавить\."

SUBCATALOG_MESSAGE = """_Здесь вы можете просмотреть и изменить все имеющиеся_ *подкаталоги* каталога\.
Что хотите сделать\?"""
ADD_SUBCATALOG_MESSAGE = "Введите название *подкаталога* ,который хотите добавить\."

ITEMS_MESSAGE = """_Здесь вы можете просмотреть и изменить все имеющиеся_ *товары* подкаталога\.
Что хотите сделать\?"""
ADD_ID_OF_ITEM_MESSAGE = "Введите *артикул* товара ,который хотите добавить\."
ADD_NAME_OF_ITEM_MESSAGE = "Введите *название* товара ,который хотите добавить\."
ADD_SIZES_OF_ITEM_MESSAGE = "Введите  *размеры* товара\."
ADD_COUNT_OF_ITEM_MESSAGE = "Введите *количество* товара, согласно размерам\."
ADD_PRICE_OF_ITEM_MESSAGE = "Введите *цену* товара\."

CHANGE_PRICE_OF_ITEM_MESSAGE = "Введите новую *цену* товара\."
NEW_PRICE_MESSAGE = "Новая *цена* установлена\."

CHANGE_SIZE_COUNT_OF_ITEM_MESSAGE = "Введите новое *количество* товара\."
NEW_COUNT_MESSAGE = "Новое *количество* установлено\."

DELETE_MESSAGE = "Позиция удалена"
ADD_MESSAGE = "Позиция добавлена"

class FSMadmin(StatesGroup):
    main = State()

    admin_brends = State()
    add_brend = State()

    admin_catalog = State()
    add_catalog = State()

    admin_subcatalog = State()
    add_subcatalog = State()

    admin_items = State()
    add_id = State()
    add_name = State()
    add_size = State()
    add_count = State()
    add_price = State()

    admin_item = State()
    change_price = State()
    change_size_count = State()

#-----------start-----------
async def admin_start(msg: types.Message):
    if msg.from_user.id == ADMIN_ID:
        await FSMadmin.main.set()
        await bot.send_message(msg.from_user.id, ADMIN_WELCOME_MESSAGE, reply_markup=keyboards.main_admin_kb, parse_mode="MarkdownV2")
        await msg.answer("")
#----------------------

#-----------general methods-----------
async def cancel_command(cb: types.CallbackQuery, state: FSMContext):
    if cb.from_user.id == ADMIN_ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await handlers.client.start_command(cb)
        await cb.answer('Ok')

async def back_command(cb: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == "FSMadmin:admin_brends":
        await state.reset_state()
        await admin_start(cb)
    elif current_state == "FSMadmin:admin_catalog":
        await change_brends(cb)
    elif current_state == "FSMadmin:admin_subcatalog":
        await change_catalog(cb, state)
    elif current_state == "FSMadmin:admin_items":
        await change_subcatalog(cb, state)
    elif current_state == "FSMadmin:admin_item":
        await change_items(cb, state)
#----------------------

#-----------work with brends menu-----------
async def change_brends(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, BRENDS_MESSAGE, reply_markup=keyboards.gen_brend_mark().add(keyboards.add_brend_btn), parse_mode="MarkdownV2")
    await cb.answer("")
    await FSMadmin.admin_brends.set()

async def add_brends(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, ADD_BRENDS_MESSAGE, parse_mode="MarkdownV2")
    await cb.answer("")
    await FSMadmin.add_brend.set()

async def new_brend(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_brend'] = msg.text
            database.sqlite_db.add_to_shop((data['add_brend'], "Unknown", "Unknown", f"{data['add_brend']+str(database.sqlite_db.get_row_count())}"))
        await bot.send_message(msg.from_user.id, ADD_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_brends.set()
        await change_brends(msg)
#----------------------

#-----------work with catalog of brend menu-----------
async def change_catalog(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back" and cb.data != "delete_catalog":
                data['brends'] = cb.data
        await bot.send_message(cb.from_user.id, CATALOG_MESSAGE,
                               reply_markup=keyboards.gen_catalog_mark(data['brends']).add(keyboards.add_catalog_btn, keyboards.delete_brend_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_catalog.set()
    except:
        await bot.send_message(cb.from_user.id, CATALOG_MESSAGE,
                               reply_markup=keyboards.gen_catalog_mark(data['brends']).add(keyboards.add_catalog_btn, keyboards.delete_brend_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_catalog.set()

async def add_catalog(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, ADD_CATALOG_MESSAGE,
                           parse_mode="MarkdownV2")
    await cb.answer("")
    await FSMadmin.add_catalog.set()

async def new_catalog(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_catalog'] = msg.text
            database.sqlite_db.add_to_shop((data['brends'], data['add_catalog'], "Unknown", f"Unknown{data['brends']+data['add_catalog']+str(database.sqlite_db.get_row_count())}"))
            database.sqlite_db.delete_catalog_from_sql(data['brends'], "Unknown")
        await bot.send_message(msg.from_user.id, ADD_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_catalog.set()
        await change_catalog(msg,state)

async def delete_brends(cb: types.CallbackQuery, state: FSMContext):
    if cb.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            database.sqlite_db.delete_brend_from_sql(data['brends'])
        await bot.send_message(cb.from_user.id, DELETE_MESSAGE)
        await cb.answer("")
        await change_brends(cb)
#----------------------

#-----------work with subcatalog of catalog menu-----------
async def change_subcatalog(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back" and cb.data != "delete_subcatalog":
                data['catalog'] = cb.data
        await bot.send_message(cb.from_user.id, SUBCATALOG_MESSAGE,
                               reply_markup=keyboards.gen_subcatalog_mark(data['catalog'], data['brends']).add(keyboards.add_subcatalog_btn, keyboards.delete_catalog_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_subcatalog.set()
    except:
        await bot.send_message(cb.from_user.id, SUBCATALOG_MESSAGE,
                               reply_markup=keyboards.gen_subcatalog_mark(data['catalog'], data['brends']).add(keyboards.add_subcatalog_btn, keyboards.delete_catalog_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_subcatalog.set()

async def add_subcatalog(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, ADD_SUBCATALOG_MESSAGE, parse_mode="MarkdownV2")
    await cb.answer("")
    await FSMadmin.add_subcatalog.set()

async def new_subcatalog(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_subcatalog'] = msg.text
            database.sqlite_db.add_to_shop((data['brends'], data['catalog'], data['add_subcatalog'], f"Unknown{data['brends']+data['catalog']+data['add_subcatalog']+str(database.sqlite_db.get_row_count())}"))
            database.sqlite_db.delete_subcatalog_from_sql(data['brends'], data['catalog'], "Unknown")
        await bot.send_message(msg.from_user.id, ADD_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_subcatalog.set()
        await change_subcatalog(msg, state)

async def delete_catalog(cb: types.CallbackQuery, state: FSMContext):
    if cb.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            database.sqlite_db.delete_catalog_from_sql(data['brends'], data['catalog'])
        await bot.send_message(cb.from_user.id, DELETE_MESSAGE)
        await cb.answer("")
        await change_catalog(cb, state)
#----------------------

#-----------work with items of subcatalog menu-----------

async def change_items(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back" and cb.data != "delete_item":
                data['subcatalog'] = cb.data
        await bot.send_message(cb.from_user.id, ITEMS_MESSAGE,
                               reply_markup=keyboards.gen_items_mark(data['subcatalog'], data['catalog'], data['brends']).add(keyboards.add_item_btn, keyboards.delete_subcatalog_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_items.set()
    except:
        await bot.send_message(cb.from_user.id, ITEMS_MESSAGE,
                               reply_markup=keyboards.gen_items_mark(data['subcatalog'], data['catalog'],data['brends']).add(keyboards.add_item_btn, keyboards.delete_subcatalog_btn),
                               parse_mode="MarkdownV2")
        await cb.answer("")
        await FSMadmin.admin_items.set()

async def add_item(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, ADD_ID_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
    await cb.answer("")
    await FSMadmin.add_id.set()

async def set_id(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_id'] = msg.text
        await bot.send_message(msg.from_user.id, ADD_NAME_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.add_name.set()

async def set_name(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_name'] = msg.text
        await bot.send_message(msg.from_user.id, ADD_SIZES_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.add_size.set()

async def set_size(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_size'] = msg.text
        await bot.send_message(msg.from_user.id, ADD_COUNT_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.add_count.set()

async def set_count(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_count'] = msg.text
        await bot.send_message(msg.from_user.id, ADD_PRICE_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.add_price.set()

async def set_price(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['add_price'] = msg.text
            database.sqlite_db.add_to_shop((data['brends'], data['catalog'], data['subcatalog'], data['add_id']))
            database.sqlite_db.delete_unknown_item_from_shop(data['brends'], data['catalog'], data['subcatalog'])
            database.sqlite_db.add_to_items((data['add_id'], data['add_name'], data['add_size'], data['add_count'], data['add_price']))
        await bot.send_message(msg.from_user.id, ADD_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_items.set()
        await change_items(msg, state)

async def delete_subcatalog(cb: types.CallbackQuery, state: FSMContext):
    if cb.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            database.sqlite_db.delete_subcatalog_from_sql(data['brends'], data['catalog'], data['subcatalog'])
        await bot.send_message(cb.from_user.id, DELETE_MESSAGE)
        await cb.answer("")
        await change_subcatalog(cb, state)

#----------------------

#-----------work with item of items menu-----------

async def change_item(cb: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            if cb.data != "back":
                data["item_id"] = cb.data
        await bot.send_message(cb.from_user.id, database.sqlite_db.gen_item_msg(data["item_id"]),
                               reply_markup=keyboards.gen_item_mark(data["item_id"]).add(keyboards.change_price, keyboards.delete_item_btn),
                               parse_mode="MarkdownV2")
        await FSMadmin.admin_item.set()
        await cb.answer("")
    except:
        await bot.send_message(cb.from_user.id, database.sqlite_db.gen_item_msg(data["item_id"]),
                               reply_markup=keyboards.gen_item_mark(data["item_id"]).add(keyboards.change_price, keyboards.delete_item_btn),
                               parse_mode="MarkdownV2")
        await FSMadmin.admin_item.set()
        await cb.answer("")

async def change_price(cb: types.CallbackQuery):
    await bot.send_message(cb.from_user.id, CHANGE_PRICE_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
    await FSMadmin.change_price.set()
    await cb.answer("")

async def new_price(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            database.sqlite_db.change_item_price(data["item_id"], int(msg.text))
        await bot.send_message(msg.from_user.id, NEW_PRICE_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_item.set()
        await change_item(msg, state)

async def delete_item(cb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        database.sqlite_db.delete_item_from_sql(data["item_id"])
    await bot.send_message(cb.from_user.id, DELETE_MESSAGE, parse_mode="MarkdownV2")
    await change_items(cb, state)
    await cb.answer("")
#----------------------

#-----------work with size of item menu-----------

async def change_size_count(cb: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["size"] = cb.data
    await bot.send_message(cb.from_user.id, CHANGE_SIZE_COUNT_OF_ITEM_MESSAGE, parse_mode="MarkdownV2")
    await FSMadmin.change_size_count.set()
    await cb.answer("")

async def new_count(msg: types.Message, state: FSMContext):
    if msg.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            database.sqlite_db.change_size_count(data["size"], int(msg.text))
        await bot.send_message(msg.from_user.id, NEW_COUNT_MESSAGE, parse_mode="MarkdownV2")
        await FSMadmin.admin_item.set()
        await change_item(msg, state)

#----------------------

def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['admin'])
    dp.register_callback_query_handler(cancel_command, text="exit", state="*")
    dp.register_callback_query_handler(back_command, text="back", state="*")

    dp.register_callback_query_handler(change_brends, text=["open_brends", "back"], state=FSMadmin.main)
    dp.register_callback_query_handler(add_brends, text="add_brend", state=FSMadmin.admin_brends)
    dp.register_message_handler(new_brend, state=FSMadmin.add_brend)

    dp.register_callback_query_handler(change_catalog, lambda cb: True, state=FSMadmin.admin_brends)
    dp.register_callback_query_handler(add_catalog, text="add_catalog", state=FSMadmin.admin_catalog)
    dp.register_message_handler(new_catalog, state=FSMadmin.add_catalog)
    dp.register_callback_query_handler(delete_brends, text="delete_brend", state=FSMadmin.admin_catalog)

    dp.register_callback_query_handler(change_subcatalog, lambda cb: True, state=FSMadmin.admin_catalog)
    dp.register_callback_query_handler(add_subcatalog, text="add_subcatalog", state=FSMadmin.admin_subcatalog)
    dp.register_message_handler(new_subcatalog, state=FSMadmin.add_subcatalog)
    dp.register_callback_query_handler(delete_catalog, text="delete_catalog", state=FSMadmin.admin_subcatalog)

    dp.register_callback_query_handler(change_items, lambda cb: True, state=FSMadmin.admin_subcatalog)
    dp.register_callback_query_handler(add_item, text="add_item", state=FSMadmin.admin_items)
    dp.register_message_handler(set_id, state=FSMadmin.add_id)
    dp.register_message_handler(set_name, state=FSMadmin.add_name)
    dp.register_message_handler(set_size, state=FSMadmin.add_size)
    dp.register_message_handler(set_count, state=FSMadmin.add_count)
    dp.register_message_handler(set_price, state=FSMadmin.add_price)
    dp.register_callback_query_handler(delete_subcatalog, text="delete_subcatalog", state=FSMadmin.admin_items)

    dp.register_callback_query_handler(change_item, lambda cb: True, state=FSMadmin.admin_items)
    dp.register_callback_query_handler(change_price, text="change_price", state=FSMadmin.admin_item)
    dp.register_message_handler(new_price, state=FSMadmin.change_price)
    dp.register_callback_query_handler(delete_item, text="delete_item", state=FSMadmin.admin_item)

    dp.register_callback_query_handler(change_size_count, lambda cb: True, state=FSMadmin.admin_item)
    dp.register_message_handler(new_count, state=FSMadmin.change_size_count)
