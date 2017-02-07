import asyncio
import discord
import text_adventure
import poll

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None
        self.polls = None

    @asyncio.coroutine
    def do_command(self, message, command, *args):
        try:
            yield from getattr(self, command)(message, *args)
        except AttributeError:
            pass

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
        yield from self.client.change_presence(game = None)

    @asyncio.coroutine
    def poll(self, message, command, *args):
        yield from getattr(self, 'poll_' + command)(message, *args)

    @asyncio.coroutine
    def poll_create(self, message, name, question, options):
        if self.polls[name] is not None:
            return
        self.polls[name] = poll.Poll(name, question, options)

    @asyncio.coroutine
    def poll_vote(self, message, name, option):
        if self.polls[name] is None:
            return
        self.polls[name].vote(message.author.id, option)

    @asyncio.coroutine
    def poll_results(self, message, name):
        if self.polls[name] is None:
            return
        self.polls[name].vote(message.author, option)

    @asyncio.coroutine
    def poll_list(self, message):
        if self.polls is None:
            return
        for poll in polls:
            // create message

    @asyncio.coroutine
    def parse_chatter(self, message):
        if message.content.lower() == 'so' or ':so:' in message.content.lower():
            yield from self.client.send_message(message.channel, 'so')
        elif message.content.startswith(self.config['game_prefix']) and self.game_obj is not None:
            yield from self.game_input(message, message.content[1:])
