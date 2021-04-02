from pyrogram import Client, filters
import keyboards
import utils
import db


@Client.on_message(filters.regex(pattern=r'^\/adduser \d*$') & filters.private & utils.check_user )
async def adduser(client, message):
    """
    Для добавления новых пользователей в базу
    :param client:
    :param message:
    :return:
    """
    user_id = message.text.split(' ')[1]
    if not db.check_user(user_id):
        db.add_user(user_id)
        await message.reply_text(f'"{user_id}" добавлен')
        await client.send_message(user_id, 'Тебя добавили в базу!\n'
                                           'Теперь ты можешь:\n'
                                           ' - Пользоватся ботом\n'
                                           ' - Добавлять новых пользователей командой /adduser {ID}\n',
                                  reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text('Юзер уже есть в базе :(')


@Client.on_message(filters.regex(pattern=r'^.*настройки.*$') & utils.check_user & utils.check_user )
@Client.on_message(filters.command(commands='settings') & utils.check_user & utils.check_user )
async def settings(client, message):
    """
    Чтение настроек логотипа из базы
    :param client:
    :param message:
    :return:
    """
    user = db.get_user(message.from_user.id)
    await message.reply_text(f'цвет: {user.color}\n'
                             f'размер: {user.size}\n'
                             f'язык: {user.lang}')


@Client.on_message(filters.command(commands='keyboard') & utils.check_user & filters.private)
async def send_keyboard(client, message):
    """
    Выдача клавиатуры пользователю
    :param client:
    :param message:
    :return:
    """
    await message.reply_text('Воть ^-^', reply_markup=keyboards.menu_keyboard)

