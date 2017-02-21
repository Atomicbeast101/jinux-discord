import asyncio
from configparser import ConfigParser
from datetime import datetime
from time import localtime, strftime

import discord
from cleverbot import Cleverbot
from twitch.api import v3

from cmds import (bhelp, cat, channelinfo, choose, chucknorris, coinflip, convert, dice, dictionary, eightball, gif,
                  info, poll, reddit, restart, rps, serverinfo, temp, time, trans, twitch, update, uptime, xkcd,
                  youtube)


# Setup ConfigParser
config = ConfigParser()
config.read('config.ini')

# Setup Logging
log_file = open('jinux.log', 'a')
if config.getboolean('Jinux', 'Logging'):
    def log(typ, reason):
        print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), typ, reason))
        log_file.write(
            '[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), typ, reason))

# Fetch config data and turn it into objects
Token_ID = config.get('Jinux', 'Token')
Cmd_char = config.get('Jinux', 'Character')
Client_ID = config.getint('Jinux', 'Client_ID')
Channel_ID = config.getint('Jinux', 'Channel')

# Preparing the bot
dclient = discord.Client()

# Poll system variables
Poll = False
Poll_question = ""
opt = []
vts = []
vtd = []


# Twitch setup
twitch_enabled = config.getboolean('Twitch', 'Enabled')
Streamers = config.get('Twitch', 'Users').split(',')
active = list()

try:
    twitch_channel = config.getint('Twitch', 'Channel')
except ValueError:
    twitch_channel = config.getint('Jinux', 'Channel')

async def twitch_live_stream_notify():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
        await asyncio.sleep(config.getint('Twitch', 'Interval'))
        log('AUTO_TASK', 'Running Twitch auto task...')
        if twitch_enabled and len(Streamers) > 0:
            for Streamer in Streamers:
                Stream = v3.streams.by_channel(Streamer)
                if Stream['stream'] is not None:
                    if Streamer not in active:
                        await dclient.send_message(dclient.get_channel(str(twitch_channel)),
                                                   "**{0}** is now live! @<https://www.twitch.tv/{0}>".format(Streamer))
                    active.append(Streamer)
                else:
                    if Streamer in active:
                        active.remove(Streamer)


# Cleverbot setup
cb = Cleverbot()


# Sets up the game status
@dclient.event
async def on_ready():
    log('BOOTUP', 'Starting up Jinux system...')
    await dclient.change_presence(game=discord.Game(name=config.get('Jinux', 'Playing')))
    global starttime
    starttime = datetime.now()
    log('BOOTUP', 'Finished starting up Jinux system!')
    if twitch_enabled:
        await dclient.loop.create_task(twitch_live_stream_notify())
    if Channel_ID != 0:
        await dclient.send_message(discord.Object(id=Channel_ID), ":wave:")


# Mention function
def get_m(a):
    return '<@{}>'.format(a.author.id)


# Chatter Bot
@dclient.event
async def on_message(msg):
    if msg.content.startswith(Cmd_char):
        global Poll, Poll_question, opt, vts, vtd, twitch_enabled, Channel_ID, Streamers, active, twitch_channel
        cmd = msg.content[1:].split(' ')[0]
        if cmd == 'cat' and config.getboolean('Functions', 'Random_cat'):
            log('COMMAND', 'Executing {}cat command for {}.'.format(Cmd_char, get_m(msg)))
            await cat.ex(dclient, msg.channel)
        elif cmd == 'channelinfo' and config.getboolean('Functions', 'ChannelInfo'):
            log('COMMAND', 'Executing {}channelinfo command for {}.'.format(Cmd_char, get_m(msg)))
            await channelinfo.ex(dclient, msg.author, msg.channel, get_m(msg))
        elif cmd == 'choose' and config.getboolean('Functions', 'Choose'):
            o = msg.content[8:].split(' ')
            log('COMMAND', 'Executing {}choose command for {}.'.format(Cmd_char, get_m(msg)))
            await choose.ex(dclient, msg.channel, get_m(msg), o, Cmd_char)
        elif cmd == 'chucknorris' and config.getboolean('Functions', 'Chucknorris'):
            log('COMMAND', 'Executing {}chucknorris command for {}.'.format(Cmd_char, get_m(msg)))
            await chucknorris.ex(dclient, msg.channel)
        elif cmd == 'coinflip' and config.getboolean('Functions', 'Coinflip'):
            log('COMMAND', 'Executing {}coinflip command for {}.'.format(Cmd_char, get_m(msg)))
            await coinflip.ex(dclient, msg.channel, get_m(msg))
        elif cmd == 'convert' and config.getboolean('Functions', 'Currency'):
            log('COMMAND', 'Executing {}convert command for {}.'.format(Cmd_char, get_m(msg)))
            await convert.ex(dclient, msg.channel, get_m(msg), msg.content[9:].split(' '), Cmd_char)
        elif cmd == 'dice' and config.getboolean('Functions', 'Dice'):
            log('COMMAND', 'Executing {}dice command for {}.'.format(Cmd_char, get_m(msg)))
            await dice.ex(dclient, msg.channel, get_m(msg))
        elif cmd == 'dictionary' and config.getboolean('Functions', 'Dictionary'):
            log('COMMAND', 'Executing {}dictionary command for {}.'.format(Cmd_char, get_m(msg)))
            await dictionary.ex(dclient, msg.author, msg.channel, get_m(msg), msg.content[11:], Cmd_char)
        elif cmd == '8ball' and config.getboolean('Functions', 'EightBall'):
            log('COMMAND', 'Executing {}8ball command for {}.'.format(Cmd_char, get_m(msg)))
            await eightball.ex(dclient, msg.channel, get_m(msg), msg.content[7:], Cmd_char)
        elif cmd == 'gif' and config.getboolean('Functions', 'Random_gif'):
            log('COMMAND', 'Executing {}gif command for {}.'.format(Cmd_char, get_m(msg)))
            await gif.ex(dclient, msg.channel, msg.content[5:], get_m(msg), Cmd_char)
        elif cmd == 'help':
            log('COMMAND', 'Executing {}help command for {}.'.format(Cmd_char, get_m(msg)))
            await bhelp.ex(dclient, msg.author, msg.channel, get_m(msg), msg.content.split(' '), Cmd_char)
        elif cmd == 'info':
            log('COMMAND', 'Executing {}info command for {}.'.format(Cmd_char, get_m(msg)))
            await info.ex(dclient, msg.channel)
        elif cmd == 'poll' and config.getboolean('Functions', 'Poll'):
            log('COMMAND', 'Executing {}poll command for {}.'.format(Cmd_char, get_m(msg)))
            Poll, Poll_question, opt, vts, vtd = await poll.ex_poll(dclient, msg.channel, msg.author, get_m(msg),
                                                                    msg.content[
                                                                        6:],
                                                                    Poll, Poll_question, opt, vts, vtd, Cmd_char)
        elif cmd == 'vote' and config.getboolean('Functions', 'Poll'):
            log('COMMAND', 'Executing {}vote command for {}.'.format(Cmd_char, get_m(msg)))
            Poll, Poll_question, opt, vts, vtd = await poll.ex_vote(dclient, msg.channel, msg.author, get_m(msg),
                                                                    msg.content[
                                                                        6:],
                                                                    Poll, Poll_question, opt, vts, vtd)
        elif cmd == 'reddit' and config.getboolean('Functions', 'Reddit'):
            log('COMMAND', 'Executing {}reddit command for {}.'.format(Cmd_char, get_m(msg)))
            await reddit.ex(dclient, msg.author, msg.channel, get_m(msg), msg.content[8:])
        elif cmd == 'rps' and config.getboolean('Functions', 'Rock_paper_scissors'):
            log('COMMAND', 'Executing {}rps command for {}.'.format(Cmd_char, get_m(msg)))
            await rps.ex(dclient, msg.channel, get_m(msg), msg.content[5:], Cmd_char)
        elif cmd == 'serverinfo' and config.getboolean('Functions', 'ServerInfo'):
            log('COMMAND', 'Executing {}serverinfo command for {}.'.format(Cmd_char, get_m(msg)))
            await serverinfo.ex(dclient, msg.author, msg.channel, get_m(msg))
        elif cmd == 'temp' and config.getboolean('Functions', 'Temperature'):
            log('COMMAND', 'Executing {}temp command for {}.'.format(Cmd_char, get_m(msg)))
            await temp.ex(dclient, msg.channel, get_m(msg), msg.content[6:], Cmd_char)
        elif cmd == 'time' and config.getboolean('Functions', 'Timezone'):
            log('COMMAND', 'Executing {}time command for {}.'.format(Cmd_char, get_m(msg)))
            await time.ex(dclient, msg.channel, get_m(msg), msg.content[6:], Cmd_char)
        elif cmd == 'trans' and config.getboolean('Functions', 'Translate'):
            log('COMMAND', 'Executing {}trans command for {}.'.format(Cmd_char, get_m(msg)))
            await trans.ex(dclient, msg.channel, get_m(msg), msg.content[7:], Cmd_char)
        elif cmd == 'twitch':
            log('COMMAND', 'Executing {}twitch command for {}.'.format(Cmd_char, get_m(msg)))
            twitch_enabled, Channel_ID, Streamers, active = await twitch.ex(
                dclient, msg.author, msg.channel, get_m(msg), msg.content[8:], twitch_enabled, twitch_channel,
                Streamers, active, Cmd_char)
        elif cmd == 'update' and config.getboolean('Functions', 'Update'):
            print()
            # TODO
        elif cmd == 'uptime':
            log('COMMAND', 'Executing {}uptime command for {}.'.format(Cmd_char, get_m(msg)))
            await uptime.ex(dclient, msg.channel, starttime)
        elif cmd == 'xkcd' and config.getboolean('Functions', 'XKCD'):
            log('COMMAND', 'Executing {}xkcd command for {}.'.format(Cmd_char, get_m(msg)))
            await xkcd.ex(dclient, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'youtube' and config.getboolean('Functions', 'Youtube'):
            log('COMMAND', 'Executing {}youtube command for {}.'.format(Cmd_char, get_m(msg)))
            await youtube.ex(dclient, msg.channel, get_m(msg), msg.content[9:], Cmd_char)
        elif cmd == '9':
            log('COMMAND', 'Executing {}restart command for {}.'.format(Cmd_char, get_m(msg)))
            await restart.ex(dclient, msg.channel, get_m(msg), msg.author)
    elif msg.content.startswith('<@{}>'.format(Client_ID)) and config.getboolean('Functions', 'Cleverbot') \
            and Client_ID != 0:
        if int(msg.author.id) != int(Client_ID):
            log('CHATTER_BOT', 'Responding to {}.'.format(get_m(msg)))
            await dclient.send_message(msg.channel, '{} {}'.format(get_m(msg), cb.ask(msg.content[22:])))

# Activate Bot
dclient.run(Token_ID)
