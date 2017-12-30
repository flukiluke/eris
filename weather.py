import asyncio
import discord
import datetime
import time
import os.path
from ftplib import FTP
from lxml import etree
import json

@asyncio.coroutine
def store_weather_task(client, config):
    yield from client.wait_until_ready()
    while not client.is_closed:
        now = datetime.datetime.now()
        endtime = datetime.datetime(now.year, now.month, now.day,17,30)
        if now.time() > datetime.time(17,30):
            endtime += datetime.timedelta(1)
        yield from asyncio.sleep((endtime - now).total_seconds())
        yield store_weather()

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    while not client.is_closed:
        now = datetime.datetime.now()
        endtime = datetime.datetime(now.year, now.month, now.day,5,30)
        if now.time() > datetime.time(5,30):
            endtime += datetime.timedelta(1)
        yield from asyncio.sleep((endtime - now).total_seconds())
        yield from client.send_message(discord.Object(id = config['main_channel']), fetch_weather())

def get_weather(day):
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    ftp.retrbinary('RETR IDV10753.xml', open('/tmp/lukebot_weather.xml', 'wb').write)
    ftp.quit()

    max_temp = precip_range = precip_chance = precis = None

    tree = etree.parse('/tmp/lukebot_weather.xml')
    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/element[@type='air_temperature_maximum']/text()")):
        max_temp = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/element[@type='air_temperature_maximum']/text()")[0]

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/element[@type='precipitation_range']/text()")):
        precip_range = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/element[@type='precipitation_range']/text()")[0]

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/text[@type='probability_of_precipitation']/text()")):
        precip_chance = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/text[@type='probability_of_precipitation']/text()")[0]

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/text[@type='precis']/text()")):
        precis = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='" + day + "']/text[@type='precis']/text()")[0]

    return {'max_temp' : max_temp, 'precip_range' : precip_range, 'precip_chance' : precip_chance, 'precis' : precis}

def store_weather():
    with open('/tmp/weather_data.txt', 'w') as data:
        data.truncate(0)
        json.dump(get_weather('1'), data)

def fetch_weather():
    current_weather = get_weather('0')

    if(any(not data for data in current_weather.values())):
        if(os.path.exists('/tmp/weather_data.txt')):
            with open('/tmp/weather_data.txt', 'r') as data:
                weather = json.load(data)

            return 'Weather: ' + weather['precis'] + ' Top of ' + weather['max_temp'] + '°C, ' + weather['precip_chance'] + ' chance of up to ' + weather['precip_range'] + ' precipitation. As of: ' + time.ctime(os.path.getctime('/tmp/weather_data.txt'))

        return "Weather data not available. As of: " + time.ctime(time.time())

    weather = current_weather

    return 'Weather: ' + weather['precis'] + ' Top of ' + weather['max_temp'] + '°C, ' + weather['precip_chance'] + ' chance of up to ' + weather['precip_range'] + ' precipitation. As of: ' + time.ctime(time.time())
