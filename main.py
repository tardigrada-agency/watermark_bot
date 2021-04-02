from pyrogram import Client
import config
import db

# Если в базе нет админа - добавим его
admin_id = config.get('pyrogram')['admin_id']
if not db.check_user(admin_id):
    db.add_user(admin_id)

# Запускаем бота
plugins = dict(root='plugins')
app = Client(f"sessions/{config.get('pyrogram')['session_name']}", config_file='./configuration.ini', plugins=plugins)
app.run()
