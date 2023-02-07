from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#main menu keyboard
major_menu_client_kb = InlineKeyboardMarkup(row_width=1)
brend_btn = InlineKeyboardButton("🛒 Бренды", callback_data="open_brends")
favorite_btn = InlineKeyboardButton("🌟 Избранное", callback_data="open_favorites")
main_shop_link_btn = InlineKeyboardButton("🛍️ Магазин RILL STUFF", url="https://t.me/stuffrilldance")
major_menu_client_kb.add(brend_btn, favorite_btn, main_shop_link_btn)
#-------------------