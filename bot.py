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
import nasa
import tramtracker
import datetime 

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None
        self.polls = {}
        self.groups = ['metro', 'quotes', 'lenny', 'poll', 'wa', 'waa', 'clear', 'tex', 'astro', 'tram']
        wolf.startWA(config['WA_appid'])

    @asyncio.coroutine
    def astro(self, message):
        (content, is_embed) = nasa.get_astropod(api_key=self.config['NASA-API'])
        if is_embed:
            yield from self.client.send_message(message.channel, embed=content)
        else:
            yield from self.client.send_message(message.channel, content)

    @asyncio.coroutine
    def astro_task(self, *args):
        yield from self.client.wait_until_ready()
        while not self.client.is_closed:
            now = datetime.datetime.now()
            endtime = datetime.datetime(now.year, now.month, now.day,9,30)
            if now.time() > datetime.time(9,30):
                endtime += datetime.timedelta(1)
            yield from asyncio.sleep((endtime - now).total_seconds())
            (content, is_embed) = nasa.get_astropod(api_key=self.config['NASA-API'])
            if is_embed:
                yield from self.client.send_message(discord.Object(id = self.config['space_channel']), embed=content)
            else:
                yield from self.client.send_message(discord.Object(id = self.config['space_channel']), content)
         

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
    def metro(self, message, *ignore):
        disruptions = metro.get_disruptions(message.content[7:])
        yield from self.client.send_message(message.channel, disruptions)

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
        process = subprocess.Popen(["fortune", "quotes.local", "-i", "-m", search], stdout=subprocess.PIPE)
        output, error = process.communicate()
        result = str.replace(output.decode(), '%\n','-------------------\n')
        yield from self.client.send_message(message.channel, result)

    @asyncio.coroutine
    def tram_route(self, message, stop, route, direction = None, *args):
        services = tramtracker.get_next_services(tramtracker.get_stops(stop, route),route, False, direction)
        yield from self.client.send_message(message.channel, services)

    @asyncio.coroutine
    def tram_stop(self, message, stop, *args):
        stops = tramtracker.get_all_stops(stop)
        yield from self.client.send_message(message.channel, stops['message'])
        msg = yield from self.client.wait_for_message(author=message.author, check=tramtracker.check_tram_number)
        
        try:
            stop = list(stops['matches'].values())[int(msg.content)]
        except IndexError:         
            yield from self.client.send_message(message.channel, 'Invalid selection') 
        services = tramtracker.get_next_services(stop, stop['route'], True)
        yield from self.client.send_message(message.channel, services)

    @asyncio.coroutine
    def tram_help(self, message, *args):
        messages = 'Syntax is: \n-!tram route [stop_number] [route] [direction (optional)] - Gives you the departures for a specific line at a specific stop \n-!tram stop [stop_number] - Gives you the departures from a stop for all routes'
        yield from self.client.send_message(message.channel, messages)

    @asyncio.coroutine
    def tram(self, message, command, *args):
        yield from getattr(self, 'tram_' + command)(message, *args)
