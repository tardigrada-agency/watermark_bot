from pyrogram import Client, filters
import utils
import db
import os


@Client.on_message(filters.document & utils.check_user)
@Client.on_message(filters.photo & utils.check_user)
async def photo(client, message):
    """
     Добавляет ватермарку на фото
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    file = None
    file_unique_id = None
    try:
        user = db.get_user(message.from_user.id)
        if message.document:
            if 'image' not in message.document.mime_type:
                await message.reply_text('Видео как файл пока нельзя :(')  # todo
                return
            file = message.document
            file_unique_id = message.document.file_unique_id
        if message.photo:
            file = message.photo
            file_unique_id = message.photo.file_unique_id

        await utils.remove_photo(file_unique_id)  # Удаляем фото с такимже file_unique_id если оно уже почему-то есть

        # Скачиваем фото из телеграмма
        status = await message.reply_text('Скачал 0%')
        await client.download_media(message=file, file_name=f'temp/{file_unique_id}.jpg',
                                    progress=utils.download_callback, progress_args=(status,))

        # Обработка фотографии
        await status.edit_text('Обработка...')
        img_size = utils.get_size_size(f'temp/{file_unique_id}.jpg')
        logo_size = utils.get_size_size(f'logo/{user.color}_{user.lang}.png')
        os.system(
            # Добавляем наше фото и логотип выбранный пользователем
            f'ffmpeg -i temp/{file_unique_id}.jpg -i logo/{user.color}_{user.lang}.png '
            # Логотип полупрозрачный на 75% 
            f'-filter_complex "[1]format=yuva444p,colorchannelmixer=aa=0.75,'
            # Меняем размер логотипа
            f'scale={img_size[0]*0.1*user.size}:-1[in2];'
            # Позиционируем логотип
            f'[0][in2]overlay='
            # рассчитываем отступы относительно разрешения фото и логотипа
            f'{img_size[0] - img_size[0]*0.1*user.size - img_size[0]*0.005}:{img_size[1] - int(logo_size[1]*(img_size[0]*0.1*user.size)/logo_size[0]) - img_size[0]*0.005}" '
            # Указываем выходной файл
            f'-q:v 1  temp/{file_unique_id}_logo.jpg')

        # Отправляем фото в телеграмм
        await client.send_chat_action(message.chat.id, action='upload_document')
        await client.send_document(chat_id=message.from_user.id,
                                   document=f'temp/{file_unique_id}_logo.jpg',
                                   progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    await utils.remove_photo(file_unique_id)  # Удаляем фото, оно нам больше не нужно
