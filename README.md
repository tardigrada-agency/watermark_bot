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
Перейдите по ссылке https://my.telegram.org/auth?to=apps и создайте приложение.

Создайте файл `configuration.ini` с текстом:

```
[pyrogram]
api_id = ID_ПРИЛОЖЕНИЯ
api_hash = HASH_ПРИЛОЖЕНИЯ
session_name = НАЗВАНИЯ_ДЛЯ_ФАЙЛА_СЕССИИ
admin_id = ИД_ЮЗЕРА_ТЕЛЕГРАММ

[mongodb]
name = ИМЯ_БАЗЫ
host = ССЫЛКА_ДЛЯ_ДОСТУПА_К_БАЗЕ
```



