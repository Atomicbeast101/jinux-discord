# imports
from configparser import ConfigParser
from time import localtime, strftime
from traceback import format_exc
from sys import argv
import discord
import logging

from bin import auto_welcome, data, cat, info, choose, chucknorris, coinflip


# configuration
config = ConfigParser()
config.read('config.ini')

token_id, playing, log_file, sql_file, auto_welcome_file, temp_channel_timelimit, cmd_char = '', '', '', '', '', '', ''
log_enabled, chat_enabled, auto_welcome_enabled, twitch_enabled, temp_channel_enabled = False, False, False, False, False
client_id, channel_id, twitch_interval, twitch_channel_id, temp_channel_charlimit = 0, 0, 0, 0, 0

try:
    # discord TODO check to make sure these values are set in config file
    token_id = config.get('Discord', 'TokenID')
    client_id = config.getint('Discord', 'ClientID')
    channel_id = config.getint('Discord', 'ChannelID')
    playing = config.get('Discord', 'Playing')

    # logging
    log_enabled = config.getboolean('Loging', 'Enabled')
    log_level = config.get('Logging', 'Level')
    if log_level not in data.log_levels:
        print('WARN: Invalid log level input! Using \'error\' instead...')
        log_level = 'error'
    log_file = config.get('Logging', 'DataFile')

    # database
    sql_file = config.get('Database', 'DataFile')

    # chat
    chat_enabled = config.getboolean('Chat', 'Enabled')

    # general
    auto_welcome_enabled = config.getboolean('AutoWelcome', 'Enabled')
    auto_welcome_file = config.get('AutoWelcome', 'DataFile')

    # twitch
    twitch_enabled = config.getboolean('Twitch', 'Enabled')
    twitch_interval = config.getint('Twitch', 'Interval')
    twitch_users = config.get('Twitch', 'Users')
    twitch_channel_id = config.getint('Twitch', 'ChannelID')
    if twitch_channel_id is 0:
        twitch_channel_id = channel_id

    # temporary channel
    temp_channel_enabled = config.getboolean('TemporaryChannel', 'Enabled')
    temp_channel_timelimit = config.get('TemporaryChannel', 'TimeLimit')
    temp_channel_charlimit = config.getint('TemporaryChannel', 'ChannelNameLimit')

    # commands
    cmd_char = config.get('Commands', 'Character')
except Exception:
    print('ERROR: Unable to load values from \'config.ini\' file!')
    print(format_exc())
    exit()


# logging
log = logging.getLogger('Jinux_Discord')
log.disabled = log_enabled
log.setLevel(level=log_level)
handler = logging.FileHandler(filename=log_file,
                              encoding='utf-8',
                              mode='a')
handler.setFormatter('%(asctime)s | %(levelname)6s | %(message)s')
log.addHandler(handler)


# preparing bot
dclient = discord.Client()
cat_obj = cat.Cat()
info_obj = info.Info()
choose_obj = choose.Choose()
chucknorris_obj = chucknorris.ChuckNorris()
coinflip_obj = coinflip.CoinFlip()


# load welcome message
welcome_msg = ''''''
try:
    with open(auto_welcome_file, 'r') as file:
        for line in file:
            welcome_msg += line + '''
    '''
    file.close()
except Exception:
    print('ERROR: Unable to load content from \'{}\' file!'.format(auto_welcome_file))
    print(format_exc())
    exit()


# auto remove bot messages
remove_bot_msgs = []
# TODO


# custom commands
custom_commands = []
# TODO
def get_custom_msg(cmd):
    # TODO
    print()


# functions

# get mention of user
def get_mention(msg):
    return '<@{}>'.format(msg.author.id)

# get name of user
def get_name(msg):
    return discord.utils.get(discord.utils.get(dclient.servers,
                                               id=msg.channel.server.id).members,
                             id=msg.author.id).name

# send embed error msg to user
async def send_error_msg(cmd, msg, reason):
    embed = discord.Embed(title='Error',
                          description=reason,
                          color=0xff0000)
    embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
    await dclient.send_message(msg.channel, embed=embed)
    log.info('Ignoring disabled {}{} command sent by {}.'.format(cmd_char,
                                                                  cmd,
                                                                  get_name(msg)))


# discord events
@dclient.event
async def on_member_join(user):
    auto_welcome.welcome(dclient, user, welcome_msg)

@dclient.event
async def on_message(msg):
    if msg.content.startswith(cmd_char) and not msg.channel.is_private:
        cmd = msg.content[1:].split(' ')[0]
        log.debug('{} executed {}{} command.'.format(get_name(msg), cmd_char, cmd))
        if cmd in data.commands:

            # checks if command is enabled
            if data.commands[cmd] is not 'NONE':
                if not config.getboolean('Commands', data.commands[cmd]):
                    send_error_msg(cmd, msg, 'Command {}{} is currently disabled!'.format(cmd_char, cmd))
                    return

            # log command executions
            log.info('Executing {}{} command for {}.'.format(cmd_char, cmd, get_name(msg)))

            # execute command
            if cmd == 'cat':
                await cat_obj.get_pic(log, dclient, msg)
            elif cmd == 'channelinfo':
                await info_obj.get_channel(log, dclient, msg)
            elif cmd == 'choose':
                await choose_obj.decide(log, dclient, msg, cmd_char)
            elif cmd == 'chucknorris':
                await chucknorris_obj.get_joke(log, dclient, msg)
            elif cmd == 'coinflip':
                await coinflip_obj.flip_coin(log, dclient, msg)
            elif cmd == 'conspiracy':
                await conspiracy_obj.get_content(log, dclient, msg)
            elif cmd == 'custcmd':
                await custcmd_obj.manage(log, dclient, msg, cmd_char)
            elif cmd == 'convert':
                await convert_obj.convert_cash(log, dclient, msg, cmd_char)
            elif cmd == 'dice':
                await dice_obj.roll(log, dclient, msg)
            elif cmd == '8ball':
                await eball_obj.predict(log, dclient, msg, cmd_char)
            elif cmd == 'gif':
                await gif_obj.get_meme(log, dclient, msg, cmd_char)
            elif cmd == 'google':
                await google_obj.search(log, dclient, msg, cmd_char)
            elif cmd == 'help':
                await help_obj.just_help(log, dclient, msg, cmd_char)
            elif cmd == 'info':
                await info_obj.get_info(log, dclient, msg)
            elif cmd == 'poll':
                await poll_obj.manage(log, dclient, msg, cmd_char)
            elif cmd == 'purge':
                await purge_obj.nuke(log, dclient, msg, cmd_char)
            elif cmd == 'vote':
                await poll_obj.vote(log, dclient, msg, cmd_char)
            elif cmd == 'reddit':
                await reddit_obj.get_feed(log, dclient, msg, cmd_char)
            elif cmd == 'remindme':
                await remind_obj.remind_me(log, dclient, msg, cmd_char)
            elif cmd == 'remindall':
                await remind_obj.remind_all(log, dclient, msg, cmd_char)
            elif cmd == 'rps':
                await rps_obj.play(log, dclient, msg, cmd_char)
            elif cmd == 'serverinfo':
                await info_obj.get_server(log, dclient, msg)
            elif cmd == 'temp':
                await temp_obj.convert(log, dclient, msg, cmd_char)
            elif cmd == 'tempch':
                await tempch_obj.manage(log, dclient, msg, cmd_char)
            elif cmd == 'time':
                await time_obj.get(log, dclient, msg, cmd_char)
            elif cmd == 'trans':
                await trans_obj.translate(log, dclient, msg, cmd_char)
            elif cmd == 'twitch':
                await twitch_obj.manage(log, dclient, msg, cmd_char)
            elif cmd == 'uptime':
                await uptime_obj.get(log, dclient, msg)
            elif cmd == 'xkcd':
                await xkcd_obj.get(log, dclient, msg, cmd_char)
            elif cmd == 'youtube':
                await youtube_obj.search(log, dclient, msg, cmd_char)

            # custom commands
            elif cmd in custom_commands:
                await dclient.send_message(msg.channel, get_custom_msg(cmd))

    # bot chat
    elif msg.content.startswith('<@{}>'.format(client_id)) and chat_enabled:
        if int(msg.author.id) != int(client_id):
            await dclient.send_message(msg.channel, '{}, COMING SOON!'.format(get_mention(msg)))

    # notice me senpai
    elif 'notice me senpai' in msg.content.lower():
        await dclient.send_message(msg.channel, 'I notice you, {}!'.format(get_mention(msg)))


# start bot
# TODO background tasks here
dclient.run(token_id)
