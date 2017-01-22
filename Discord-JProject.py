import discord
import requests
import json
import asyncio
from Config import TOKEN_ID, CLIENT_ID, CMD_CHAR
from Data import LANG_LIST, CURR_LIST, HELP, HELP_CAT, HELP_TRANS, HELP_CHUCKNORRIS, HELP_CONVERT, HELP_POLL,\
    HELP_YES, HELP_NO, HELP_BALL, HELP_TEMP, HELP_YOUTUBE, HELP_GIF, HELP_UPTIME, HELP_INFO, HELP_TIME, HELP_TWITCH, \
    HELP_COINFLIP
from translate import Translator
from cleverbot import Cleverbot
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
from random import choice
from twitch.api import v3
from threading import Thread


# Setting up bot
client = discord.Client()


# Uptime
curr_uptime = 0


# Twitch
t_enable = False
ch = 0
users = list()
active = list()


# Cleverbot
cb = Cleverbot('Jinux')


# Preparing the bot
@client.event
async def on_ready():
    # Sets game status
    await client.change_presence(game=discord.Game(name='Bot v2.2 | -help'))

    # Sets up current time status
    global curr_uptime
    curr_uptime = datetime.now()

    # Sets up twitch live status notification
    f = open('twitch_settings.txt', 'r')
    e = f.readline().rstrip()
    global t_enable
    if e == 'True':
        t_enable = True
    else:
        t_enable = False
    c = f.readline().rstrip()
    global ch
    ch = int(c)
    f.close()
    fu = open('twitch_usernames.txt', 'r')
    global users
    for li in fu:
        users.append(li.rstrip())
    fu.close()


async def run_notify():
    while True:
        await asyncio.sleep(60)
        if t_enable:
            for u in users:
                r = v3.streams.by_channel(u)['stream']
                if r is not None:
                    if u not in active:
                        await client.send_message(client.get_channel(str(ch)), '**{0} is now live!** Link: <https://'
                                                                               'www.twitch.tv/{0}>'.format(u))
                    active.append(u)
                else:
                    if u in active:
                        active.remove(u)

l = asyncio.get_event_loop()
l.call_soon_threadsafe(asyncio.async, run_notify())


# Variables for poll system
poll = False
q = ""
yes = 0
no = 0
voted = []


# Checks to make sure the string currency can be converted to float data value
def chk_curr(msg):
    try:
        float(msg)
        return True
    except ValueError:
        return False


# Checks to make sure the string temperature can be converted to int data value
def chk_temp(msg):
    try:
        int(msg)
        return True
    except ValueError:
        return False


# Checks to make sure the temperature measurement is in F, K, or C
def chk_temp_msr(msg):
    msg = msg.upper()
    if msg == 'F' or msg == 'K' or msg == 'C':
        return True
    return False


# Returns the mention of the author that the bot will reply to
def get_mention(msg):
    return '<@{}>'.format(msg.author.id)


# Automatically called every time a player sends a message to any channel
@client.event
async def on_message(msg):
    global poll
    global q
    global yes
    global no
    global voted
    if len(msg.content) > 0:
        if msg.content[0] == CMD_CHAR:
            cmd = msg.content.split(' ')[0].lower()
            # Help Guide
            if cmd == CMD_CHAR + 'help':
                args = msg.content.split(' ')
                if len(args) == 2:
                    arg = args[1].lower()
                    arg = arg.replace(CMD_CHAR, '')
                    if arg == 'cat':
                        await client.send_message(msg.channel, HELP_CAT)
                    elif arg == 'trans':
                        await client.send_message(msg.channel, HELP_TRANS)
                    elif arg == 'chucknorris':
                        await client.send_message(msg.channel, HELP_CHUCKNORRIS)
                    elif arg == 'convert':
                        await client.send_message(msg.channel, HELP_CONVERT)
                    elif arg == 'poll':
                        await client.send_message(msg.channel, HELP_POLL)
                    elif arg == 'yes':
                        await client.send_message(msg.channel, HELP_YES)
                    elif arg == 'no':
                        await client.send_message(msg.channel, HELP_NO)
                    elif arg == '8ball':
                        await client.send_message(msg.channel, HELP_BALL)
                    elif arg == 'temp':
                        await client.send_message(msg.channel, HELP_TEMP)
                    elif arg == 'youtube':
                        await client.send_message(msg.channel, HELP_YOUTUBE)
                    elif arg == 'gif':
                        await client.send_message(msg.channel, HELP_GIF)
                    elif arg == 'uptime':
                        await client.send_message(msg.channel, HELP_UPTIME)
                    elif arg == 'info':
                        await client.send_message(msg.channel, HELP_INFO)
                    elif arg == 'time':
                        await client.send_message(msg.channel, HELP_TIME)
                    elif arg == 'twitch':
                        await client.send_message(msg.channel, HELP_TWITCH)
                    elif arg == 'coinflip':
                        await client.send_message(msg.channel, HELP_COINFLIP)
                    else:
                        await client.send_message(msg.channel, HELP)
                else:
                    await client.send_message(msg.channel, HELP)
            # Posts random picture/gif of cat through -cat command
            elif cmd == CMD_CHAR + 'cat':
                r = requests.get('http://random.cat/meow')
                d = json.loads(r.text)
                await client.send_message(msg.channel, '{}'.format(d['file']))
            # Translate message to language of user choice through -trans command
            elif cmd == CMD_CHAR + 'trans':
                args = msg.content.split(' ')
                if len(args) >= 3:
                    if args[1].upper() in LANG_LIST:
                        s = msg.content[10:]
                        tr = Translator(to_lang=args[1])
                        tn = tr.translate(s)
                        await client.send_message(msg.channel, tn)
                    else:
                        await client.send_message(msg.channel, '{} Invalid language input! Please check https://www.' +
                                                               'sitepoint.com/web-foundations/iso-2-letter-language-' +
                                                               'codes/ for correct language code! Ex: en for English ' +
                                                               'or de for German'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}trans <language> '
                                                           '<to translate...>'.format(get_mention(msg), CMD_CHAR))
            # Posts random Chuck Norris joke through -chucknorris command
            elif cmd == CMD_CHAR + 'chucknorris':
                r = requests.get('https://api.chucknorris.io/jokes/random')
                d = json.loads(r.text)
                await client.send_message(msg.channel, d['value'])
            # Converts money between different currencies through -convert command
            elif cmd == CMD_CHAR + 'convert':
                args = msg.content.split(' ')
                if len(args) == 4:
                    b = args[1]
                    cc = args[2].upper()
                    ct = args[3].upper()
                    if chk_curr(b):
                        b = float(b)
                        if cc in CURR_LIST and ct in CURR_LIST:
                            r = requests.get('http://free.currencyconverterapi.com/api/v3/convert?q={}_{}&compact=y'
                                             .format(cc, ct))
                            d = json.loads(r.text)
                            nb = b * float(d[cc + '_' + ct]['val'])
                            await client.send_message(msg.channel, '`{}: {:.2f}` > `{}: {:.2f}`'.format(cc, b, ct, nb))
                        else:
                            await client.send_message(msg.channel, '{} Invalid currency code! Please check https://' +
                                                                   'currencysystem.com/codes/!'
                                                                   .format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, '{} Currency must be in numeric/decimal value! Like ' +
                                                               '100 or 54.42!'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}convert <amount> <current-currency> <currency' +
                                                           '-to-convert-to>'.format(get_mention(msg), CMD_CHAR))
            # Poll system through -poll command
            elif cmd == CMD_CHAR + 'poll':
                if msg.channel.permissions_for(msg.author).administrator:
                    args = msg.content.split(' ')
                    if len(args) >= 2:
                        if args[1].lower() == 'start':
                            if len(args) >= 3:
                                if poll:
                                    await client.send_message(msg.channel, '{} poll already running! Please close '
                                                                           'the current one with: {}poll stop'
                                                                           .format(get_mention(msg), CMD_CHAR))
                                else:
                                    poll = True
                                    yes = 0
                                    no = 0
                                    voted = []
                                    q = msg.content[12:]
                                    await client.send_message(msg.channel, '[Poll Started]: {}'.format(q))
                                    await client.send_message(msg.channel, 'Answer: -yes OR -no')
                            else:
                                await client.send_message(msg.channel, '{} Usage: {}poll start <Question...?>'
                                                                       .format(get_mention(msg), CMD_CHAR))
                        elif args[1].lower() == 'stop':
                            if not poll:
                                await client.send_message(msg.channel, "Poll isn't running, {}!"
                                                                       .format(get_mention(msg)))
                            else:
                                poll = False
                                await client.send_message(msg.channel, '[Poll Closed]: {}'.format(q))
                                await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                              str(no)))
                        else:
                            await client.send_message(msg.channel, '{} Usage: {}poll <start|stop> (Question...?)'
                                                                   .format(get_mention(msg), CMD_CHAR))
                    else:
                        await client.send_message(msg.channel, '{} Usage: {}poll <start|stop> (Question...?)'
                                                               .format(get_mention(msg), CMD_CHAR))
                else:
                    await client.send_message(msg.channel, 'You must be an administrator, {}!'.format(get_mention(msg)))
            elif cmd == CMD_CHAR + 'yes':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        yes += 1
                        await client.send_message(msg.channel, '[Question]: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                      str(no)))
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud, {}?'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say yes for, {}?'
                                                           .format(get_mention(msg)))
            elif cmd == CMD_CHAR + 'no':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        no += 1
                        await client.send_message(msg.channel, '[Question]: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                      str(no)))
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud, {}?'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say no for, {}?'
                                                           .format(get_mention(msg)))
            # Magic eight ball through -8ball command
            elif cmd == CMD_CHAR + '8ball':
                if len(msg.content.split(' ')) > 1:
                    q = msg.content[7:]
                    q.replace(' ', '%')
                    q.replace('?', '%3F')
                    q.replace(',', '%2C')
                    r = requests.get('https://8ball.delegator.com/magic/JSON/' + q)
                    d = json.loads(r.text)
                    await client.send_message(msg.channel, '{} {}'.format(get_mention(msg), d['magic']['answer']))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}8ball <Question...>'.format(get_mention(msg),
                                                                                                    CMD_CHAR))
            # Convert temperature between F and C through -temp command
            elif cmd == CMD_CHAR + 'temp':
                args = msg.content.split(' ')
                if len(args) == 4:
                    if chk_temp(args[1]):
                        t = int(args[1])
                        if chk_temp_msr(args[2]) and chk_temp_msr(args[3]):
                            fr = args[2][0]
                            to = args[3][0]
                            if fr.upper() == 'F' and to.upper() == 'K':
                                ft = (t + 459.67) * (5/9)
                                await client.send_message(msg.channel, '`{:.1f} Fahrenheit`  >  `{:.1f} Kelvin`'
                                                          .format(t, ft))
                            elif fr.upper() == 'F' and to.upper() == 'C':
                                ft = (t - 32) * .5556
                                await client.send_message(msg.channel, '`{:.1f} Fahrenheit`  >  `{:.1f} Celsius`'
                                                          .format(t, ft))
                            elif fr.upper() == 'K' and to.upper() == 'F':
                                ft = (t * (9 / 5)) - 459.67
                                await client.send_message(msg.channel, '`{:.1f} Kelvin`  >  `{:.1f} Fahrenheit`'
                                                          .format(t, ft))
                            elif fr.upper() == 'K' and to.upper() == 'C':
                                ft = (t * (9/5)) - 273.15
                                await client.send_message(msg.channel, '`{:.1f} Kelvin`  >  `{:.1f} Celsius`'
                                                          .format(t, ft))
                            elif fr.upper() == 'C' and to.upper() == 'F':
                                ft = (t * 1.8) + 32
                                await client.send_message(msg.channel, '`{:.1f} Celsius`  >  `{:.1f} Fahrenheit`'
                                                          .format(t, ft))
                            elif fr.upper() == 'C' and to.upper() == 'K':
                                ft = (t + 273.15) * (5 / 9)
                                await client.send_message(msg.channel, '`{:.1f} Celsius`  >  `{:.1f} Kelvin`'
                                                          .format(t, ft))
                        else:
                            await client.send_message(msg.channel, 'You can only convert the temperature between F, K, '
                                                                   'or C, {}'.format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, 'Temperature to convert must be in whole # (lke 19 or '
                                                               '25, {}'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}temp <temp#> <from F|K|C> '
                                                           '<to F|K|C>'.format(get_mention(msg), CMD_CHAR))
            # Search first video from YouTube
            elif cmd == CMD_CHAR + 'youtube':
                args = msg.content.split(' ')
                if len(args) >= 2:
                    se = msg.content[8:]
                    se.replace(" ", "+")
                    try:
                        s = BeautifulSoup(requests.get('https://www.youtube.com/results?search_query={}'.format(se))
                                          .text, 'html.parser')
                        vds = s.find('div', id='results').find_all('div', class_='yt-lockup-content')
                        if not vds:
                            await client.send_message(msg.channel, "{} Couldn't find any results!"
                                                      .format(get_mention(msg)))
                        i, f = 0, False
                        while not f and i < 20:
                            h = vds[i].find('a', class_='yt-uix-sessionlink')['href']
                            if h.startswith('/watch'):
                                f = True
                            i += 1
                        if not f:
                            await client.send_message(msg.channel, "{} Couldn't find any link!"
                                                      .format(get_mention(msg)))
                        await client.send_message(msg.channel, 'https://youtube.com{}'.format(h))
                    except Exception as ex:
                        await client.send_message(msg.channel, '{} Unable to search for a video!'
                                                  .format(get_mention(msg)))
                        print(ex)
                else:
                    await client.send_message(msg.channel, '{} Usage: {}youtube <to-search>'.format(get_mention(msg),
                                                                                                    CMD_CHAR))
            # Posts random GIF from Giphy depending on tags players put down
            elif cmd == CMD_CHAR + 'gif':
                args = msg.content.split(' ')
                if len(args) >= 2:
                    try:
                        s = msg.content[6:]
                        s = s.replace(' ', '+')
                        r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(s))
                        d = json.loads(r.text)
                        await client.send_message(msg.channel, '{}'.format(
                                                                    d['data']['fixed_height_downsampled_url']))
                    except Exception as ex:
                        await client.send_message(msg.channel, '{} Unable to find a GIF!'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}gif <tags>'.format(get_mention(msg),
                                                                                           CMD_CHAR))
            # Prints current up time of bot
            elif cmd == CMD_CHAR + 'uptime':
                now_uptime = datetime.now()
                t = now_uptime - curr_uptime
                ft = datetime(1, 1, 1) + timedelta(seconds=t.seconds)
                await client.send_message(msg.channel, 'I have been up for `{} days`, `{} hours`, `{} minutes` '
                                                       'and `{} seconds`.'.format(str(ft.day - 1), str(ft.hour),
                                                                                  str(ft.minute), str(ft.second)))
            # Prints information about the bot
            elif cmd == CMD_CHAR + 'info':
                await client.send_message(msg.channel, "I'm a bot, obviously. My master is Atomicbeast101, you can "
                                                       "find my source files at http://github.com/Atomicbeast101/"
                                                       "Discord-JProject")
            # Prints current time according to given timezone
            elif cmd == CMD_CHAR + 'time':
                args = msg.content.split(' ')
                if len(args) == 2:
                    if args[1] in all_timezones:
                        tz = timezone(args[1])
                        t = datetime.now(tz)
                        await client.send_message(msg.channel, 'It is `{:2f}:{:2f}:{:2f}` in `{}` right now.'
                                                  .format(t.hour, t.minute, t.second, args[1]))
                    else:
                        await client.send_message(msg.channel, '{} Invalid timezone! List of timezones: https://'
                                                               'en.wikipedia.org/wiki/List_of_tz_database_time_'
                                                               'zones'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}time <timezone>'.format(get_mention(msg),
                                                                                                CMD_CHAR))
            # Rock, Paper, Scissors Game
            elif cmd == CMD_CHAR + 'rps':
                args = msg.content.split(' ')
                if len(args) == 2:
                    if args[1].lower() in ['rock', 'paper', 'scissors']:
                        r = choice(['rock', 'paper', 'scissors'])
                        if args[1].lower() == 'rock' and r == 'rock':
                            await client.send_message(msg.channel, "{}, you chose {} while I chose {}...it's a tie!"
                                                      .format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'paper' and r == 'paper':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...it's a tie!"
                                                      .format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'scissors' and r == 'scissors':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...it's a tie!"
                                                      .format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'rock' and r == 'paper':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...I win! (paper covers "
                                                      "rock).".format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'rock' and r == 'scissors':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...You win! (rock smashes "
                                                      "scissors).".format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'paper' and r == 'rock':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...You win! (paper covers "
                                                      "rock).".format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'paper' and r == 'scissors':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...I win! (scissors cut "
                                                      "paper).".format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'scissors' and r == 'paper':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...You win! (scissors cut "
                                                      "paper).".format(get_mention(msg), args[1].lower(), r))
                        elif args[1].lower() == 'scissors' and r == 'rock':
                            await client.send_message(msg.channel,
                                                      "{}, you chose {} while I chose {}...I win! (rock smashes "
                                                      "scissors).".format(get_mention(msg), args[1].lower(), r))
                    else:
                        await client.send_message(msg.channel, '{} You must choose between rock, paper, or scissors!'
                                                  .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}rps <rock|paper|scissors>'
                                              .format(get_mention(msg), CMD_CHAR))
            # Twitch live status
            elif cmd == CMD_CHAR + 'twitch':
                args = msg.content.split(' ')
                if len(args) > 1:
                    if args[1].lower() == 'add':
                        if msg.channel.permissions_for(msg.author).administrator:
                            if len(args) == 3:
                                global users
                                if args[2].lower() in users:
                                    await client.send_message(msg.channel, '{}, {} is already added!'
                                                              .format(get_mention(msg), args[2].lower()))
                                else:
                                    users.append(args[2].lower())
                                    f = open('twitch_usernames.txt', 'a')
                                    f.write(args[2].lower() + '\n')
                                    f.close()
                                    await client.send_message(msg.channel, '{}, {} added!'
                                                              .format(get_mention(msg), args[2].lower()))
                            else:
                                await client.send_message(msg.channel, '{} Usage: {}twitch add <username>'
                                                          .format(get_mention(msg), CMD_CHAR))
                        else:
                            await client.send_message(msg.channel, 'You must be an administrator, {}!'
                                                      .format(get_mention(msg)))
                    elif args[1].lower() == 'remove':
                        if msg.channel.permissions_for(msg.author).administrator:
                            if len(args) == 3:
                                if args[2].lower() in users:
                                    users.remove(args[2].lower())
                                    f = open('twitch_usernames.txt', 'w')
                                    for u in users:
                                        f.write(u + '\n')
                                    f.close()
                                    await client.send_message(msg.channel, '{}, {} removed from the list!'
                                                              .format(get_mention(msg), args[2].lower()))
                                else:
                                    await client.send_message(msg.channel, '{}, {} is already added!'
                                                              .format(get_mention(msg), args[2].lower()))
                            else:
                                await client.send_message(msg.channel, '{} Usage: {}twitch remove <username>'
                                                          .format(get_mention(msg), CMD_CHAR))
                        else:
                            await client.send_message(msg.channel, 'You must be an administrator, {}!'
                                                      .format(get_mention(msg)))
                    elif args[1].lower() == 'list':
                        await client.send_message(msg.channel, 'List of Twitch usernames: ```{}```'
                                                  .format(', '.join(str(u) for u in users)))
                    elif args[1].lower() == 'toggle':
                        if msg.channel.permissions_for(msg.author).administrator:
                            global t_enable
                            global ch
                            if t_enable:
                                t_enable = False
                            else:
                                t_enable = True
                            f = open('twitch_settings.txt', 'w')
                            f.write(str(t_enable) + '\n')
                            f.write(str(ch))
                            f.close()
                            await client.send_message(msg.channel, 'Twitch live status notification is now set to `{}`!'
                                                      .format(str(t_enable)))
                        else:
                            await client.send_message(msg.channel, 'You must be an administrator, {}!'
                                                      .format(get_mention(msg)))
                    elif args[1].lower() == 'setchannel':
                        if msg.channel.permissions_for(msg.author).administrator:
                            if len(args) == 3:
                                if chk_temp(args[2]):
                                    ch = int(args[2])
                                    f = open('twitch_settings.txt', 'w')
                                    f.write(str(t_enable) + '\n')
                                    f.write(str(ch))
                                    f.close()
                                    await client.send_message(msg.channel, 'Channel set! Will send notifications '
                                                                           'there!')
                                else:
                                    await client.send_message(msg.channel, '{}, channel ID must be in # value!'
                                                              .format(get_mention(msg)))
                            else:
                                await client.send_message(msg.channel, '{} Usage: {}twitch setchannel <channelID>'
                                                          .format(get_mention(msg), CMD_CHAR))
                        else:
                            await client.send_message(msg.channel, 'You must be an administrator, {}!'
                                                      .format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, '{} Usage: {}twitch <add|remove|list|toggle|setchannel>'
                                                  .format(get_mention(msg), CMD_CHAR))
                else:
                    await client.send_message(msg.channel, '{} Usage: {}twitch <add|remove|list|toggle|setchannel>'
                                              .format(get_mention(msg), CMD_CHAR))
            # Coinflip game
            elif cmd == CMD_CHAR + 'coinflip':
                a = choice(['heads', 'tails'])
                await client.send_message(msg.channel, 'Coinflip: `{}`.'.format(a))
        else:
            # Automatic response to mention. Running on CleverBot API
            if msg.content.startswith('<@' + CLIENT_ID + '>'):
                if int(msg.author.id) != int(CLIENT_ID):
                    m = msg.content[22:]
                    re = cb.ask(m)
                    await client.send_message(msg.channel, '{} {}'.format(get_mention(msg), re))

client.run(TOKEN_ID)
