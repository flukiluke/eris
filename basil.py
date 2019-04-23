import subprocess
import time


class Cooldown():
    def __init__(self, t):
        # t has units of seconds
        self.lastTime = 0
        self.readyTime = time.time()
        self.cooldown = t

    def attempt(self, command, *args):
        T = time.time()
        if T > self.readyTime:
            self.lastTime = self.readyTime
            self.readyTime = T + self.cooldown
            return command(*args)
        else:
            return None

    def format(self):
        return (int(lastTime/60), int((readyTime-time.time())/60))


waterWally = Cooldown(10*60)

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
    if runtime <= 0:
        return "Nice try, you won't fool me with that one again."
    if runtime > 60:
        return 'Please only water me between 0 and 60 seconds.'
    output = waterWally.attempt(basilcmd, ['water', runtime])
    if output is None:
        return "I was watered %d minutes ago, but you may tend to me once more in a mere %d minutes." % waterWally.format()
    else:
        return output.decode().strip() + 'S i p p'

def play(song):
    return 'Now Playing: Despacito ft. Daddy Yankee'

def graph():
    pass
