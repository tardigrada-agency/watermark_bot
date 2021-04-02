# Watermark

## Запуск в docker

### Подготовка

`$ mkdir sessions`

`$ mkdir temp`

`$ wget https://raw.githubusercontent.com/tardigrada-agency/watermark/main/docker-compose.yaml`

`$ wget https://raw.githubusercontent.com/tardigrada-agency/watermark/main/configuration.ini `

Перейдите по ссылке https://my.telegram.org/auth?to=apps и создайте приложение, вставте api_id и api_hash в `configuration.ini`.

Замените `watermark_bot`  на имя вашего бота,

Замените `123456789` на ваш ид в телеграмме,

Замените данных для подключения к базе mongodb, если у вас нет сервера с базой можно использовать https://www.mongodb.com/cloud/atlas

Создайте сессию [pyrogram](https://docs.pyrogram.org/intro/quickstart) и поместите ее в папку sessions

### Запуск

`$ docker-compose up -d`

### Обновление

 `$ docker-compose pull`

### Выключение

`$ docker-compose stop`



## Установка

### FFmpeg

Для обработки изображений и видео бот использует программу ffmpeg. 

Если он не доступен через `$ ffmpeg` - бот не будет работать и его нужно поставить.

Ниже команды установки для разных дистрибутивов linux:

Ubuntu - `sudo apt-get install ffmpeg`

Arch/Manjaro - `sudo pacman -S ffmpeg`



### Python 3

### Установка библиотек

В директории бота запустите `python3 -m pip install -r requirements.txt`



### Настройка
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

Создайте сессию [pyrogram](https://docs.pyrogram.org/intro/quickstart) и поместите ее в папку sessions

## Запуск

`$ python3 main.py`

