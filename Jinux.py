import asyncio
from configparser import ConfigParser
from datetime import datetime
from time import localtime, strftime

import discord
import aiml
from twitch.api import v3

from cmds import (bhelp, cat, channelinfo, choose, chucknorris, coinflip, convert, dice, dictionary, eightball, gif,
                  info, poll, purge, reddit, restart, rps, serverinfo, temp, time, trans, twitch, update, uptime, xkcd,
                  youtube)
import auto_welcome


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
cmd_char = config.get('Jinux', 'Character')
Client_ID = config.getint('Jinux', 'Client_ID')
Channel_ID = config.getint('Jinux', 'Channel')

# Preparing the bot
dclient = discord.Client()

# poll system variables
poll_enable = False
poll_question = ""
options = []
votes = []
voted = []

# Twitch setup
twitch_enabled = config.getboolean('Twitch', 'Enabled')
streamers = config.get('Twitch', 'Users').split(',')
active = list()
start_time = 0

try:
    twitch_channel = config.getint('Twitch', 'Channel')
except ValueError:
    twitch_channel = config.getint('Jinux', 'Channel')

async def twitch_live_stream_notify():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
        await asyncio.sleep(config.getint('Twitch', 'Interval'))
        log('AUTO_TASK', 'Running Twitch auto task...')
        if twitch_enabled and len(streamers) > 0:
            for streamer in streamers:
                stream = v3.streams.by_channel(streamer)
                if stream['stream'] is not None:
                    if streamer not in active:
                        await dclient.send_message(dclient.get_channel(str(twitch_channel)),
                                                   "**{0}** is now live! @<https://www.twitch.tv/{0}>".format(streamer))
                    active.append(streamer)
                else:
                    if streamer in active:
                        active.remove(streamer)


# Chat Setup
chat = aiml.Kernel()
chat.learn('aiml_files/*.aiml')
chat.respond('load aiml b')


# Sets up the game status
@dclient.event
async def on_ready():
    log('BOOTUP', 'Starting up Jinux system...')
    await dclient.change_presence(game=discord.Game(name=config.get('Jinux', 'Playing')))
    global start_time
    start_time = datetime.now()
    log('BOOTUP', 'Finished starting up Jinux system!')
    if Channel_ID != 0:
        await dclient.send_message(discord.Object(id=Channel_ID), ":wave:")


# Auto welcome new members
@dclient.event
async def on_member_join(member):
    if config.getboolean('Jinux', 'Auto_Welcome'):
        await auto_welcome.welcome(dclient, member, config.getint('Auto_Welcome_Channel'), '<@{}>'.format(member.id))


# Mention function
def get_mention(a):
    return '<@{}>'.format(a.author.id)


# Real Player Name
def get_name(msg):
    return discord.utils.get(discord.utils.get(dclient.servers, id=msg.channel.server.id).members,
                             id=msg.author.id).name


# Chatter Bot
@dclient.event
async def on_message(msg):
    if msg.content.startswith(cmd_char):
        global poll_enable, poll_question, options, votes, voted, twitch_enabled, Channel_ID, streamers, active, \
            twitch_channel
        cmd = msg.content[1:].split(' ')[0]
        if cmd == 'cat' and config.getboolean('Functions', 'Random_cat'):
            log('COMMAND', 'Executing {}cat command for {}.'.format(cmd_char, get_name(msg)))
            await cat.ex(dclient, msg.channel)
        elif cmd == 'channelinfo' and config.getboolean('Functions', 'ChannelInfo'):
            log('COMMAND', 'Executing {}channelinfo command for {}.'.format(cmd_char, get_name(msg)))
            await channelinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
        elif cmd == 'choose' and config.getboolean('Functions', 'Choose'):
            o = msg.content[8:].split(' ')
            log('COMMAND', 'Executing {}choose command for {}.'.format(cmd_char, get_name(msg)))
            await choose.ex(dclient, msg.channel, get_mention(msg), o, cmd_char)
        elif cmd == 'chucknorris' and config.getboolean('Functions', 'Chucknorris'):
            log('COMMAND', 'Executing {}chucknorris command for {}.'.format(cmd_char, get_name(msg)))
            await chucknorris.ex(dclient, msg.channel)
        elif cmd == 'coinflip' and config.getboolean('Functions', 'Coinflip'):
            log('COMMAND', 'Executing {}coinflip command for {}.'.format(cmd_char, get_name(msg)))
            await coinflip.ex(dclient, msg.channel, get_mention(msg))
        elif cmd == 'convert' and config.getboolean('Functions', 'Currency'):
            log('COMMAND', 'Executing {}convert command for {}.'.format(cmd_char, get_name(msg)))
            await convert.ex(dclient, msg.channel, get_mention(msg), msg.content[9:].split(' '), cmd_char)
        elif cmd == 'dice' and config.getboolean('Functions', 'Dice'):
            log('COMMAND', 'Executing {}dice command for {}.'.format(cmd_char, get_name(msg)))
            await dice.ex(dclient, msg.channel, get_mention(msg))
        elif cmd == 'dictionary' and config.getboolean('Functions', 'Dictionary'):
            log('COMMAND', 'Executing {}dictionary command for {}.'.format(cmd_char, get_name(msg)))
            await dictionary.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content[12:], cmd_char)
        elif cmd == '8ball' and config.getboolean('Functions', 'EightBall'):
            log('COMMAND', 'Executing {}8ball command for {}.'.format(cmd_char, get_name(msg)))
            await eightball.ex(dclient, msg.channel, get_mention(msg), msg.content[7:], cmd_char)
        elif cmd == 'gif' and config.getboolean('Functions', 'Random_gif'):
            log('COMMAND', 'Executing {}gif command for {}.'.format(cmd_char, get_name(msg)))
            await gif.ex(dclient, msg.channel, msg.content[5:], get_mention(msg), cmd_char)
        elif cmd == 'help':
            log('COMMAND', 'Executing {}help command for {}.'.format(cmd_char, get_name(msg)))
            await bhelp.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content.split(' '), cmd_char)
        elif cmd == 'info':
            log('COMMAND', 'Executing {}info command for {}.'.format(cmd_char, get_name(msg)))
            await info.ex(dclient, msg.channel)
        elif cmd == 'poll' and config.getboolean('Functions', 'poll'):
            log('COMMAND', 'Executing {}poll command for {}.'.format(cmd_char, get_name(msg)))
            poll_enable, poll_question, options, votes, voted = await poll.ex_poll(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted, cmd_char)
        elif cmd == 'purge' and config.getboolean('Functions', 'Purge'):
            log('COMMAND', 'Executing {}purge command for {}.'.format(cmd_char, get_name(msg)))
            await purge.ex(dclient, msg.channel, get_mention(msg), msg.content[7:], cmd_char)
        elif cmd == 'vote' and config.getboolean('Functions', 'poll'):
            log('COMMAND', 'Executing {}vote command for {}.'.format(cmd_char, get_name(msg)))
            poll_enable, poll_question, options, votes, voted = await poll.ex_vote(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted)
        elif cmd == 'reddit' and config.getboolean('Functions', 'Reddit'):
            log('COMMAND', 'Executing {}reddit command for {}.'.format(cmd_char, get_name(msg)))
            await reddit.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content[8:])
        elif cmd == 'rps' and config.getboolean('Functions', 'Rock_paper_scissors'):
            log('COMMAND', 'Executing {}rps command for {}.'.format(cmd_char, get_name(msg)))
            await rps.ex(dclient, msg.channel, get_mention(msg), msg.content[5:], cmd_char)
        elif cmd == 'serverinfo' and config.getboolean('Functions', 'ServerInfo'):
            log('COMMAND', 'Executing {}serverinfo command for {}.'.format(cmd_char, get_name(msg)))
            await serverinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
        elif cmd == 'temp' and config.getboolean('Functions', 'Temperature'):
            log('COMMAND', 'Executing {}temp command for {}.'.format(cmd_char, get_name(msg)))
            await temp.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
        elif cmd == 'time' and config.getboolean('Functions', 'Timezone'):
            log('COMMAND', 'Executing {}time command for {}.'.format(cmd_char, get_name(msg)))
            await time.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
        elif cmd == 'trans' and config.getboolean('Functions', 'Translate'):
            log('COMMAND', 'Executing {}trans command for {}.'.format(cmd_char, get_name(msg)))
            await trans.ex(dclient, msg.channel, get_mention(msg), msg.content[7:], cmd_char)
        elif cmd == 'twitch':
            log('COMMAND', 'Executing {}twitch command for {}.'.format(cmd_char, get_name(msg)))
            twitch_enabled, Channel_ID, streamers, active = await twitch.ex(
                dclient, msg.author, msg.channel, get_mention(msg), msg.content[8:], twitch_enabled, twitch_channel,
                streamers, active, cmd_char)
        elif cmd == 'update' and config.getboolean('Functions', 'Update'):
            print()
            # TODO
        elif cmd == 'uptime':
            log('COMMAND', 'Executing {}uptime command for {}.'.format(cmd_char, get_name(msg)))
            await uptime.ex(dclient, msg.channel, start_time)
        elif cmd == 'xkcd' and config.getboolean('Functions', 'XKCD'):
            log('COMMAND', 'Executing {}xkcd command for {}.'.format(cmd_char, get_name(msg)))
            await xkcd.ex(dclient, msg.channel, msg.content[6:])
        elif cmd == 'youtube' and config.getboolean('Functions', 'Youtube'):
            log('COMMAND', 'Executing {}youtube command for {}.'.format(cmd_char, get_name(msg)))
            await youtube.ex(dclient, msg.channel, get_mention(msg), msg.content[9:], cmd_char)
        elif cmd == '9':
            log('COMMAND', 'Executing {}restart command for {}.'.format(cmd_char, get_name(msg)))
            await restart.ex(dclient, msg.channel, get_mention(msg), msg.author)
    elif msg.content.startswith('<@{}>'.format(Client_ID)) and config.getboolean('Functions', 'Cleverbot') \
            and Client_ID != 0:
        if int(msg.author.id) != int(Client_ID):
            log('CHATTER_BOT', 'Responding to {}.'.format(get_name(msg)))
            await dclient.send_message(msg.channel, '{} {}'.format(get_mention(msg), chat.respond(msg.content[22:])))

# Execute Twitch Loop
if twitch_enabled:
    dclient.loop.create_task(twitch_live_stream_notify())

# Activate Bot
dclient.run(Token_ID)
