from pyrogram import Client, filters
import keyboards
import utils
import db


@Client.on_message(filters.regex(pattern=r'^\/adduser \d*$') & filters.private & utils.check_user)
async def adduser(client, message):
    """
    Для добавления новых пользователей в базу
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    user_id = message.text.split(' ')[1]
    if not db.check_user(user_id):  # Проверяем есть ли юзер в базе
        db.add_user(user_id)  # Добавляем
        await message.reply_text(f'"{user_id}" добавлен')
        await client.send_message(user_id, 'Тебя добавили в базу!\n'
                                           'Теперь ты можешь:\n'
                                           ' - Пользоватся ботом\n'
                                           ' - Добавлять новых пользователей командой /adduser {ID}\n',
                                  reply_markup=keyboards.menu_keyboard)
    else:
        await message.reply_text('ERROR: Юзер уже есть в базе :(')  # Если юзер уже есть в базе - вернем ошибку


@Client.on_message(filters.regex(pattern=r'^.*настройки.*$') & utils.check_user)
@Client.on_message(filters.command(commands='settings') & utils.check_user)
async def settings(_, message):
    """
    Чтение настроек логотипа из базы
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    user = db.get_user(message.from_user.id)    # получаем юзера из базы по его ид
    await message.reply_text(f'цвет: {user.color}\n'
                             f'размер: {user.size}\n'
                             f'язык: {user.lang}\n'
                             f'режим: {user.mode}',
                             reply_markup=keyboards.menu_keyboard)


@Client.on_message(filters.command(commands='users') & utils.check_user)
async def users(client, message):
    """
    Чтение настроек логотипа из базы
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    users_settings: str = ''
    for user in db.User.objects:
        users_settings += f'{user.id}: {user.lang}, {user.color}, {user.size}, {user.mode}\n'
    await client.send_message(message.chat.id, users_settings,
                              reply_markup=keyboards.menu_keyboard)


@Client.on_message(filters.command(commands='keyboard') & utils.check_user & filters.private)
async def send_keyboard(_, message):
    """
    Выдача клавиатуры пользователю
    :param _: Клиент для работы с телеграмом, нам он не нужен
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    await message.reply_text('Воть ^-^', reply_markup=keyboards.menu_keyboard)
