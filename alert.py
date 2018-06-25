import asyncio
from datetime import datetime
import discord

alerts = [("@everyone REMINDER: 3rd year registration opens next week.", datetime(2018, 6, 26, 10, 0)),
          ("@everyone REMINDER: 2nd year registration opens next week.", datetime(2018, 6, 28, 10, 0)),
          ("@everyone REMINDER: 3rd year registration opens in an hour.", datetime(2018, 7, 3, 9, 0)),
          ("@everyone REMINDER: 2nd year registration opens in an hour.", datetime(2018, 7, 5, 9, 0)),
          ]

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    alerts.sort(key=lambda x: x[1])
    now = datetime.now()
    for alert in alerts:
        if alert[1] > now:
            yield from asyncio.sleep((alert[1] - datetime.now()).total_seconds()) 
            yield from client.send_message(discord.Object(id = config['main_channel']), alert[0])
