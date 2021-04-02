from pyrogram import filters
import os
import db


# Custom filters
check_user = filters.create(lambda _, __, message: db.check_user(message.chat.id))
language = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_language')
size = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_size')
color = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_color')


async def remove_video(file_id):
    """
    Удаляем видео для file_id
    :param file_id:
    :return:
    """
    if os.path.isfile(f"documents/{file_id}.mp4"):
        os.remove(f"documents/{file_id}.mp4")
    if os.path.isfile(f"documents/{file_id}_logo.mp4"):
        os.remove(f"documents/{file_id}_logo.mp4")


async def remove_photo(file_id):
    """
    Удаляем фото для file_id
    :param file_id:
    :return:
    """
    if os.path.isfile(f"documents/{file_id}.jpg"):
        os.remove(f"documents/{file_id}.jpg")
    if os.path.isfile(f"documents/{file_id}_logo.jpg"):
        os.remove(f"documents/{file_id}_logo.jpg")


async def download_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % скачивания файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    await status.edit_text(f"Скачал {int((current/total)*100)}%")


async def upload_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % загрузки файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    await status.edit_text(f"Загрузил {int((current/total)*100)}%")
