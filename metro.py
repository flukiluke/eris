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

def get_name(line_name, data):
    for line in data['lines']:
        if(line['line_name'].lower() == line_name.lower()):
            return line['line_id']
    return "Line not found"

def get_disruptions(line_name, client, config):
    with urllib.request.urlopen("http://www.metrotrains.com.au/api?op=get_notify_data") as url:
        data = json.loads(url.read().decode())

    line  = get_name(line_name, data)

    if(line == 'Line not found'):
        return "Line not found"
    elif line in data['line_status']:
        if(isinstance(data['line_status'][line]['alerts'], list)):
            for alert in data['line_status'][line]['alerts']:
                return remove_tags(alert['alert_text'])
        elif(data['line_status'][line]['alerts']):
            return remove_tags(data['line_status'][line]['alerts'])
        else:
            return 'No alerts for this line'
    else:
        return 'Good service - on time to 5 minutes'
