#!/usr/bin/env python3
import discord
import asyncio
import logging
import shlex
import config
import bot

CONFIG_FILE = 'eris.json'

logging.basicConfig(level = logging.INFO)
config = config.load(CONFIG_FILE)
client = discord.Client()
bot = bot.Bot(client, config)

@client.async_event
def on_ready():
    print('Logged in as ' + client.user.name)

@client.async_event
def on_message(message):
    if not interesting_message(message):
        return
    if message.content.startswith(config['cmd_prefix']):
        tokens = shlex.split(message.content[1:])
        yield from bot.do_command(message, *tokens)
    yield from bot.parse_chatter(message)

def interesting_message(message):
    if config['channels'] and message.channel.name not in config['channels']: 
        return False
    if message.author == client.user:
        return False
    return True


client.run(config['token'])
