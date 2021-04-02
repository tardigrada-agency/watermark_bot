from pyrogram import Client, filters
import keyboards
import utils
import db


@Client.on_message(filters.command(commands=['start', 'help']) & filters.private)
async def send_welcome(client, message):
    text = f"Привет!\nЯ лого бот ИА 'Тардиграда'!\nТвой ид: {message.from_user.id}\n"
    if db.check_user(message.from_user.id):
        await message.reply_text(text, reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text(text)


@Client.on_message(~utils.check_user & filters.private)
async def no_access(client, message):
    """
    Если у пользователя нет доступа для работы с ботом - сообщим ему об этом
    :param client:
    :param message:
    :return:
    """
    await message.reply(f"У тебя нет доступа :(\nТвой ид: {message.chat.id}")
