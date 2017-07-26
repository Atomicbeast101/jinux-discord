from configparser import ConfigParser
from time import localtime, strftime
from datetime import datetime
import random as r
import asyncio
import discord
import sqlite3
import aiohttp

from cmds import (bhelp, cat, channelinfo, choose, chucknorris, coinflip, convert, conspiracy, dice, dictionary,
                  eightball, gif, info, poll, purge, reddit, remindme, rps, serverinfo, temp, tempch, custom_cmd, time,
                  trans, twitch, uptime, xkcd, youtube)
from Data import CMD_LIST, CMD_CONFIG
import auto_welcome


# Setup ConfigParser
config = ConfigParser()
config.read('config.ini')


# Setup Logging
log_file = open('jinux.log', 'a')
LOG_FORMAT = '[{}]: {^6} - {}{}'

def log(typ, reason):
    print(LOG_FORMAT.format(strftime("%b %d, %Y %X", localtime()), typ, reason, ''))
    try:
        if config.getboolean('Jinux', 'Logging'):
            log_file.write(LOG_FORMAT.format(strftime("%b %d, %Y %X", localtime()), typ, reason, '\n'))
    except IOError as e:
        print(LOG_FORMAT.format(strftime("%b %d, %Y %X", localtime()), 'LOGGER', 'Unable to store logs to file! ERROR: {}'.format(e.args[1], '')))


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
    conspiracy_list.append(consp.rstrip())


# RemindMe/All database setup
con = sqlite3.connect(config.get('Jinux', 'Data_File'))
con_ex = con.cursor()
try:
    con_ex.execute('''CREATE TABLE IF NOT EXISTS reminder (
                      id INTEGER PRIMARY KEY,
                      type CHAR(1) NOT NULL,
                      channel CHAR(10) NOT NULL,
                      message TEXT NOT NULL,
                      date DATETIME NOT NULL);''')
    con.commit()
except sqlite3.Error as e:
    log('SQLITE', 'Error when trying to setup table for remindme/all: {}'.format(e.args[1]))

async def check_remindme():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
        try:
            for reminders in con_ex.execute("SELECT * FROM reminder WHERE date <= Datetime('{}');".format(
                    datetime.now().strftime('%Y-%m-%d %X'))):
                if reminders[1] == '0':  # ME type
                    user = discord.User(id=reminders[2])
                    await dclient.send_message(user, '{}'.format(reminders[3]))
                    con_ex.execute('DELETE FROM reminder WHERE id={};'.format(reminders[0]))
                    con.commit()
                    log('REMIND', 'Removed ID {} from database.'.format(reminders[0]))
                elif reminders[1] == '1':  # ALL type
                    user = dclient.get_channel(reminders[2])
                    await dclient.send_message(user, '{}'.format(reminders[3]))
                    con_ex.execute('DELETE FROM reminder WHERE id={};'.format(reminders[0]))
                    con.commit()
                    log('REMIND', 'Removed ID {} from database.'.format(reminders[0]))
        except sqlite3.Error as e:
            log('SQLITE', 'Error when trying to select/delete data: {}'.format(e.args[1]))
        await asyncio.sleep(1)


# Custom cmd setup
cmd_list = list()
try:
    con_ex.execute('''CREATE TABLE IF NOT EXISTS custom_cmd (
                      cmd VARCHAR(10) PRIMARY KEY,
                      message TEXT NOT NULL);''')
    con.commit()
except sqlite3.Error as e:
    log('SQLITE', 'Error when trying to setup table for mottos: {}'.format(e.args[1]))

try:
    for row in con_ex.execute("SELECT cmd FROM custom_cmd;"):
        cmd_list.append(row[0])
    cmd_list.extend(CMD_LIST)
except sqlite3.Error as e:
    log('SQLITE', 'Error when trying to select information from the table: {}'.format(e.args[1]))

def get_custom_cmd_msg(cmd):
    try:
        for cmd_msg in con_ex.execute("SELECT message FROM custom_cmd WHERE cmd='{}'".format(cmd)):
            return cmd_msg[0]
    except sqlite3.Error as e:
        log('SQLITE', 'Error when trying to select information from the table: {}'.format(e.args[1]))


# Twitch setup
twitch_enabled = config.getboolean('Twitch', 'Enabled')
twitch_timelimit = config.getint('Twitch', 'Interval')
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
        if twitch_enabled and len(streamers) > 0:
            for streamer in streamers:
				try:
					async with aiohttp.ClientSession() as s:
						async with s.get('https://api.twitch.tv/kraken/streams/{}?client_id=ygyhel3k6oyrq17gg4ame28uffxsxp'
										 'gzddma'.format(streamer)) as raw_data:
							data = await raw_data.json()
							try:
								if data['stream'] is not None:
									if streamer not in active:
										await dclient.send_message(dclient.get_channel(str(twitch_channel)),
																   "**{0}** is now live! @<https://www.twitch.tv/{0}>".format(
																	   streamer))
										log('TWITCH', 'Announced that player {} is streaming on Twitch.'.format(streamer))
										active.append(streamer)
									else:
										if streamer in active:
											active.remove(streamer)
							except KeyError:
								if streamer in active:
									active.remove(streamer)
				except Exception as e:
                    log('TWITCH', 'Error when trying to retrieve data from Twitchs API server: {}'.format(e.args[1]))
        await asyncio.sleep(twitch_timelimit)


# Temporary Channel Setup
time_limit = config.get('Temporary_Channel', 'Time_Limit')
channel_name_limit = config.getint('Temporary_Channel', 'Channel_Name_Limit')
try:
    con_ex.execute('''CREATE TABLE IF NOT EXISTS temp_channel (
                      id VARCHAR(10) PRIMARY KEY,
                      name VARCHAR(255) NOT NULL,
                      owner VARCHAR(10) NOT NULL,
                      date DATETIME NOT NULL);''')
    con.commit()
except sqlite3.Error as e:
    log('SQLITE', 'Error when trying to setup table for tempch: {}'.format(e.args[1]))

async def temp_channel_timeout():
    await dclient.wait_until_ready()
    while not dclient.is_closed:
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
        except sqlite3.Error as e:
            log('SQLITE', 'Error when trying to select/delete data: {}'.format(e.args[1]))
        await asyncio.sleep(1)


# Auto remove temporary channel from database if an admin force removes it from the server
@dclient.event
async def on_channel_delete(channel):
    try:
        con_ex.execute('SELECT id FROM temp_channel WHERE id={};'.format(channel.id))
        ch_info = con_ex.fetchone()[0]
        con_ex.execute('DELETE FROM temp_channel WHERE id={};'.format(ch_info))
        con.commit()
        log('TEMP_CHANNEL', 'Removed ID {} from database.'.format(ch_info))
    except sqlite3.Error as e:
        log('SQLITE', 'Error when trying to select/delete data: {}'.format(e.args[1]))


# Reply messages for users who talk to Jinux
replies_list = list()
replies = open('replies.txt', 'r')
for reply in replies:
    replies_list.append(reply.rstrip())


# Auto remove Jinux's messages
bot_messages = list()
message_expiration = config.get('Bot_Messages', 'Expiration')
async def clear_bot_messages():
    for bot_msg in bot_messages:
        if bot_msg.is_passed_time(message_expiration):
            dclient.delete_message(bot_msg.get_msg())


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
file = open('welcome_message.txt', 'r')
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
        if cmd in CMD_LIST:
            # checks if command is enabled
            if CMD_LIST[cmd] is not 'NONE':
                if not config.getboolean('Functions', CMD_CONFIG[cmd]):
                    embed=discord.Embed(title="Error", description="Command {}{} is currently disabled!".format(cmd_char, cmd), color=0xff0000)
                    embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
                    embed.add_field(name="Reason", value=ex, inline=False)
                    await dclient.send_message(msg.channel, embed=embed)
                    log('COMMAND', 'Ignoring {}{} command sent by {} because it\'s currently disabled.'.format(cmd_char, cmd, get_name(msg)))
                    return
                
            # log command execution
            log('COMMAND', 'Executing {}{} command for {}.'.format(cmd_char, cmd, get_name(msg)))

            # execute built-in commands
            if cmd == 'cat':
                to_log, error_type, error_msg = await cat.ex(dclient, msg.channel)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'channelinfo':
                await channelinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
            elif cmd == 'choose':
                await choose.ex(dclient, msg.channel, get_mention(msg), msg.content[8:], cmd_char)
            elif cmd == 'chucknorris':
                to_log, error_type, error_msg = await chucknorris.ex(dclient, msg.channel)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'coinflip':
                await coinflip.ex(dclient, msg.channel, get_mention(msg))
            elif cmd == 'conspiracy':
                await conspiracy.ex(dclient, msg.channel, conspiracy_list)
            elif cmd == 'custcmd':
                to_log, error_type, error_msg, cmd_list = await custom_cmd.ex(dclient, msg.channel, get_mention(msg), msg.author, msg.content[9:],
                                        cmd_list, con, con_ex, log_file, cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'convert':
                to_log, error_type, error_msg = await convert.ex(dclient, msg.channel, get_mention(msg), msg.content[9:].split(' '), cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'dice':
                await dice.ex(dclient, msg.channel, get_mention(msg))
            elif cmd == '8ball':
                to_log, error_type, error_msg = await eightball.ex(dclient, msg.channel, get_mention(msg), msg.content[7:], cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'gif':
                to_log, error_type, error_msg = await gif.ex(dclient, msg.channel, msg.content[5:], get_mention(msg), cmd_char)

            elif cmd == 'help':
                await bhelp.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content.split(' '), cmd_char)
            elif cmd == 'info':
                await info.ex(dclient, msg.channel)
            elif cmd == 'poll':
                poll_enable, poll_question, options, votes, voted = await poll.ex_poll(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted, cmd_char)
            elif cmd == 'purge':
                await purge.ex(dclient, msg.channel, msg.author, get_mention(msg), msg.content[7:], cmd_char)
            elif cmd == 'vote':
                poll_enable, poll_question, options, votes, voted = await poll.ex_vote(dclient, msg.channel, msg.author,
                                                                                   get_mention(msg), msg.content[6:],
                                                                                   poll_enable, poll_question, options,
                                                                                   votes, voted)
            elif cmd == 'reddit':
                await reddit.ex(dclient, msg.author, msg.channel, get_mention(msg), msg.content[8:])
            elif cmd == 'remindme':
                to_log, error_type, error_msg = await remindme.ex_me(dclient, msg.channel, get_mention(msg), con, con_ex, msg.author.id, msg.content[10:],
                                 log_file, cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'remindall':
                to_log, error_type, error_msg = await remindme.ex_all(dclient, msg.channel, get_mention(msg), con, con_ex, msg.channel.id, msg.content[11:],
                                 log_file, cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'rps':
                await rps.ex(dclient, msg.channel, get_mention(msg), msg.content[5:], cmd_char)
            elif cmd == 'serverinfo':
                await serverinfo.ex(dclient, msg.author, msg.channel, get_mention(msg))
            elif cmd == 'temp':
                await temp.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
            elif cmd == 'tempch':
                to_log, error_type, error_msg = await tempch.ex(dclient, msg.channel, msg.author, get_mention(msg), msg.content[8:], msg.author, time_limit,
                            channel_name_limit, msg.channel.server, con, con_ex, log_file, cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'time':
                await time.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
            elif cmd == 'trans':
                await trans.ex(dclient, msg.channel, get_mention(msg), msg.content[7:], cmd_char)
            elif cmd == 'twitch':
                twitch_enabled, Channel_ID, streamers, active = await twitch.ex(
                    dclient, msg.author, msg.channel, get_mention(msg), msg.content[8:], twitch_enabled, twitch_channel,
                    streamers, active, cmd_char)
            elif cmd == 'uptime':
                await uptime.ex(dclient, msg.channel, start_time)
            elif cmd == 'xkcd':
                to_log, error_type, error_msg = await xkcd.ex(dclient, msg.channel, get_mention(msg), msg.content[6:], cmd_char)
                if to_log:
                    log(error_type, error_msg)
            elif cmd == 'youtube':
                to_log, error_type, error_msg = await youtube.ex(dclient, msg.channel, get_mention(msg), msg.content[9:], cmd_char)
                if to_log:
                    log(error_type, error_msg)
            
            # execute custom commands
            elif cmd in cmd_list:
                await dclient.send_message(msg.channel, get_custom_cmd_msg(cmd))

    # bot autoreply      
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
