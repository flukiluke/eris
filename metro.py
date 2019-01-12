import urllib.request, json
import xml.etree.ElementTree
import asyncio
import discord
from bs4 import BeautifulSoup, Tag

@asyncio.coroutine
def send_alert(alert, client, channel):
    message = remove_tags(alert)
    yield from client.send_message(channel, message)

def remove_tags(text):
    soup = BeautifulSoup(text, features="lxml")

    for tag in soup.find_all('div'):
        tag.decompose()

    return soup.get_text()

def get_name(line_name, data):
    for line in data['lines']:
        if(line['line_name'].lower() == line_name.lower()):
            return line['line_id']
    return None

@asyncio.coroutine
def get_disruptions(line_name, client, channel):
    with urllib.request.urlopen("http://www.metrotrains.com.au/api?op=get_notify_data") as url:
        data = json.loads(url.read().decode())

    line = get_name(line_name, data)

    if(line is None):
        yield from send_alert("Line not found", client, channel)
    elif line in data['line_status']:
        if(isinstance(data['line_status'][line]['alerts'], list)):
            for alert in data['line_status'][line]['alerts']:
                yield from send_alert(alert['alert_text'], client, channel)
        elif(data['line_status'][line]['alerts']):
            yield from send_alert(data['line_status'][line]['alerts'], client, channel)
        else:
            yield from send_alert('No alerts for this line', client, channel)
    else:
        yield from send_alert('Good service - trains are running on time to five minutes', client, channel)
