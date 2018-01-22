import asyncio
import datetime
import discord

alerts = [("@everyone REMINDER: 3rd year enrolment opens next week.", datetime.datetime(2018, 1, 23, 10, 0)),
          ("@everyone REMINDER: 2nd year enrolment opens next week.", datetime.datetime(2018, 1, 25, 10, 0)),
          ("@everyone REMINDER: 1st year enrolment opens next week.", datetime.datetime(2018, 1, 30, 10, 0)),
          ("@everyone REMINDER: 3rd year enrolment opens in an hour.", datetime.datetime(2018, 1, 30, 9, 0)),
          ("@everyone REMINDER: 2nd year enrolment opens in an hour.", datetime.datetime(2018, 2, 1, 9, 0)),
          ("@everyone REMINDER: 1st year enrolment opens in an hour.", datetime.datetime(2018, 2, 6, 9, 0)),
          ]

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    now = datetime.datetime.now()
    for alert in alerts:
        if alert[1] > now:
            yield from asyncio.sleep((alert[1] - datetime.datetime.now()).total_seconds()) 
            yield from client.send_message(discord.Object(id = config['main_channel']), alert[0])
