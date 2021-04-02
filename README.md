# Watermark

## Установка

### FFmpeg

Для обработки изображений и видео бот использует программу ffmpeg. 

Если он не доступен через `$ ffmpeg` - бот не будет работать и его нужно поставить.

Ниже команды установки для разных дистрибутивов linux:

Ubuntu - `sudo apt-get install ffmpeg`

Arch/Manjaro - `sudo pacman -S ffmpeg`



### Python 3

Бот проверен с python версии 3.9.1, более старые/новые скорей всего будут работать, но это не проверено.



### Установка библиотек

В директории бота запустите `python3 -m pip install -r requirements.txt`



### Конфигурация

Создайте файл `configuration.ini` с текстом:

```
[pyrogram]
api_id = api_id_телеграмма
api_hash = api_hash_телеграмма
session_name = Названия_для_файла_сессиии

[mongodb]
name = Имя_базы
host = mongodb+srv://ссылка_для_доступа_к_базе
```



