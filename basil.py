import subprocess

def basilcmd(*cmds):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', cmd], stderr=subprocess.STDOUT)
    return output

def moisture():
    output = basilcmd(['moisture'])
    return 'Soil moisture content: ' + output.decode().strip() + '%'

def history():
    output = basilcmd(['history'])
    return '```' + output.decode().strip() + '```'

def water(runtime):
    if runtime <= 0 or runtime > 60:
        return 'Please only water between 0 and 60 seconds'
    basilcmd(['water', runtime])
    return 'Hydration deployed'

