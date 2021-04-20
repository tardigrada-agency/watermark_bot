from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для выбора цвета логотипа
colors = {'⚫': 'black', '⚪': 'white'}
color_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_color={v}') for k, v in colors.items())
]])

# Клавиатура для выбора размера логотипа
sizes = {'small': 1, 'middle': 2, 'big': 3}
size_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_size={v}') for k, v in sizes.items())
]])

# Клавиатура для выбора языка логотипа
languages = {'🇬🇧': 'eng'}
language_keyboard = InlineKeyboardMarkup([[
    *(InlineKeyboardButton(k, callback_data=f'new_language={v}') for k, v in languages.items())
]])

# Главное меню
menu = ('цвет', 'размер', 'язык')
menu_keyboard = ReplyKeyboardMarkup([[
    *(KeyboardButton(i) for i in menu)
]])


