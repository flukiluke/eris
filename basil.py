import subprocess

def moisture():
    output = subprocess.check_output(['ssh', 'rrpi', './basilbot/basilcli.py', 'moisture'], stderr=subprocess.STDOUT)
    return output.decode().strip() + '%'


