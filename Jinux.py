import asyncio
import logging
from configparser import ConfigParser
from datetime import datetime

import discord
from cleverbot import Cleverbot
from twitch.api import v3

from cmds import (bhelp, cat, choose, chucknorris, coinflip, convert, dice,
                  eightball, gif, info, poll, reddit, restart, rps, temp, time,
                  trans, twitch, uptime, xkcd, youtube)

# Setup Logging
log = logging.getLogger('discord')
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='jinux_bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)

# Setup ConfigParser
config = ConfigParser()
config.read('config.ini')

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

# Current time
currenttime = 0

# Twitch
Twitch_enabled = config.getboolean('Twitch', 'Enabled')
Streamers = config.get('Twitch', 'Users').split(',')
active = list()


async def twitch_live_stream_notify():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
		if Twitch_enabled:
			await asyncio.sleep(config.getint('Twitch', 'Interval'))
			for Streamer in Streamers:
				Stream = v3.streams.by_channel(Streamer)
				if Stream is not None:
					if Streamer not in active:
						await dclient.send_message(dclient.get_channel(str(Channel_ID)), ''''**{0} is now live!**
																			URL: <https://www.twitch.tv/{0}'''.format(
							Streamer))
					active.append(Streamer)
				else:
					if Streamer in active:
						active.remove(Streamer)


dclient.loop.create_task(twitch_live_stream_notify())

# Cleverbot setup
cb = Cleverbot('Jinux')


# Sets up the game status
@dclient.event
async def on_ready():
    await dclient.change_presence(game=discord.Game(name=config.get('Jinux', 'Playing')))
    global currenttime
    currenttime = datetime.now()
    await dclient.send_message(discord.Object(id=Channel_ID), ":raised_hands:")


# Mention function
def get_m(a):
    return '<@{}>'.format(a.author.id)


# Chatter Bot
@dclient.event
async def on_message(msg):
    if msg.content.startswith(Cmd_char):
        global Poll, Poll_question, opt, vts, vtd, Twitch_enabled, Channel_ID, Streamers, active
        cmd = msg.content[1:].split(' ')[0]
        if cmd == 'cat' and config.getboolean('Functions', 'Random_cat'):
            await cat.ex(dclient, msg.channel)
        elif cmd == 'choose' and config.getboolean('Functions', 'Choose'):
            o = msg.content[8:].split(' ')
            await choose.ex(dclient, msg.channel, get_m(msg), o, Cmd_char)
        elif cmd == 'chucknorris' and config.getboolean('Functions', 'Chucknorris'):
            await chucknorris.ex(dclient, msg.channel)
        elif cmd == 'coinflip' and config.getboolean('Functions', 'Coinflip'):
            await coinflip.ex(dclient, msg.channel, get_m(msg))
        elif cmd == 'convert' and config.getboolean('Functions', 'Currency'):
            await convert.ex(dclient, msg.channel, get_m(msg), msg.content[9:].split(' '), Cmd_char)
        elif cmd == 'dice' and config.getboolean('Functions', 'Dice'):
            await dice.ex(dclient, msg.channel, get_m(msg))
        elif cmd == '8ball' and config.getboolean('Functions', '8ball'):
            await eightball.ex(dclient, msg.channel, get_m(msg), msg.content[7:], Cmd_char)
        elif cmd == 'gif' and config.getboolean('Functions', 'Random_gif'):
            await gif.ex(dclient, msg.channel, msg.content[5:], get_m(msg), Cmd_char)
        elif cmd == 'help':
            await bhelp.ex(dclient, msg.author, msg.channel, get_m(msg), msg.content.split(' '), Cmd_char)
        elif cmd == 'info':
            await info.ex(dclient, msg.channel)
        elif cmd == 'poll' and config.getboolean('Functions', 'Poll'):
            Poll, Poll_question, opt, vts, vtd = await poll.ex_poll(dclient, msg.channel, msg.author, get_m(msg),
                                                                    msg.content[6:],
                                                                    Poll, Poll_question, opt, vts, vtd, Cmd_char)
        elif cmd == 'vote' and config.getboolean('Functions', 'Poll'):
            Poll, Poll_question, opt, vts, vtd = await poll.ex_vote(dclient, msg.channel, msg.author, get_m(msg),
                                                                    msg.content[6:],
                                                                    Poll, Poll_question, opt, vts, vtd, Cmd_char)
        elif cmd == 'purge':
            print()
        elif cmd == 'reddit' and config.getboolean('Functions', 'Reddit'):
            await reddit.ex(dclient, msg.author, msg.channel, get_m(msg), msg.content[8:], Cmd_char)
        elif cmd == 'rps' and config.getboolean('Functions', 'Rock_paper_scissors'):
            await rps.ex(dclient, msg.channel, get_m(msg), msg.content[5:], Cmd_char)
        elif cmd == 'temp' and config.getboolean('Functions', 'Temperature'):
            await temp.ex(dclient, msg.channel, get_m(msg), msg.content[6:], Cmd_char)
        elif cmd == 'time' and config.getboolean('Functions', 'Timezone'):
            await time.ex(dclient, msg.channel, get_m(msg), msg.content[6:], Cmd_char)
        elif cmd == 'trans' and config.getboolean('Functions', 'Translate'):
            await trans.ex(dclient, msg.channel, get_m(msg), msg.content[7:], Cmd_char)
        elif cmd == 'twitch' and config.getboolean('Functions', 'Twitch'):
            Twitch_enabled, Channel_ID, Streamers, active = await twitch.ex(dclient, msg.author, msg.channel,
                                                                            get_m(msg), msg.content[8:],
                                                                            Twitch_enabled, Channel_ID, Streamers,
                                                                            active, Cmd_char)
        elif cmd == 'uptime':
            await uptime.ex(dclient, msg.channel, currenttime)
        elif cmd == 'xkcd' and config.getboolean('Functions', 'XKCD'):
            await xkcd.ex(dclient, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'youtube' and config.getboolean('Functions', 'Youtube'):
            await youtube.ex(dclient, msg.channel, get_m(msg), msg.content[9:], Cmd_char)
        elif cmd == 'restart':
            await restart.ex(dclient, msg.channel, get_m(msg), msg.author)
    elif msg.content.startswith('<@{}>'.format(Client_ID)) and config.getboolean('Functions', 'Cleverbot'):
        if int(msg.author.id) != int(Client_ID):
            await dclient.send_message(msg.channel, '{} {}'.format(get_m(msg), cb.ask(msg.content[22:])))
    elif int(msg.author.id) == int(msg.channel.id) and config.getboolean('Functions', 'Cleverbot'):
        await dclient.send_message(msg.channel, '{} {}'.format(get_m(msg), cb.ask(msg.content[22:])))

# Activate Bot
dclient.run(Token_ID)
