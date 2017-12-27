import asyncio
import datetime
import discord

alerts = [("@everyone REMINDER: 2nd year enrolment opens in 1 hour.", datetime.datetime(2017, 7, 4, 9, 00))]

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    now = datetime.datetime.now() + datetime.timedelta(hours=10)
    for alert in alerts:
        if alert[1] > now:
            yield from asyncio.sleep((alert[1] - now).total_seconds()) 
            yield from client.send_message(discord.Object(id = config['main_channel']), alert[0])
    


