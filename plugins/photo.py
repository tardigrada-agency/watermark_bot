from pyrogram import Client, filters
from PIL import Image
import utils
import db
import os


@Client.on_message(filters.document & utils.check_user)
@Client.on_message(filters.photo & utils.check_user)
async def photo(client, message):
    """
     Добавляет ватермарку на фото
    :param client:
    :param message:
    :return:
    """
    file = None
    file_unique_id = None
    try:
        user = db.get_user(message.from_user.id)
        if message.document:
            if "image" not in message.document.mime_type:
                await message.reply_text("Видео как файл пока нельзя :(")  # todo
                return
            file = message.document
            file_unique_id = message.document.file_unique_id
        if message.photo:
            file = message.photo
            file_unique_id = message.photo.file_unique_id

        await utils.remove_photo(file_unique_id)  # Удаляем фото с такимже file_unique_id если оно уже почему-то есть

        # Скачиваем фото из телеграмма
        status = await message.reply_text("Скачал 0%")
        await client.download_media(message=file, file_name=f"temp/{file_unique_id}.jpg",
                                    progress=utils.download_callback, progress_args=(status,))

        # Обработка фотографии
        await status.edit_text("Обработка...")
        img_size = Image.open(f"temp/{file_unique_id}.jpg").size
        logo_size = Image.open(f"logo/{user.size}_{user.color}_{user.lang}.png").size
        os.system(
            f'ffmpeg -i temp/{file_unique_id}.jpg -i logo/{user.size}_{user.color}_{user.lang}.png '
            f'-filter_complex "[1]format=yuva444p,colorchannelmixer=aa=0.75[in2];[0][in2]overlay={img_size[0] - logo_size[0] - 10 * user.size}:{img_size[1] - logo_size[1]}" '
            f'-q:v 1  temp/{file_unique_id}_logo.jpg')

        # Отправляем фоток в телеграмм
        await client.send_chat_action(message.chat.id, action="upload_document")
        await client.send_document(chat_id=message.from_user.id,
                                   document=f"temp/{file_unique_id}_logo.jpg",
                                   progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    await utils.remove_photo(file_unique_id)  # Удаляем фото, оно нам больше не нужно
