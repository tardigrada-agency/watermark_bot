from pyrogram import Client, filters
import keyboards
import db
import utils


@Client.on_message(filters.regex(pattern='^.*язык.*$') & filters.private)
async def language_select(client, message):
    """
    Присылает клавиатуру выбора языка логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply("Выбери язык:", reply_markup=keyboards.language_keyboard)


@Client.on_callback_query(utils.language)
async def language_callback(client, data):
    """
    Принимает callback от нажатия кнопок в keyboards.language_keyboard
    :param client:
    :param data:
    :return:
    """
    await client.answer_callback_query(data.id, text=f"Язык установлен!")


@Client.on_message(filters.regex(pattern='^.*цвет.*$') & filters.private)
async def color_select(client, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply("Выбери цвет:", reply_markup=keyboards.color_keyboard)


@Client.on_callback_query(utils.color)
async def color_callback(client, data):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client:
    :param data:
    :return:
    """
    await client.answer_callback_query(data.id, text=f"Цвет установлен!")


@Client.on_message(filters.regex(pattern='^.*размер.*$') & filters.private)
async def size_select(client, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply("Выбери цвет:", reply_markup=keyboards.size_keyboard)


@Client.on_callback_query(utils.size)
async def size_callback(client, data):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client:
    :param data:
    :return:
    """
    await client.answer_callback_query(data.id, text=f"Размер установлен!")
