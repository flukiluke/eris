import asyncio
import discord
import text_adventure
import poll

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None
        self.polls = {}
        self.groups = ['game', 'poll']

    @asyncio.coroutine
    def do_command(self, message, command, *args):
        if command not in self.groups:
            return
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
    def poll_create(self, message, name, question, *options):
        if name in self.polls:
            yield from self.client.send_message(message.channel, "Poll " + name + " already exists")
            return
        self.polls[name] = poll.Poll(name, question, options)
        yield from self.client.send_message(message.channel, "Created poll " + name)

    @asyncio.coroutine
    def poll_delete(self, message, name):
        if name not in self.polls:
            yield from self.client.send_message(message.channel, "Poll " + name + "not found")

        del self.polls[name]
        yield from self.client.send_message(message.channel, "Poll " + name + " deleted")

    @asyncio.coroutine
    def poll_vote(self, message, name, option):
        if name not in self.polls:
            yield from self.client.send_message(message.channel, "Poll " + name + "not found")
            return
        try:
            self.polls[name].vote(message.author, option)
        except LookupError as e:
            yield from self.client.send_message(message.channel, "That's not an option. *This* is an option (list): " + self.polls[name].options_string())
            return
        yield from self.client.send_message(message.channel, "Thank you for voting")

    @asyncio.coroutine
    def poll_results(self, message, name):
        if name not in self.polls:
            yield from self.client.send_message(message.channel, "Poll " + name + " not found")
            return
        results = self.polls[name].results()
        result_message = "Results for poll " + name + "\n"
        for option, voters in results.items():
            result_message += "- **" + option + "**: "
            if len(voters) == 0:
                result_message += "No votes\n"
            elif len(voters) == 1:
                result_message += "1 vote (" + voters[0].display_name + ")\n"
            else:
                result_message += str(len(voters)) + " votes (" + ", ".join([voter.display_name for voter in voters]) + ")\n"
        yield from self.client.send_message(message.channel, result_message)

    @asyncio.coroutine
    def poll_list(self, message):
        if self.polls is None:
            return
        result_message = "Poll list:"
        for poll in self.polls.values():
            result_message += "\n" + poll.name + ": " + poll.question + " Answer " + poll.options_string()
        yield from self.client.send_message(message.channel, result_message)

    @asyncio.coroutine
    def parse_chatter(self, message):
        if message.content.lower() == 'so' or ':so:' in message.content.lower():
            yield from self.client.send_message(message.channel, 'so')
        elif message.content.startswith(self.config['game_prefix']) and self.game_obj is not None:
            yield from self.game_input(message, message.content[1:])
