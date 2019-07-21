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
import quotes
import translate
import datetime
import langcodes
import basil

class Bot(object):
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.game_obj = None
        self.polls = {}
        self.groups = ['metro', 'quote', 'lenny', 'poll', 'wa', 'waa', 'clear', 'tex', 'astro', 'tram', 'gather', 'tl', 'tll', 'remind', 'basil']
        wolf.startWA(config['WA_appid'])

    @asyncio.coroutine
    def remind(self, message, *args):
        if len(args) < 3:
            yield from self.client.send_message(message.channel, "remind <target> <time> <message>")
            return
        target = args[0]
        if args[0] == 'all':
            target = '@everyone'
        elif args[0] == 'me':
            target = message.author.mention
        yield from alert.queue(target, args[1], args[2])
        yield from self.client.send_message(discord.Object(id = self.config['main_channel']), target + ' ' + args[2])

    @asyncio.coroutine
    def basil(self, message, command, *args):
        yield from getattr(self, 'basil_' + command)(message, *args)

    @asyncio.coroutine
    def basil_moisture(self, message, *args):
        yield from self.client.send_message(message.channel, basil.moisture())

    @asyncio.coroutine
    def basil_history(self, message, samples=48):
        yield from self.client.send_message(message.channel, basil.history(samples))

    @asyncio.coroutine
    def basil_graph(self, message, samples=48):
        imagefile = basil.graph(samples)
        if imagefile is not None:
            yield from self.client.send_file(message.channel, imagefile, filename='graph.png')
            os.system('rm ' + imagefile)

    @asyncio.coroutine
    def basil_water(self, message, runtime):
        yield from self.client.send_message(message.channel, basil.water(int(runtime)))

    @asyncio.coroutine
    def basil_help(self, message, cmd=None):
        yield from self.client.send_message(message.channel, basil.help(str(cmd).strip()))

    @asyncio.coroutine
    def tl(self, message, *ignore):
        yield from self.client.send_message(message.channel, translate.translate(message.content.split(' ', 1)[1]))

    @asyncio.coroutine
    def tll(self, message, language, *args):
        try:
            language_code = str(langcodes.find(language))
        except LookupError:
            yield from self.client.send_message(message.channel, 'Could not find language')
            return
        except:
            yield from self.client.send_message(message.channel, 'A language lookup error occured')
            return
        yield from self.client.send_message(message.channel, translate.translate(message.content.split(' ', 2)[2], language_code))

    # async def gather(self, message):
    #    logfile = open('logs/' + message.channel.name + '.log', 'w')
    #    earliest_msg = message
    #    while True:
    #        try:
    #            async for message in self.client.logs_from(message.channel, before=earliest_msg):
    #                logfile.write(message.timestamp.isoformat() +  '\t' + message.author.name + '\t' + message.content + '\n')
    #            earliest_msg = message
    #        except:
    #            break
    #    logfile.close()

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
            yield from self.client.send_message(discord.Object(id = self.config['main_channel']), quotes.choose())

    @asyncio.coroutine
    def weather_task(self):
        yield from weather.task(self.client, self.config)

    @asyncio.coroutine
    def metro(self, message, *ignore):
        line = message.content[7:]
        yield from metro.get_disruptions(line, self.client, message.channel)

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
         pass

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
        number = int(number) + 1
        if message.channel.id != self.config['quote_channel'] or number < 2 or number > 100 or message.author.id not in self.config['auth_users']:
            return
        yield from self.client.purge_from(message.channel, limit = number)

    @asyncio.coroutine
    def lenny(self, message):
        yield from self.client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

    @asyncio.coroutine
    def quote(self, message, *ignore):
        search = message.content[7:]
        if search == '':
            result = quotes.choose()
        else:
            result = '\n------------\n'.join(quotes.search(search))
        yield from self.client.send_message(message.channel, result)

    @asyncio.coroutine
    def tram_route(self, message, stop, route, direction = None, *args):
        services = tramtracker.get_next_services(tramtracker.get_stops(stop, route, self.config['tram_stop_file']),route, False, direction)
        yield from self.client.send_message(message.channel, services)

    @asyncio.coroutine
    def tram_stop(self, message, stop, *args):
        stops = tramtracker.get_all_stops(stop, self.config['tram_stop_file'])
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
