from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import sqlite_db

#general btn
cancel_btn = InlineKeyboardButton("В главное меню", callback_data="exit")
back_btn = InlineKeyboardButton("Назад", callback_data="back")

#admin buttons
brends_btn = InlineKeyboardButton("Бренды", callback_data="open_brends")
add_brend_btn = InlineKeyboardButton("Добавить бренд", callback_data="add_brend")
delete_brend_btn = InlineKeyboardButton("Удалить бренд", callback_data="delete_brend")

add_catalog_btn = InlineKeyboardButton("Добавить каталог", callback_data="add_catalog")
delete_catalog_btn = InlineKeyboardButton("Удалить каталог", callback_data="delete_catalog")

add_subcatalog_btn = InlineKeyboardButton("Добавить подкаталог", callback_data="add_subcatalog")
delete_subcatalog_btn = InlineKeyboardButton("Удалить подкаталог", callback_data="delete_subcatalog")

add_item_btn = InlineKeyboardButton("Добавить товар", callback_data="add_item")
delete_item_btn = InlineKeyboardButton("Удалить товар", callback_data="delete_item")

next_btn = InlineKeyboardButton("Следующий товар", callback_data="next")
prev_btn = InlineKeyboardButton("Предыдущий товар", callback_data="prev")
change_price = InlineKeyboardButton("Изменить цену", callback_data="change_price")

#main menu keyboard
main_admin_kb = InlineKeyboardMarkup(row_width=1)
main_admin_kb.add(brends_btn, cancel_btn)

#generate markup
def gen_brend_mark():
    markup = InlineKeyboardMarkup(row_width=2)
    data = sqlite_db.get_brends()
    lst = []
    for dt in data:
        lst.append(dt[0])
    lst = set(lst)
    for item in lst:
        markup.insert(InlineKeyboardButton(item, callback_data=item))
    markup.add(back_btn)
    return markup

def gen_catalog_mark(brend):
    markup = InlineKeyboardMarkup(row_width=2)
    data = sqlite_db.get_catalog(brend)
    lst = []
    for dt in data:
        lst.append(dt[1])
    lst = set(lst)
    for item in lst:
        markup.insert(InlineKeyboardButton(item, callback_data=item))
    markup.add(cancel_btn, back_btn)
    return markup

def gen_subcatalog_mark(catalog, brend):
    markup = InlineKeyboardMarkup(row_width=2)
    data = sqlite_db.get_subcatalog(catalog, brend)
    lst = []
    for dt in data:
        lst.append(dt[2])
    lst = set(lst)
    for item in lst:
        markup.insert(InlineKeyboardButton(item, callback_data=item))
    markup.add(cancel_btn, back_btn)
    return markup

def gen_items_mark(subcatalog, catalog, brend):
    markup = InlineKeyboardMarkup(row_width=2)
    data = sqlite_db.get_items(subcatalog, catalog, brend)
    for id in data:
        markup.insert(InlineKeyboardButton(data[id], callback_data=id))
    markup.add(cancel_btn, back_btn)
    return markup

def gen_item_mark(item_id):
    markup = InlineKeyboardMarkup(row_width=2)
    data = sqlite_db.get_item(item_id)
    for dt in data:
        markup.insert(InlineKeyboardButton(dt[2], callback_data=dt[2]))
    markup.add(prev_btn, next_btn,cancel_btn, back_btn)
    return markup