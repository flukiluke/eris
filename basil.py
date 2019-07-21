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

HELPTEXT['moisture'] = {'args': [], 'text':'Check the instantaneous moisture of the pot'}
def moisture():
    output = basilcmd(['moisture'])
    return 'Soil moisture content: ' + output.decode().strip() + '%'

HELPTEXT['water'] = {'args': ['time'], 'text': 'Dispense water for [time] seconds'}
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

HELPTEXT['graph'] = {'args': ['N'], 'text': 'Graph [N] of the automatic hourly moisture measurements.'}
def graph(samples):
    data = basilcmd(['raw_history', str(samples)])
    image = tempfile.NamedTemporaryFile(delete=False)
    subprocess.run(['gnuplot', 'basil_history.gnuplot'], stdout=image, input=data)
    image.close()
    return image.name

HELPTEXT['history'] = {'args': ['N'], 'text': 'Print [N] of the automatic hourly moisture measurements.'}
def history(samples):
    output = basilcmd(['history', samples])
    return '```' + output.decode().strip() + '```'

HELPTEXT['help'] = {'args': ['command'], 'text': 'Get detailed help for [command]'}
def help(cmd):
    str = ''

    if cmd in HELPTEXT:
        str += '!basil %s' % cmd
        for a in HELPTEXT[cmd]['args']:
            str += ' [%s]' % a
        str += ': %s\n' % HELPTEXT[cmd]['text']
    else:
        str += 'Basil commands:\n\n'
        for text in HELPTEXT:
            str += '!basil %s' % text
            for a in HELPTEXT[text]['args']:
                str += ' [%s]' % a
            str += '\n'
    return str
