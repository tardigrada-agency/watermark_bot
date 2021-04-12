from pyrogram import Client
import logging
import config

# Reading config
api_hash = config.bot_config['pyrogram']['api_hash']
api_id = config.bot_config['pyrogram']['api_id']
session_name = config.bot_config['pyrogram']['session_name']

# Starting bot
plugins = dict(root='plugins')
with Client(f'data/{session_name}', api_hash=api_hash, api_id=api_id) as app:
    logging.info(f'@{app.get_me()["username"]} session created')
