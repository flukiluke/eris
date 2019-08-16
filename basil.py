import subprocess
import re
import time
import tempfile

last_watered = 0
COOLDOWN = 60
WATER_MAX_SECS = 60

HELPTEXT = {}

def basilcmd(cmds):
    try:
        output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', *cmds], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        if err.returncode == 255:
            return '**Critical Basil Error**: Failed to reach reading room pi by SSH.'
        else:
            return '**Critical Basil Error**: Unknown SSH error, code %d' % err.returncode
    else:
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
        return "<:thonk:422588696701960203>"
    if runtime > WATER_MAX_SECS:
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

# Supports: 3w, 7d, 1m,
def parse_time_format(s):
    clean=s.replace(' ','')
    t=0
    tmap={'h':1, 'd':24, 'w':24*7, 'm':24*30, 'y':24*365}

    for spec in re.findall(clean,'[0-9]+([wdmy]|h?)'):
        if spec[-1].isalpha():
            t += tmap[spec[-1]]*int(spec[:-1])
        else:
            t += int(spec)
    return t



HELPTEXT['graph'] = {'args': ['N'], 'text': 'Graph [N] of the automatic hourly moisture measurements.'}
def graph(fmt):
    data = basilcmd(['raw_history', str(parse_time_format(fmt))])
    image = tempfile.NamedTemporaryFile(delete=False)
    subprocess.run(['gnuplot', 'basil_history.gnuplot'], stdout=image, input=data)
    image.close()
    return image.name

HELPTEXT['history'] = {'args': ['N'], 'text': 'Print [N] of the automatic hourly moisture measurements.'}
def history(fmt):
    output = basilcmd(['history', str(parse_time_format(fmt))])
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
