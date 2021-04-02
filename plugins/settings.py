from pyrogram import Client, filters
import keyboards
import db
import utils


@Client.on_message(filters.regex(pattern=r'^.*язык.*$') & filters.private & utils.check_user)
async def language_select(client, message):
    """
    Присылает клавиатуру выбора языка логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply('Выбери язык:', reply_markup=keyboards.language_keyboard)


@Client.on_callback_query(utils.language & utils.check_user)
async def language_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.language_keyboard
    :param client:
    :param query:
    :return:
    """
    user = db.get_user(query.from_user.id)
    user.lang = query.data.split('=')[1]
    user.save()

    await client.answer_callback_query(query.id, text=f'Язык установлен!')


@Client.on_message(filters.regex(pattern='^.*цвет.*$') & filters.private & utils.check_user)
async def color_select(client, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply('Выбери цвет:', reply_markup=keyboards.color_keyboard)


@Client.on_callback_query(utils.color & utils.check_user)
async def color_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client:
    :param query:
    :return:
    """
    user = db.get_user(query.from_user.id)
    user.color = query.data.split('=')[1]
    user.save()
    await client.answer_callback_query(query.id, text=f'Цвет установлен!')


@Client.on_message(filters.regex(pattern='^.*размер.*$') & filters.private & utils.check_user)
async def size_select(client, message):
    """
    Присылает клавиатуру выбора размера логотипа
    :param client:
    :param message:
    :return:
    """
    await message.reply('Выбери цвет:', reply_markup=keyboards.size_keyboard)


@Client.on_callback_query(utils.size & utils.check_user)
async def size_callback(client, query):
    """
    Принимает callback от нажатия кнопок в keyboards.size_keyboard
    :param client:
    :param query:
    :return:
    """
    user = db.get_user(query.from_user.id)
    user.size = query.data.split('=')[1]
    await client.answer_callback_query(query.id, text=f'Размер установлен!')
