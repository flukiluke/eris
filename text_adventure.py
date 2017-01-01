import pexpect

class GameException(Exception):
    pass

class Game(object):
    def __init__(self, config, name):
        if name != 'zork':
            raise GameException('Game {} not found'.format(name))
        self.process = pexpect.spawn(config['games']['zork']['frotz'],
                                     [config['games']['zork']['datafile']],
                                     encoding = 'utf8')

    def output(self):
        self.process.expect('(.+)>')
        return self.process.match.groups()[0]

    def inp(self, text):
        self.process.send(text + '\n')

    def stop(self):
        self.process.close()
