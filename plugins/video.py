from pyrogram import Client, filters
import utils
import db
import os


@Client.on_message(filters.video & utils.check_user)
async def video(client, message):
    """
     Добавляет ватермарку на видео
    :param client: Клиент для работы с телеграмом
    :param message: Сообщение пользователя которое запустило эту функцию
    :return:
    """
    await utils.remove_video(message.video.file_unique_id)  # Удаляем видео с таким ид если оно уже почему-то есть
    try:
        user = db.get_user(message.from_user.id)    # Получаем юзера из базы

        # Скачиваем видео из телеграмма
        status = await message.reply_text('Скачал 0%')
        await client.download_media(message=message.video, file_name=f'temp/{message.video.file_unique_id}.mp4',
                                    progress=utils.download_callback, progress_args=(status,))

        # Запукаем ffmpeg для нашего видео
        await status.edit_text('Обработка...')
        os.system(
            # Добавляем наше фото и логотип выбранный пользователем
            f'ffmpeg -i temp/{message.video.file_unique_id}.mp4 -i logo/{user.size}_{user.color}_{user.lang}.png '
            # Логотип полупрозрачный на 75% 
            f'-filter_complex "[1]format=yuva444p,colorchannelmixer=aa=0.75[in2];[0][in2]overlay=10:10" '
            # Указываем выходной файл
            f'temp/{message.video.file_unique_id}_logo.mp4')

        # Загружаем видео обратно в телеграмм
        await client.send_chat_action(message.chat.id, action='upload_video')
        await client.send_video(chat_id=message.from_user.id,
                                video=f'temp/{message.video.file_unique_id}_logo.mp4',
                                progress=utils.upload_callback, progress_args=(status,))
        await status.delete()
    except Exception as e:
        await message.reply_text(f'ERROR: {str(e)}')
    await utils.remove_video(message.video.file_unique_id)   # Удаляем видео, оно нам больше не нужно
