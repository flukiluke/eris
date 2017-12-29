import asyncio
import discord
import datetime
from ftplib import FTP
from lxml import etree
import json

@asyncio.coroutine
def store_weather_task(client, config):
    yield from client.wait_until_ready()
    while not client.is_closed:
        now = datetime.datetime.now()
        endtime = datetime.datetime(now.year, now.month, now.day,23,55)
        if now.time() > datetime.time(23,55):
            endtime += datetime.timedelta(1)
        yield from asyncio.sleep((endtime - now).total_seconds())
        yield store_weather()

def store_weather():
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    ftp.retrbinary('RETR IDV10753.xml', open('/tmp/lukebot_weather.xml', 'wb').write)
    ftp.quit()

    tree = etree.parse('/tmp/lukebot_weather.xml')
    max_temp = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/element[@type='air_temperature_maximum']/text()")[0]
    
    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/element[@type='precipitation_range']/text()")):
        precip_range = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/element[@type='precipitation_range']/text()")[0]
    else:
        precip_range = '[Data not available]'

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/text[@type='probability_of_precipitation']/text()")):
        precip_chance = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/text[@type='probability_of_precipitation']/text()")[0]
    else:
       precip_chance = '[Data not available]'

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/text[@type='precis']/text()")):
        precis = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='1']/text[@type='precis']/text()")[0]
    else:
        precis = '[Data not available]'

    weather_data = {'max_temp' : max_temp, 'precip_range' : precip_range, 'precip_chance' : precip_chance, 'precis' : precis}

    with open('/tmp/weather_data.txt', 'w') as data:
        data.truncate(0)
        json.dump(weather_data, data)

def get_stored_weather():
    weather = get_weather()

    with open('/tmp/weather_data.txt', 'r') as data:
        weather_data = json.load(data) 
    
    for data in weather.values():
        if data == '[Data not available]':
            return 'Weather: ' + weather_data['precis'] + ' Top of ' + weather_data['max_temp'] + '°C, ' + weather_data['precip_chance'] + ' chance of up to ' + weather_data['precip_range'] + ' precipitation.'

    weather_data = weather
    
    return 'Weather: ' + weather_data['precis'] + ' Top of ' + weather_data['max_temp'] + '°C, ' + weather_data['precip_chance'] + ' chance of up to ' + weather_data['precip_range'] + ' precipitation.'


def task(client, config):
    yield from client.wait_until_ready()
    while not client.is_closed:
        now = datetime.datetime.now()
        endtime = datetime.datetime(now.year, now.month, now.day,5,30)
        if now.time() > datetime.time(5,30):
            endtime += datetime.timedelta(1)
        yield from asyncio.sleep((endtime - now).total_seconds())
        yield from client.send_message(discord.Object(id = config['main_channel']), get_stored_weather())

def get_weather():
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    ftp.retrbinary('RETR IDV10753.xml', open('/tmp/lukebot_weather.xml', 'wb').write)
    ftp.quit()

    tree = etree.parse('/tmp/lukebot_weather.xml')
    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='air_temperature_maximum']/text()")):
        max_temp = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='air_temperature_maximum']/text()")[0]
    else:
        max_temp = '[Data not available]'
    
    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='precipitation_range']/text()")):
        precip_range = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='precipitation_range']/text()")[0]
    else:
        precip_range = '[Data not available]'

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='probability_of_precipitation']/text()")):
        precip_chance = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='probability_of_precipitation']/text()")[0]
    else:
       precip_chance = '[Data not available]'

    if(tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='precis']/text()")):
        precis = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='precis']/text()")[0]
    else:
        precis = '[Data not available]'

    return {'max_temp' : max_temp, 'precip_range' : precip_range, 'precip_chance' : precip_chance, 'precis' : precis}
