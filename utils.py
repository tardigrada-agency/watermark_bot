from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import filters
import subprocess as sp
import shutil
import os
import db

# Custom filters
check_user = filters.create(lambda _, __, message: db.check_user(message.from_user.id))
new_language = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_language')
new_size = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_size')
new_color = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_color')
document_video = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'video' if message.document else False)
document_image = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'image' if message.document else False)
document_zip = filters.create(
    lambda _, __, message: message.document.mime_type == 'application/zip' if message.document else False)


def remove_video(file_id):
    """
    Удаляем видео для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    if os.path.isfile(f'temp/{file_id}.mp4'):
        os.remove(f'temp/{file_id}.mp4')
    if os.path.isfile(f'temp/{file_id}_logo.mp4'):
        os.remove(f'temp/{file_id}_logo.mp4')


def remove_photo(file_id):
    """
    Удаляем фото для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    if os.path.isfile(f'temp/{file_id}.jpg'):
        os.remove(f'temp/{file_id}.jpg')
    if os.path.isfile(f'temp/{file_id}_logo.jpg'):
        os.remove(f'temp/{file_id}_logo.jpg')


def remove_zip(file_id):
    """
    Удаляет все файла/папки после работы с zip архивом
    :param file_id:
    :return:
    """
    if os.path.isdir(f'./temp/{file_id}'):
        shutil.rmtree(f'./temp/{file_id}')
    if os.path.isdir(f'./temp/{file_id}_logo'):
        shutil.rmtree(f'./temp/{file_id}_logo')
    if os.path.isfile(f'./temp/{file_id}.zip'):
        os.remove(f'./temp/{file_id}.zip')
    if os.path.isfile(f'./temp/{file_id}_logo.zip'):
        os.remove(f'./temp/{file_id}_logo.zip')


async def download_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % скачивания файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    await status.edit_text(f'Скачал {int((current / total) * 100)}%')


async def upload_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % загрузки файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    await status.edit_text(f'Загрузил {int((current / total) * 100)}%')


def get_size_size(file_path: str) -> list or Exception:
    """
    Получает разрешение файла
    :param file_path: Путь к файлу
    :return: Количество пикселей по высоте, количество пикселей по ширине
    """
    parser = createParser(file_path)
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            return err
    return [metadata.getValues('width')[0], metadata.getValues('height')[0]]


async def logo_on_photo(file, size, color, lang):
    """
    Функция добавления логотипа размера: size, цвета: color, языка: lang на фото
    :param file: Ид фотографии
    :param size: Размер логотипа
    :param color: Цвет логотипа
    :param lang: Язык логотипа
    :return:
    """
    img_size = get_size_size(f'temp/{file}')
    logo_size = get_size_size(f'logo/{color}_{lang}.png')
    sp.call([
        # Добавляем наше фото и логотип выбранный пользователем
        'ffmpeg', '-i', f'temp/{file}', '-i', f'logo/{color}_{lang}.png',
        # Логотип полупрозрачный на 75% 
        '-filter_complex', '[1]format=yuva444p,colorchannelmixer=aa=0.75,'
        # Меняем размер логотипа
        f'scale={int(img_size[0] * 0.1 * size)}:-1[in2];'
        # Позиционируем логотип
        f'[0][in2]overlay='
        # рассчитываем отступы относительно разрешения фото и логотипа
        f'{int(img_size[0] - img_size[0] * 0.1 * size - img_size[0] * 0.005)}:'
        f'{int(img_size[1] - int(logo_size[1] * (img_size[0] * 0.1 * size) / logo_size[0]) - img_size[0] * 0.005)}',
        # Указываем выходной файл
        '-q:v', '1',  f'temp/{file.split(".")[0]}_logo.jpg'])


async def logo_on_video(file, size, color, lang):
    """
    Функция добавления логотипа размера: size, цвета: color, языка: lang на видео
    :param file: Ид видео
    :param size: Размер логотипа
    :param color: Цвет логотипа
    :param lang: Язык логотипа
    :return:
    """
    video_size = get_size_size(f'temp/{file}')
    sp.call(['ffmpeg',
             # Добавляем наше фото и логотип выбранный пользователем
             '-i', f'temp/{file}', '-i', f'logo/{color}_{lang}.png', '-filter_complex',
             # Логотип полупрозрачный на 75%
             '[1]format=yuva444p,colorchannelmixer=aa=0.75,'
             # Меняем размер логотипа
             f'scale={video_size[0] * 0.1 * size}:-1[in2];[0][in2]overlay='
             f'{video_size[0] * 0.005}:{video_size[0] * 0.005}',
             # Указываем выходной файл
             f'temp/{file.split(".")[0]}_logo.mp4'])
