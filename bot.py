import os
import asyncio
import discord
import poll
import image
import random
import time
import subprocess
import weather
import wolf
import alert
import metro

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None
        self.polls = {}
        self.groups = ['metro', 'weather', 'quotes', 'lenny', 'poll', 'wa', 'waa', 'clear', 'tex']
        wolf.startWA(config['WA_appid'])

    @asyncio.coroutine
    def do_command(self, message, command, *args):
        if command not in self.groups:
            return
        try:
            yield from getattr(self, command)(message, *args)
        except AttributeError:
            pass

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
    def fortune_task(self):
        yield from self.client.wait_until_ready()
        while not self.client.is_closed:
            yield from asyncio.sleep(random.randint(30 * 60 * 60, 40 * 60 * 60))
            yield from self.client.send_message(discord.Object(id = self.config['main_channel']), self.fortune())

    def fortune(self):
        process = subprocess.Popen(["fortune", "quotes.local"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode()

    @asyncio.coroutine
    def weather_task(self):
        yield from weather.task(self.client, self.config)

    @asyncio.coroutine
    def store_weather_task(self):
        yield from weather.store_weather_task(self.client, self.config)

    @asyncio.coroutine
    def weather(self, message):
        weather_data = weather.get_weather()
        result = 'Weather: ' + weather_data['precis'] + ' Top of ' + weather_data['max_temp'] + '°C, ' + weather_data['precip_chance'] + ' chance of up to ' + weather_data['precip_range'] + ' precipitation.'  
        yield from self.client.send_message(message.channel, result)

    @asyncio.coroutine
    def metro(self, message, *ignore):
        yield from metro.get_disruptions(message.content[7:], self.client, self.config)

    @asyncio.coroutine
    def alert_task(self):
        yield from alert.task(self.client, self.config)

    @asyncio.coroutine
    def wa(self, message, *ignore):
        results = wolf.do_wolfram(message.content[4:], False)
        answer = ''
        for result in results:
            answer += "\n" + result
        yield from self.client.send_message(message.channel, answer)

    @asyncio.coroutine
    def waa(self, message, *ignore):
        results = wolf.do_wolfram(message.content[4:], True)
        answer = ''
        for result in results:
            answer += "\n" + result
        yield from self.client.send_message(message.channel, answer)

    @asyncio.coroutine
    def parse_chatter(self, message):
         #print(message.content)
         pass
#        if message.content.lower() == 'so' or ':so:' in message.content.lower():
#            yield from self.client.send_message(message.channel, 'so')
#       elif message.content.startswith(self.config['game_prefix']) and self.game_obj is not None:
#           yield from self.game_input(message, message.content[1:])
#       else:
#           embed, title_text, title = image.get_embed_reply(message.content)
#           if embed is not None:
#               yield from self.client.send_message(message.channel, title, embed = embed)
#               yield from self.client.send_message(message.channel, title_text)

    @asyncio.coroutine
    def tex(self, message, *ignore):
        imagefile = image.get_tex_image(message.content[5:])
        if imagefile is not None:
            yield from self.client.send_file(message.channel, imagefile, filename='render.png')
            os.system('rm ' + imagefile)
        else:
            yield from self.client.send_message(message.channel, 'General Protection Fault')

    @asyncio.coroutine
    def clear(self, message, number):
        number = int(number)
        if message.channel.name != 'quotes' or number < 2 or number > 100:
            return
        yield from self.client.delete_messages(self.client.logs_from(message.channel, limit = number))
   
    @asyncio.coroutine
    def lenny(self, message):
        yield from self.client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

    @asyncio.coroutine
    def quotes(self, message, options):
        search = message.content[8:]
        process = subprocess.Popen(["grep", "-i", search, "quotes.local"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        yield from self.client.send_message(message.channel, output.decode())
