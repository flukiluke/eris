import discord
import re
import subprocess
import logging

def parse(message, quotes_file):
    content = message.content

    match = re.search('.+([A-Za-z0-9]:|\]:)+.+(\n[A-Za-z0-9].*)*', content)

    if(match is not None):
        if(match.group(0) == content):
            with open(quotes_file, 'a') as data:
                data.write('%\n' + content + '\n')
            process = subprocess.Popen(['strfile', quotes_file], stdout=subprocess.PIPE)
            output, error = process.communicate()
            logging.info(output.decode())
