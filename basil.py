import subprocess
import tempfile

def basilcmd(cmds):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', *cmds], stderr=subprocess.STDOUT)
    return output

def moisture():
    output = basilcmd(['moisture'])
    return 'Soil moisture content: ' + output.decode().strip() + '%'

def history():
    output = basilcmd(['history'])
    return '```' + output.decode().strip() + '```'

def water(runtime):
    if runtime <= 0:
        return "Nice try, you won't fool me with that one again."
    if runtime > 60:
        return 'Please only water me between 0 and 60 seconds.'
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



