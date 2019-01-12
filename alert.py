import discord
import asyncio
from dateparser import parse
from datetime import datetime
import db

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    now = datetime.now().timestamp()
    c = db.cursor()
    c.execute("SELECT target, time, message FROM alerts WHERE time > " + datetime.now().timestamp())
    for alert in c.fetchall():
        yield from asyncio.sleep(alert[1] - datetime.now().timestamp())
        yield from client.send_message(discord.Object(id = config['main_channel']), alert[0] + ' ' + alert[2])

@asyncio.coroutine
def queue(target, time, message):
    when = parse(time, locales=['en-AU'])
    db.insert('alerts', {'target': target, 'time': when.timestamp(), 'message': message})
    delay = (when - datetime.now()).total_seconds()
    yield from asyncio.sleep(delay)




