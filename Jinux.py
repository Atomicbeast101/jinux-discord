import asyncio
from configparser import ConfigParser
from datetime import datetime
from time import localtime, strftime

import discord
import sqlite3
import random as r
from twitch.api import v3

from cmds import (bhelp, cat, channelinfo, choose, chucknorris, coinflip, convert, conspiracy, dice, dictionary,
                  eightball, gif, info, likebill, poll, purge, reddit, remindme, rps, serverinfo, temp, tempch,
                  custom_cmd, time, trans, twitch, uptime, xkcd, youtube)
import auto_welcome


# Setup ConfigParser
config = ConfigParser()
config.read('config.ini')

# Setup Logging
log_file = open('jinux.log', 'a')
if config.getboolean('Jinux', 'Logging'):
    def log(typ, reason):
        print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), typ, reason))
        log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), typ, reason))

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

# Conspiracy setup
conspiracy_list = list()
conspiracies = open('conspiracies.txt', 'r')
for consp in conspiracies:
    conspiracy_list.append(consp.encode('utf-8').rstrip()[2:-1])

# RemindMe/All database setup
con = sqlite3.connect(config.get('Jinux', 'Data_File'))
con_ex = con.cursor()
try:
    con_ex.execute("CREATE TABLE IF NOT EXISTS reminder ("
                   "id INTEGER PRIMARY KEY,"
                   "type CHAR(1) NOT NULL,"
                   "channel CHAR(10) NOT NULL,"
                   "message TEXT NOT NULL,"
                   "date DATETIME NOT NULL);")
    con.commit()
except sqlite3.Error as e:
    print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                 'Error when trying to setup table for remindme/all: ' + e.args[0]))
    log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                            'Error when trying to setup table for remindme/all: ' + e.args[0]))
async def check_remindme():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
        await asyncio.sleep(1)
        try:
            for reminders in con_ex.execute("SELECT * FROM reminder WHERE date <= Datetime('{}');".format(
                    datetime.now().strftime('%Y-%m-%d %X'))):
                if reminders[1] == '0':  # ME type
                    user = discord.User(id=reminders[2])
                    await dclient.send_message(user, '{}'.format(reminders[3]))
                    con_ex.execute('DELETE FROM reminder WHERE id={};'.format(reminders[0]))
                    con.commit()
                    log('REMINDER', 'Removed ID {} from database.'.format(reminders[0]))
                elif reminders[1] == '1':  # ALL type
                    user = dclient.get_channel(reminders[2])
                    await dclient.send_message(user, '{}'.format(reminders[3]))
                    con_ex.execute('DELETE FROM reminder WHERE id={};'.format(reminders[0]))
                    con.commit()
                    log('REMINDER', 'Removed ID {} from database.'.format(reminders[0]))
        except sqlite3.Error as ex:
            print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                         'Error when trying to select/delete data: ' + ex.args[0]))
            log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                    'Error when trying to insert/delete data: ' + ex.args[0]))


# Custom cmd setup
cmd_list = list()
try:
    con_ex.execute("CREATE TABLE IF NOT EXISTS custom_cmd ("
                   "cmd VARCHAR(10) PRIMARY KEY,"
                   "message TEXT NOT NULL);")
    con.commit()
except sqlite3.Error as e:
    print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                 'Error when trying to setup table for mottos: ' + e.args[0]))
    log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                            'Error when trying to setup table for mottos: ' + e.args[0]))
try:
    for row in con_ex.execute("SELECT cmd FROM custom_cmd;"):
        cmd_list.append(row[0])
    cmd_list.extend(['cat', 'channelinfo', 'choose', 'chucknorris', 'coinflip', 'convert', 'conspiracy', 'custcmd',
                     'dice', 'dictionary', '8ball', 'gif', 'help', 'info', 'poll', 'purge', 'vote', 'reddit',
                     'remindme', 'remindall', 'rps', 'serverinfo', 'temp', 'time', 'trans', 'twitch', 'xkcd',
                     'youtube'])
except sqlite3.Error as e:
    print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                 'Error when trying to select information from the table: ' + e.args[0]))
    log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                            'Error when trying to select information from the table: ' + e.args[0]))


def get_custom_cmd_msg(cmd):
    try:
        for cmd_msg in con_ex.execute("SELECT message FROM custom_cmd WHERE cmd='{}'".format(cmd)):
            return cmd_msg[0]
    except sqlite3.Error as e1:
        print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                     'Error when trying to select information from the table: ' + e1.args[0]))
        log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                'Error when trying to select information from the table: ' +
                                                e1.args[0]))


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
        if twitch_enabled and len(streamers) > 0:
            for streamer in streamers:
                stream = v3.streams.by_channel(streamer)
                if stream['stream'] is not None:
                    if streamer not in active:
                        await dclient.send_message(dclient.get_channel(str(twitch_channel)),
                                                   "**{0}** is now live! @<https://www.twitch.tv/{0}>".format(streamer))
                    log('TWITCH', 'Announced that player {} is streaming on Twitch.'.format(streamer))
                    active.append(streamer)
                else:
                    if streamer in active:
                        active.remove(streamer)


# Temporary Channel Setup
time_limit = config.get('Temporary_Channel', 'Time_Limit')
channel_name_limit = config.getint('Temporary_Channel', 'Channel_Name_Limit')
try:
    con_ex.execute("CREATE TABLE IF NOT EXISTS temp_channel ("
                   "id VARCHAR(10) PRIMARY KEY,"
                   "name VARCHAR(255) NOT NULL,"
                   "owner VARCHAR(10) NOT NULL,"
                   "date DATETIME NOT NULL);")
    con.commit()
except sqlite3.Error as e:
    print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                 'Error when trying to setup table for tempch: ' + e.args[0]))
    log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                            'Error when trying to setup table for tempch: ' + e.args[0]))
async def temp_channel_timeout():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
        await asyncio.sleep(1)
        try:
            for channel in con_ex.execute("SELECT * FROM temp_channel WHERE date <= Datetime('{}');".format(
                    datetime.now().strftime('%Y-%m-%d %X'))):
                remove_channel = dclient.get_channel(channel[0])
                channel_name = channel[1]
                owner = discord.User(id=channel[2])
                await dclient.delete_channel(remove_channel)
                con_ex.execute('DELETE FROM temp_channel WHERE id={};'.format(channel[0]))
                con.commit()
                await dclient.send_message(owner, 'Channel `{}` has expired and has been removed!'.format(channel_name))
                log('TEMP_CHANNEL', 'Removed ID {} from database.'.format(channel[0]))
        except sqlite3.Error as ex:
            print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                         'Error when trying to select/delete data: ' + ex.args[0]))
            log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                    'Error when trying to insert/delete data: ' + ex.args[0]))


# Auto remove temporary channel from database if an admin force removes it from the server
@dclient.event
async def on_channel_delete(channel):
    try:
        con_ex.execute('SELECT * FROM temp_channel WHERE id={};'.format(channel.id))
        ch_info = con_ex.fetchone()[0]
        remove_channel = ch_info[0]
        channel_name = ch_info[1]
        owner = discord.User(id=ch_info[2])
        await dclient.delete_channel(remove_channel)
        con_ex.execute('DELETE FROM temp_channel WHERE id={};'.format(ch_info[0]))
        con.commit()
        await dclient.send_message(owner, 'Channel `{}` has been force removed by an admin!'.format(channel_name))
        log('TEMP_CHANNEL', 'Removed ID {} from database.'.format(channel[0]))
    except sqlite3.Error as ex:
        print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                     'Error when trying to select/delete data: ' + ex.args[0]))
        log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                'Error when trying to insert/delete data: ' + ex.args[0]))


# Reply messages for users who talk to Jinux
replies_list = list()
replies = open('replies.txt', 'r')
for reply in replies:
    replies_list.append(reply.encode('utf-8').rstrip()[2:-1])


# Sets up the game status
@dclient.event
async def on_ready():
    log('BOOTUP', 'Starting up Jinux system...')
    await dclient.change_presence(game=discord.Game(name=config.get('Jinux', 'Playing')))
    global start_time
    start_time = datetime.now()
    # Notifies that Jinux has successfully connected to the Discord server
    if Channel_ID != 0:
        await dclient.send_message(discord.Object(id=Channel_ID), ":wave:")
    log('BOOTUP', 'Finished starting up Jinux system!')


# Auto welcome new members
welcome_msg = ''''''
file = open('Welcome_Message.txt', 'r')
for line in file:
    welcome_msg += line + '''
'''
file.close()


@dclient.event
async def on_member_join(member):
    if config.getboolean('Jinux', 'Auto_Welcome'):
        await auto_welcome.welcome(dclient, member, '<@{}>'.format(member.id), welcome_msg)


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
    if msg.content.startswith(cmd_char) and not msg.channel.is_private:
        global poll_enable, poll_question, options, votes, voted, twitch_enabled, Channel_ID, streamers, active, \
            twitch_channel, cmd_list, chat_limit
        cmd = msg.content[1:].split(' ')[0]
        if cmd == 'cat' and config.getboolean('Functions', 'Random_cat'):
            log('COMMAND', 'Executing {}cat command for {}.'.format(cmd_char, get_name(msg)))
            await cat.ex(dclient, msg.channel)
        elif cmd == 'channelinfo' and config.getboolean('Functions', 'ChannelInfo'):
            log('COMMAND', 'Executing {}channelinfo command for {}.'.format(cmd_char, get_name(msg)))
            await channelinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
        elif cmd == 'choose' and config.getboolean('Functions', 'Choose'):
            log('COMMAND', 'Executing {}choose command for {}.'.format(cmd_char, get_name(msg)))
            await choose.ex(dclient, msg.channel, get_mention(msg), msg.content[8:], cmd_char)
        elif cmd == 'chucknorris' and config.getboolean('Functions', 'Chucknorris'):
            log('COMMAND', 'Executing {}chucknorris command for {}.'.format(cmd_char, get_name(msg)))
            await chucknorris.ex(dclient, msg.channel)
        elif cmd == 'coinflip' and config.getboolean('Functions', 'Coinflip'):
            log('COMMAND', 'Executing {}coinflip command for {}.'.format(cmd_char, get_name(msg)))
            await coinflip.ex(dclient, msg.channel, get_mention(msg))
        elif cmd == 'convert' and config.getboolean('Functions', 'Currency'):
            log('COMMAND', 'Executing {}convert command for {}.'.format(cmd_char, get_name(msg)))
            await convert.ex(dclient, msg.channel, get_mention(msg), msg.content[9:].split(' '), cmd_char)
        elif cmd == 'conspiracy' and config.getboolean('Functions', 'Conspiracy'):
            log('COMMAND', 'Executing {}conspiracy command for {}.'.format(cmd_char, get_name(msg)))
            await conspiracy.ex(dclient, msg.channel, conspiracy_list)
        elif cmd == 'custcmd' and config.getboolean('Functions', 'Custom_Cmd'):
            log('COMMAND', 'Executing {}custcmd command for {}.'.format(cmd_char, get_name(msg)))
            cmd_list = await custom_cmd.ex(dclient, msg.channel, get_mention(msg), msg.author, msg.content[9:],
                                           cmd_list, con, con_ex, log_file, cmd_char)
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
        elif cmd == 'likebill':
            log('COMMAND', 'Executing {}likebill command for {}.'.format(cmd_char, get_name(msg)))
            await likebill.ex(dclient, msg.channel)
        elif cmd == 'poll' and config.getboolean('Functions', 'poll'):
            log('COMMAND', 'Executing {}poll command for {}.'.format(cmd_char, get_name(msg)))
            poll_enable, poll_question, options, votes, voted = await poll.ex_poll(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted, cmd_char)
        elif cmd == 'purge' and config.getboolean('Functions', 'Purge'):
            log('COMMAND', 'Executing {}purge command for {}.'.format(cmd_char, get_name(msg)))
            await purge.ex(dclient, msg.channel, msg.author, get_mention(msg), msg.content[7:], cmd_char)
        elif cmd == 'vote' and config.getboolean('Functions', 'poll'):
            log('COMMAND', 'Executing {}vote command for {}.'.format(cmd_char, get_name(msg)))
            poll_enable, poll_question, options, votes, voted = await poll.ex_vote(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted)
        elif cmd == 'reddit' and config.getboolean('Functions', 'Reddit'):
            log('COMMAND', 'Executing {}reddit command for {}.'.format(cmd_char, get_name(msg)))
            await reddit.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content[8:])
        elif cmd == 'remindme' and config.getboolean('Functions', 'Remind_Me_All'):
            log('COMMAND', 'Executing {}remindme command for {}.'.format(cmd_char, get_name(msg)))
            await remindme.ex_me(dclient, msg.channel, get_mention(msg), con, con_ex, msg.author.id, msg.content[10:],
                                 log_file, cmd_char)
        elif cmd == 'remindall' and config.getboolean('Functions', 'Remind_Me_All'):
            log('COMMAND', 'Executing {}remindall command for {}.'.format(cmd_char, get_name(msg)))
            await remindme.ex_all(dclient, msg.channel, get_mention(msg), con, con_ex, msg.channel.id, msg.content[11:],
                                 log_file, cmd_char)
        elif cmd == 'rps' and config.getboolean('Functions', 'Rock_Paper_Scissors'):
            log('COMMAND', 'Executing {}rps command for {}.'.format(cmd_char, get_name(msg)))
            await rps.ex(dclient, msg.channel, get_mention(msg), msg.content[5:], cmd_char)
        elif cmd == 'serverinfo' and config.getboolean('Functions', 'ServerInfo'):
            log('COMMAND', 'Executing {}serverinfo command for {}.'.format(cmd_char, get_name(msg)))
            await serverinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
        elif cmd == 'temp' and config.getboolean('Functions', 'Temperature'):
            log('COMMAND', 'Executing {}temp command for {}.'.format(cmd_char, get_name(msg)))
            await temp.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
        elif cmd == 'tempch' and config.getboolean('Temporary_Channel', 'Enabled'):
            log('COMMAND', 'Executing {}tempch command for {}.'.format(cmd_char, get_name(msg)))
            await tempch.ex(dclient, msg.channel, msg.author, get_mention(msg), msg.content[8:], msg.author, time_limit,
                            channel_name_limit, msg.channel.server, con, con_ex, log_file, cmd_char)
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
        elif cmd == 'uptime':
            log('COMMAND', 'Executing {}uptime command for {}.'.format(cmd_char, get_name(msg)))
            await uptime.ex(dclient, msg.channel, start_time)
        elif cmd == 'xkcd' and config.getboolean('Functions', 'XKCD'):
            log('COMMAND', 'Executing {}xkcd command for {}.'.format(cmd_char, get_name(msg)))
            await xkcd.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
        elif cmd == 'youtube' and config.getboolean('Functions', 'Youtube'):
            log('COMMAND', 'Executing {}youtube command for {}.'.format(cmd_char, get_name(msg)))
            await youtube.ex(dclient, msg.channel, get_mention(msg), msg.content[9:], cmd_char)
        elif cmd in cmd_list:
            await dclient.send_message(msg.channel, get_custom_cmd_msg(cmd))
    elif msg.content.startswith('<@{}>'.format(Client_ID)) and config.getboolean('Functions', 'Chatting') \
            and Client_ID != 0:
        if int(msg.author.id) != int(Client_ID):
            await dclient.send_message(msg.channel, '{}, {}'.format(get_mention(msg), r.choice(replies_list)))


# Execute Twitch Loop
if twitch_enabled:
    dclient.loop.create_task(twitch_live_stream_notify())

# Execute RemindMe/All Loop
if config.getboolean('Functions', 'Remind_Me_All'):
    dclient.loop.create_task(check_remindme())

# Execute Temporary Channel Loop
if config.getboolean('Temporary_Channel', 'Enabled'):
    dclient.loop.create_task(temp_channel_timeout())

# Activate Bot
dclient.run(Token_ID)
