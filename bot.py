import asyncio
import discord

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config

    @asyncio.coroutine
    def do_command(self, command, *args):
        yield from getattr(self, command)(*args)

    @asyncio.coroutine
    def game(self, *args):
        print("Doing command")
        print(args[0])
        yield from self.client.change_presence(game = discord.Game(name = args[0]))
