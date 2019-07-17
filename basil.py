import subprocess

import time
import tempfile

lastWatered = time.time()
COOLDOWN = 60



def basilcmd(cmds):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', *cmds], stderr=subprocess.STDOUT)
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
        return 'I was watered %d seconds ago, but you may tend to me again in a mere %d seconds' % (int(dt), int(COOLDOWN - dt))
    else:
        output = basilcmd(['water', str(runtime)])
        if output.decode().strip() == 'OK':
            return str(runtime) + " seconds of S i p p"
        else:
            return "Hydration subsystem reported error: " + output.decode().strip()

def ghistory(samples):
    data = basilcmd(['raw_history', str(samples)])
    image = tempfile.NamedTemporaryFile(delete=False)
    subprocess.run(['gnuplot', 'basil_history.gnuplot'], stdout=image, input=data)
    image.close()
    return image.name

def play(song):
    return 'Now Playing: Despacito ft. Daddy Yankee'
