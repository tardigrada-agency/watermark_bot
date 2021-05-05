from pyrogram import Client
import keyboards
import zipfile
import shutil
import utils
import re
import db
import os


@Client.on_message(utils.document_zip & utils.check_user)
async def zip_file(client, message):
    """
    Добавляет ватермарку на все файлы в zip архиве
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    utils.remove_zip(message.document.file_unique_id)  # Удаляем архив с таким ид если оно уже почему-то есть
    try:
        user = db.get_user(message.from_user.id)  # Получаем юзера из базы
        re_photo = re.compile(r'(^.*\.)jpe?g|png')
        re_video = re.compile(r'(^.*\.)mov|mp4|avi')

        # Скачиваем архив
        status = await message.reply_text('Скачал 0%')
        await download_zip(message.document, client, status)

        # Раскрываем архив
        await status.edit_text('extracting....')
        with zipfile.ZipFile(f'temp/{message.document.file_unique_id}.zip', 'r') as zipObj:
            zipObj.extractall(f'temp/{message.document.file_unique_id}')

        os.mkdir(f'temp/{message.document.file_unique_id}_logo')  # Создаем папку для файлов с логотипом

        #   Для всех файлов из архива запускам ffmpeg
        path = f'temp/{message.document.file_unique_id}'
        for root, dirs, files in os.walk(path):
            for file in files:
                if re_photo.match(file.lower()):
                    await status.edit_text(f'Обработка фотографии {file}')
                    await utils.draw_logo_on_photo(f'{message.document.file_unique_id}'
                                                   f'{root.replace(f"temp/{message.document.file_unique_id}", "")}/'
                                                   f'{file}', user.size,
                                                   user.color, user.lang, user.mode)
                    shutil.move(f'temp/{message.document.file_unique_id}'
                                f'{root.replace(f"temp/{message.document.file_unique_id}", "")}/'
                                f'{utils.get_filename(file)}_logo.jpg',
                                f'temp/{message.document.file_unique_id}_logo/{file}')
                if re_video.match(file.lower()):
                    await status.edit_text(f'Обработка видео {file}')
                    await utils.draw_logo_on_video(f'{message.document.file_unique_id}'
                                                   f'{root.replace(f"temp/{message.document.file_unique_id}", "")}/'
                                                   f'{file}', user.size, user.color, user.lang, user.mode)
                    shutil.move(f'temp/'
                                f'{message.document.file_unique_id}'
                                f'{root.replace(f"temp/{message.document.file_unique_id}", "")}/'
                                f'{utils.get_filename(file)}_logo.mp4',
                                f'temp/{message.document.file_unique_id}_logo/{file}')

        # Создаем новый архив из файлоы с логотипом
        await status.edit_text(f'Архивация...')
        await zip_dir(message.document.file_unique_id)

        # Отправляем архив
        await client.send_chat_action(message.chat.id, action='upload_document')
        await client.send_document(chat_id=message.from_user.id,
                                   document=f'temp/{message.document.file_unique_id}_logo.zip',
                                   file_name=f'{utils.get_filename(message.document.file_name)}_logo.zip',
                                   progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    utils.remove_zip(message.document.file_unique_id)  # Удаляем архив, оно нам больше не нужно


async def download_zip(file, client, status):
    """
    Функция для скачивания файла с сервера телеграмм
    :param status: : Сообщение чтобы показывать юзеру что происходит
    :param file: Файл который нужно скачать
    :param client: Клиент для общения с телеграммом
    :return:
    """
    await client.download_media(message=file, file_name=f'temp/{file.file_unique_id}.zip',
                                progress=utils.download_callback, progress_args=(status,))


async def zip_dir(file_id):
    """
    Создает зип архив ./temp/{file_id}_logo.zip из папки ./temp/{file_id}_logo
    :param file_id: Ид изначального архива
    :return:
    """
    zip_archive = zipfile.ZipFile(f'./temp/{file_id}_logo.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(f'./temp/{file_id}_logo'):
        for file in files:
            zip_archive.write(os.path.join(root, file), arcname=file)
    zip_archive.close()
