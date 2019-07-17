import subprocess
import time
import csv

lastWatered = time.time()

COOLDOWN = 60

def basilcmd(*cmds):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', cmd], stderr=subprocess.STDOUT)
    return output

def moisture():
    output = basilcmd(['moisture'])
    return 'Soil moisture content: ' + output.decode().strip() + '%'

def history(num=12):
    output = basilcmd(['history', num])
    return '```' + output.decode().strip() + '```'

def water(runtime):
    dt = time.time() - lastWatered
    if runtime <= 0:
        return "Nice try, you won't fool me with that one again."
    if runtime > 60:
        return 'Please only water me between 0 and 60 seconds.'
    if dt < COOLDOWN:
        return 'I was watered %d seconds ago, please wait another %d seconds before attempting to water me again' % (int(dt), int(COOLDOWN - dt))
    else:
        output = basilcmd(['water', runtime])
    return output.decode().strip() + 'S i p p'

def play(song):
    return 'Now Playing: Despacito ft. Daddy Yankee'

def graph(num=12):
    output = basilcmd(['dump', num])
    r = csv.reader(output.decode().split('\n'),delimiter=',')
