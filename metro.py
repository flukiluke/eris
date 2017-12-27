import urllib.request, json
import xml.etree.ElementTree
import asyncio
import discord
from bs4 import BeautifulSoup, Tag

def remove_tags(text):
    soup = BeautifulSoup(text, "html")

    for tag in soup.find_all('div'):
        tag.decompose()

    return soup.get_text()

def get_name(line_name):
    lines = {'alamein': 82, 'belgrave': 84, 'craigieburn': 85, 'cranbourne': 86, 'south morang': 87,
             'frankston': 88, 'glen waverley': 89, 'hurstbridge': 90, 'lilydale': 91, 'pakenham': 92,
             'sandringham': 93, 'stony point': 94, 'sunbury': 95, 'upfield': 96, 'werribee': 97, 
             'williamstown': 98, 'mernda': '82'}
    name = line_name.lower()
    if name not in lines:
        return 'Line not found'
    return str(lines[name])

@asyncio.coroutine
def get_disruptions(line_name, client, config):
    line  = get_name(line_name)

    with urllib.request.urlopen("http://www.metrotrains.com.au/api?op=get_notify_data") as url:
        data = json.loads(url.read().decode())
    
    if(line == 'Line not found'):
        yield from client.send_message(discord.Object(id = config['main_channel']), "Line not found")
    elif line in data['line_status']:
        if(isinstance(data['line_status'][line]['alerts'], list)):
            for alert in data['line_status'][line]['alerts']:
                yield from client.send_message(discord.Object(id = config['main_channel']), remove_tags(alert['alert_text'])) 
        elif(data['line_status'][line]['alerts']):
            yield from client.send_message(discord.Object(id = config['main_channel']), remove_tags(data['line_status'][line]['alerts']))
        else:
            yield from client.send_message(discord.Object(id = config['main_channel']), 'No alerts for this line')
    else:
        yield from client.send_message(discord.Object(id = config['main_channel']), 'Line not found in MetroNotify API')
