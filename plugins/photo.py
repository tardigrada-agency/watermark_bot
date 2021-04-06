from pyrogram import Client, filters
import utils
import db


@Client.on_message(filters.photo & utils.check_user)
async def photo(client, message):
    """
    Вызываеться когда пользователь прислал фотографию
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    try:
        user = db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Удаляем фото с такимже file_unique_id если оно уже почему-то есть
        utils.remove_photo(message.photo.file_unique_id)

        # Скачиваем фото из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_photo(message.photo, client, status)

        # Обработка фотографии
        await utils.logo_on_photo(f'{message.photo.file_unique_id}.jpg', user.size, user.color, user.lang)

        # Отправляем фото в телеграмм
        await client.send_chat_action(message.chat.id, action='upload_photo')
        await client.send_photo(chat_id=message.from_user.id,
                                photo=f'temp/{message.photo.file_unique_id}_logo.jpg',
                                progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    utils.remove_photo(message.photo.file_unique_id)  # Удаляем фото, оно нам больше не нужно


@Client.on_message(utils.document_image & utils.check_user)
async def photo_document(client, message):
    """
    Вызываеться когда пользователь прислал фотографию как документ
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    try:
        user = db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Удаляем фото с такимже file_unique_id если оно уже почему-то есть
        utils.remove_photo(message.document.file_unique_id)

        # Скачиваем фото из телеграмма
        status = await message.reply_text('Скачал 0%')
        await download_photo(message.document, client, status)

        # Обработка фотографии
        await status.edit_text('Обработка...')
        await utils.logo_on_photo(f'{message.document.file_unique_id}.jpg', user.size, user.color, user.lang)

        # Отправляем фото в телеграмм
        await client.send_chat_action(message.chat.id, action='upload_document')
        await client.send_document(chat_id=message.from_user.id,
                                   document=f'temp/{message.document.file_unique_id}_logo.jpg',
                                   file_name=f'{message.document.file_name.split(".")[0]}_logo.jpg',
                                   progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    utils.remove_photo(message.document.file_unique_id)  # Удаляем фото, оно нам больше не нужно


async def download_photo(file, client, status):
    """
    Функция для скачивания файла с сервера телеграмм
    :param status: : Сообщение чтобы показывать юзеру что происходит
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.jpg',
                                progress=utils.download_callback, progress_args=(status,))
