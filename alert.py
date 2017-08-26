import asyncio
import datetime
import discord

alerts = []

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    now = datetime.datetime.now() + datetime.timedelta(hours=10)
    for alert in alerts:
        if alert[1] > now:
            yield from asyncio.sleep((alert[1] - now).total_seconds()) 
            yield from client.send_message(discord.Object(id = config['main_channel']), alert[0])
    


