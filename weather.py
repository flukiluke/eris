import asyncio
import discord
import datetime
from ftplib import FTP
from lxml import etree

@asyncio.coroutine
def task(client, config):
    yield from client.wait_until_ready()
    while not client.is_closed:
        now = datetime.datetime.now()
        endtime = datetime.datetime(now.year, now.month, now.day, 19, 30)
        if now.time() > datetime.time(19, 30):
            endtime += datetime.timedelta(1)
        yield from asyncio.sleep((endtime - now).total_seconds())
        yield from client.send_message(discord.Object(id = config['main_channel']), get_weather())

def get_weather():
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    ftp.retrbinary('RETR IDV10753.xml', open('/tmp/lukebot_weather.xml', 'wb').write)
    ftp.quit()

    tree = etree.parse('/tmp/lukebot_weather.xml')
    max_temp = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='air_temperature_maximum']/text()")[0]
    precip_range = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/element[@type='precipitation_range']/text()")[0]
    precip_chance = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='probability_of_precipitation']/text()")[0]
    precis = tree.xpath("//area[@aac='VIC_PT042']/forecast-period[@index='0']/text[@type='precis']/text()")[0]

    return 'Weather: ' + precis + ' Top of ' + max_temp + '°C, ' + precip_chance + ' chance of up to ' + precip_range + ' precipitation.'
    
    
    
