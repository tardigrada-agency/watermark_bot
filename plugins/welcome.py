from pyrogram import Client, filters
import keyboards
import utils
import db


@Client.on_message(filters.command(commands=['start', 'help']) & filters.private)
async def send_welcome(_, message):
    """
    Функция которая срабатывает когда пользователь прислал /start (запустил бота) или /help
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message:
    :return:
    """
    text = f"Привет!\nЯ лого бот созданый ИА 'Тардиграда'!\nТвой ид: {message.from_user.id}\n"
    if db.check_user(message.from_user.id):
        await message.reply_text(text, reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text(text)
        await message.reply_text(text)


@Client.on_message(~utils.check_user & filters.private)
async def no_access(_, message):
    """
    Если у пользователя нет доступа для работы с ботом - сообщим ему об этом
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message:
    :return:
    """
    await message.reply(f"У тебя нет доступа :(\nТвой ид: {message.chat.id}")
