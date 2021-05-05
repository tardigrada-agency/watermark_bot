from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import filters
import subprocess as sp
import modes
import shutil
import os
import db

# Custom filters
check_user = filters.create(lambda _, __, message: db.check_user(message.from_user.id))
new_language = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_language')
new_size = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_size')
new_mode = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_mode')
new_color = filters.create(lambda _, __, data: data.data.split("=")[0] == 'new_color')
document_video = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'video' if message.document else False)
document_image = filters.create(
    lambda _, __, message: message.document.mime_type.split("/")[0] == 'image' if message.document else False)
document_zip = filters.create(
    lambda _, __, message: message.document.mime_type == 'application/zip' if message.document else False)


def get_filename(path: str) -> str:
    base = os.path.basename(path)
    return os.path.splitext(base)[0]


def remove_file(path: str):
    if os.path.isfile(path):
        os.remove(path)


def remove_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)


def remove_video(file_id):
    """
    Удаляем видео для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    remove_file(f'temp/{file_id}.mp4')
    remove_file(f'temp/{file_id}_logo.mp4')


def remove_photo(file_id):
    """
    Удаляем фото для file_id
    :param file_id: Ид файлы который должен быть удален
    :return:
    """
    remove_file(f'temp/{file_id}.jpg')
    remove_file(f'temp/{file_id}_logo.jpg')


def remove_zip(file_id):
    """
    Удаляет все файла/папки после работы с zip архивом
    :param file_id:
    :return:
    """
    remove_dir(f'./temp/{file_id}')
    remove_dir(f'./temp/{file_id}_logo')
    remove_file(f'./temp/{file_id}.zip')
    remove_file(f'./temp/{file_id}_logo.zip')


async def download_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % скачивания файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    try:
        await status.edit_text(f'Скачал {int((current / total) * 100)}%')
    except Exception as e:
        print(e)


async def upload_callback(current, total, status):
    """
    Callback чтобы показывать юзеру % загрузки файла на сервер
    :param current:
    :param total:
    :param status:
    :return:
    """
    try:
        await status.edit_text(f'Загрузил {int((current / total) * 100)}%')
    except Exception as e:
        print(e)


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


async def draw_logo_on_photo(file, size, color, lang, mode):
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
    mode = modes.modes[mode]
    sp.call([
        # Добавляем наше фото и логотип выбранный пользователем
        'ffmpeg', '-i', f'temp/{file}', '-i', f'logo/{color}_{lang}.png',
        # Логотип полупрозрачный на 75% 
        # Логотип полупрозрачный на 75%
        '-filter_complex', f'[1]format=yuva444p,curves=lighter,colorchannelmixer=aa={mode["opacity"](logo_size, img_size, size)},'
        # Меняем размер логотипа
        f'scale={mode["scale"](logo_size, img_size, size)}:-1[in2];'
        # Позиционируем логотип
        f'[0][in2]overlay='
        # рассчитываем отступы относительно разрешения фото и логотипа
        f'{mode["x"](logo_size, img_size, size)}:'
        f'{mode["y"](logo_size, img_size, size)}',
        # Указываем выходной файл
        '-q:v', '1',  f'temp/{get_filename(file)}_logo.jpg'])


async def draw_logo_on_video(file, size, color, lang, mode):
    """
    Функция добавления логотипа размера: size, цвета: color, языка: lang на видео
    :param file: Ид видео
    :param size: Размер логотипа
    :param color: Цвет логотипа
    :param lang: Язык логотипа
    :return:
    """
    img_size = get_size_size(f'temp/{file}')
    logo_size = get_size_size(f'logo/{color}_{lang}.png')
    mode = modes.modes[mode]
    sp.call([
        # Добавляем наше фото и логотип выбранный пользователем
        'ffmpeg', '-i', f'temp/{file}', '-i', f'logo/{color}_{lang}.png',
        # Логотип полупрозрачный на 75%
        # Логотип полупрозрачный на 75%
        '-filter_complex', f'[1]format=yuva444p,colorchannelmixer=aa={mode["opacity"](logo_size, img_size, size)},'
        # Меняем размер логотипа
                           f'scale={mode["scale"](logo_size, img_size, size)}:-1[in2];'
        # Позиционируем логотип
                           f'[0][in2]overlay='
        # рассчитываем отступы относительно разрешения фото и логотипа
                           f'{mode["x"](logo_size, img_size, size)}:'
                           f'{mode["y"](logo_size, img_size, size)}',
        # Указываем выходной файл
        '-q:v', '1', f'temp/{get_filename(file)}_logo.mp4'])