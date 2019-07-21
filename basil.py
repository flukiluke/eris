import subprocess

import time
import tempfile

last_watered = 0
COOLDOWN = 60
WATER_MAX_SECS = 60

HELPTEXT = {}

def basilcmd(cmds):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', *cmds], stderr=subprocess.STDOUT)
    return output

HELPTEXT['moisture'] = 'Check the instantaneous moisture of the pot'
def moisture():
    output = basilcmd(['moisture'])
    return 'Soil moisture content: ' + output.decode().strip() + '%'

HELPTEXT['history [N]'] = 'Print [N] of the automatic hourly moisture measurements.'
def history(num=12):
    output = basilcmd(['history', num])
    return '```' + output.decode().strip() + '```'

HELPTEXT['water [time]'] = 'Dispense water for [time] seconds'
def water(runtime):
    global last_watered, COOLDOWN, WATER_MAX_SECS
    dt = time.time() - last_watered
    if runtime <= 0:
        return "Nice try, you won't fool me with that one again."
    if runtime > WATER_MAX:
        return "Please only water me between 0 and %d seconds." % WATER_MAX_SECS
    if dt < COOLDOWN:
        return "I was watered %d second(s) ago, but you may tend to me again in a mere %d second(s)" % (int(dt), int(COOLDOWN - dt))
    else:
        output = basilcmd(['water', str(runtime)])
        if output.decode().strip() == 'OK':
            last_watered = time.time()
            return str(runtime) + " seconds of S i p p"
        else:
            return "Hydration subsystem reported error: " + output.decode().strip()

HELPTEXT['graph [N]'] = 'Graph [N] of the automatic hourly moisture measurements.'
def graph(samples):
    data = basilcmd(['raw_history', str(samples)])
    image = tempfile.NamedTemporaryFile(delete=False)
    subprocess.run(['gnuplot', 'basil_history.gnuplot'], stdout=image, input=data)
    image.close()
    return image.name


HELPTEXT['help [command]'] = 'Get detailed help for [command]'
def help(cmd):
    str = ''
    try:
        str += '!basil %s: %s\n' % (cmd, HELPTEXT[cmd])
    except KeyError:
        str += 'Basil commands:\n'
        for text in HELPTEXT:
            str += '!basil %s\n' % text
    return str
