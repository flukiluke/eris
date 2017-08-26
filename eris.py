#!/usr/bin/env python3
import discord
import asyncio
import logging
import shlex
import configure
import bot

CONFIG_FILE = 'eris.json'

logging.basicConfig(level = logging.INFO)
config = configure.load(CONFIG_FILE)
client = discord.Client()
bot = bot.Bot(client, config)

def custom_lex(string):
    return string.split(' ', 1)

@client.async_event
def on_message(message):
    if not interesting_message(message):
        return
    if message.content.startswith(config['cmd_prefix']):
        try:
            tokens = shlex.split(message.content[1:])
        except:
            tokens = custom_lex(message.content[1:])
        yield from bot.do_command(message, *tokens)
    yield from bot.parse_chatter(message)

def interesting_message(message):
    if config['channels'] and message.channel.name not in config['channels']:
        return False
    if message.author == client.user:
        return False
    return True

client.loop.create_task(bot.fortune_task())
client.loop.create_task(bot.weather_task())
client.loop.create_task(bot.alert_task())
client.run(config['token'])
