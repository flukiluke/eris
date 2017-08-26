import json
import logging
from discord import utils

def load(filename):
    try:
        fp = open(filename, mode = 'r')
        config = json.load(fp)
    except OSError as e:
        logging.getLogger('config').error('Config file ' + filename + ' not found.')
        exit(1)
    else:
        fp.close()
        return config
