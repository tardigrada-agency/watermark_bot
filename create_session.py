from pyrogram import Client
import logging
import config

# Reading config
api_hash = config.config['pyrogram']['api_hash']
api_id = config.config['pyrogram']['api_id']
session_name = config.config['pyrogram']['session_name']

# Starting bot
plugins = dict(root='plugins')
with Client(f'sessions/{session_name}', api_hash=api_hash, api_id=api_id) as app:
    logging.info(f'@{app.get_me()["username"]} session created')
