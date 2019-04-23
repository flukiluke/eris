import subprocess

def basilcmd(cmd):
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/cli.py', cmd], stderr=subprocess.STDOUT)
    return output

def moisture():
    output = basilcmd('moisture')
    return 'Soil moisture content: ' + output.decode().strip() + '%'

def history():
    output = basilcmd('history')
    return '```' + output.decode().strip() + '```'



