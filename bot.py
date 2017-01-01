import asyncio
import discord
import text_adventure

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None

    @asyncio.coroutine
    def do_command(self, message, command, *args):
        yield from getattr(self, command)(message, *args)

    @asyncio.coroutine
    def game(self, message, command, *args):
        yield from getattr(self, 'game_' + command)(message, *args)

    @asyncio.coroutine
    def game_start(self, message, name):
        if self.game_obj is not None:
            return
        self.game_obj = text_adventure.Game(self.config, name)
        yield from self.client.change_presence(game = discord.Game(name = name))
        yield from self.client.send_message(message.channel, self.game_obj.output())

    @asyncio.coroutine
    def game_input(self, message, inp):
        if self.game_obj is None:
            return
        self.game_obj.inp(inp)
        yield from self.client.send_message(message.channel, self.game_obj.output())

    @asyncio.coroutine
    def game_end(self, message):
        if self.game_obj is None:
            return
        self.game_obj.stop()
        self.game_obj = None
        yield from self.client.change_presence(game = discord.Game(name = ''))

    @asyncio.coroutine
    def parse_chatter(self, message):
        if message.content.lower() == 'so' or ':so:' in message.content.lower():
            yield from self.client.send_message(message.channel, 'so')
        elif message.content.startswith(self.config['game_prefix']) and self.game_obj is not None:
            yield from self.game_input(message, message.content[1:])
