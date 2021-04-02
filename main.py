from pyrogram import Client
import config

plugins = dict(root="plugins")
app = Client(config.get('pyrogram')['session_name'], config_file="./configuration.ini", plugins=plugins)
app.run()
