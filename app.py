# imports
from bin import data, general, poll, fake_help
from datetime import datetime, timedelta
from bin.MusicPlayer import MusicPlayer
from configparser import ConfigParser
from bin.temp_channel import TempCh
from bin.reminders import Reminders
from bin.custom_cmd import CustCmd
from traceback import format_exc
from bin.xkcd import XKCD
import asyncio
import logging
import discord
import sqlite3
import os

# PACKAGES: discord.py geopy pytube configparser asyncio pynacl youtube_dl bs4 pydictionary
# YUM/APT PACKAGES: ffmpeg


# Config variables
gen_tokenid = ''
gen_channelid = 0
gen_playing = ''
gen_welcomemessage = ''
gen_cmdchar = ''

log_disabled = True
log_level = ''
log_filename = ''

dat_datafile = ''

mus_enabled = False
mus_textchannelid = 0
mus_voicechannelid = 0
mus_playlistnamecharlimit = 0

tch_enabled = False
tch_timelimit = ''
tch_channelnamecharlimit = 0

aut_enabled = False
aut_filename = ''

cf_enabled = False
cf_filename = ''

cus_enabled = False
cus_cmdcharlimit = ''
config = ConfigParser()
dirPath = os.path.dirname(os.path.realpath(__file__))
config.read(dirPath + '/config.ini')
try:
    # General
    gen_userid = config.get('General', 'UserID')
    gen_tokenid = config.get('General', 'TokenID')
    gen_channelid = config.getint('General', 'ChannelID')
    gen_playing = config.get('General', 'Playing')
    gen_welcomemessage = config.get('General', 'WelcomeMessage')
    gen_cmdchar = config.get('General', 'CommandCharacter')

    # Log
    log_disabled = config.getboolean('Log', 'Disabled')
    log_level = config.get('Log', 'Level')
    log_filename = config.get('Log', 'FileName')

    # Data
    dat_datafile = config.get('Data', 'DataFile')

    # Music
    mus_enabled = config.getboolean('Music', 'Enabled')
    mus_textchannelid = config.get('Music', 'TextChannelID')
    mus_voicechannelid = config.get('Music', 'VoiceChannelID')
    mus_playlistnamecharlimit = config.getint('Music', 'PlaylistNameCharLimit')

    # TemporaryChannel
    tch_enabled = config.getboolean('TemporaryChannel', 'Enabled')
    tch_timelimit = config.get('TemporaryChannel', 'TimeLimit')
    tch_channelnamecharlimit = config.getint('TemporaryChannel', 'ChannelNameCharLimit')

    # AutoWelcome
    aut_enabled = config.getboolean('AutoWelcome', 'Enabled')
    aut_filename = config.get('AutoWelcome', 'FileName')

    # ChatFilter
    cf_enabled = config.getboolean('ChatFilter', 'Enabled')
    cf_filename = config.get('ChatFilter', 'Filename')

    # CustomCommands
    cus_enabled = config.getboolean('CustomCommands', 'Enabled')
    cus_cmdcharlimit = config.getint('CustomCommands', 'CommandCharacterLimit')
except Exception:
    print('ERROR: Unable to load values from \'config.ini\' file!\n{}'.format(format_exc()))
    exit()

# Prepare Jinux bot
dclient = discord.Client()


def get_name(msg):
    return discord.utils.get(discord.utils.get(dclient.servers,
                                               id=msg.channel.server.id).members,
                             id=msg.author.id).name


def get_mention(msg):
    return '<@{}>'.format(msg.author.id)


# Setup logging
log = logging.getLogger(__name__)
log.disabled = log_disabled
if log_level in ['INFO', 'ERROR']:
    log.setLevel(level=log_level)
else:
    log.setLevel(level='INFO')
log_format = logging.Formatter('%(asctime)s | %(levelname)6s | %(message)s')
log_format.datefmt = '%a, %d %b %Y %H:%M:%S'
file_handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='a')
file_handler.setFormatter(log_format)
log.addHandler(file_handler)

# Load database file
db = sqlite3.connect(dat_datafile)
db_ex = db.cursor()
try:
    db_ex.execute("CREATE TABLE IF NOT EXISTS reminder ("
                  "id INTEGER PRIMARY KEY,"
                  "send_remind DATETIME NOT NULL,"
                  "owner VARCHAR(18) NOT NULL,"
                  "loc_id VARCHAR(18) NOT NULL,"
                  "channel_user CHAR(1) NOT NULL,"
                  "message VARCHAR(200) NOT NULL);")
    db_ex.execute("CREATE TABLE IF NOT EXISTS custom_cmd ("
                  "command VARCHAR(20) PRIMARY KEY,"
                  "owner VARCHAR(18) NOT NULL,"
                  "message VARCHAR(200) NOT NULL);")
    db_ex.execute("CREATE TABLE IF NOT EXISTS temp_channel ("
                  "name VARCHAR(25) PRIMARY KEY,"
                  "id VARCHAR(18) NOT NULL,"
                  "type CHAR(1) NOT NULL,"
                  "owner VARCHAR(18) NOT NULL,"
                  "expiration_date DATETIME NOT NULL);")
    db_ex.execute("CREATE TABLE IF NOT EXISTS song ("
                  "youtube_id VARCHAR(20) PRIMARY KEY,"
                  "name VARCHAR(100) NOT NULL);")
    db_ex.execute("CREATE TABLE IF NOT EXISTS playlist ("
                  "name VARCHAR(50) PRIMARY KEY,"
                  "owner VARCHAR(18) NOT NULL);")
    db_ex.execute("CREATE TABLE IF NOT EXISTS playlist_song ("
                  "name VARCHAR(50) NOT NULL,"
                  "youtube_id VARCHAR(20) NOT NULL,"
                  "PRIMARY KEY (name, youtube_id),"
                  "FOREIGN KEY (name) REFERENCES playlist(song),"
                  "FOREIGN KEY (youtube_id) REFERENCES song(youtube_id));")
    db.commit()
except sqlite3.Error:
    print('ERROR: Unable to load SQLite database \'{}\' file!\n{}'.format(dat_datafile, format_exc()))
    exit()

# Load music system
music_player = MusicPlayer()


def song_status(_song_enddattime, _duration, _title):
    diff = _duration - (_song_enddattime - datetime.now()).seconds
    diff_min, diff_sec = divmod(diff, 60)
    dur_min, dur_sec = divmod(_duration, 60)
    return '''**Now Playing:** 
```markdown
[{}:{:02}/{}:{:02}]: {}
```'''.format(diff_min, diff_sec, dur_min, dur_sec, _title)


async def play_music():
    global music_player
    await dclient.wait_until_ready()
    while True:
        await music_player.auto_switch_song()
        await asyncio.sleep(0.1)


# Load TemporaryChannel
async def sync_tempch():
    await dclient.wait_until_ready()
    while True:
        try:
            for row in db_ex.execute('SELECT name, id, owner FROM temp_channel WHERE expiration_date <= Datetime(?);',
                                     (datetime.now().strftime('%Y-%m-%d %X'), )):
                channel_name = row[0]
                channel_id = row[1]
                owner = discord.User(id=row[2])
                await dclient.delete_channel(dclient.get_channel(id=channel_id))
                db_ex.execute('DELETE FROM temp_channel WHERE name=?;', (channel_name, ))
                db.commit()
                await dclient.send_message(owner, 'Temporary channel `{}` has expired and been removed!'
                                           .format(channel_name))
                log.info('Removed temporary channel {} from the database.'.format(channel_name))
        except sqlite3.Error:
            log.error('Unable to sync temporary channels from the database!\n{}'.format(format_exc()))
        await asyncio.sleep(1)


@dclient.event
async def on_channel_delete(channel):
    try:
        for row in db_ex.execute('SELECT id FROM temp_channel WHERE id=?;', (channel.id, )):
            db_ex.execute('DELETE FROM temp_channel WHERE id=?;', (channel.id,))
            db.commit()
            if db_ex.rowcount > 0:
                log.info(
                    'Removed temporary channel ID {} from the database on channel_delete event.'.format(channel.id))
            break
    except sqlite3.Error:
        log.error('Unable to remove temporary channel from the database on channel_delete event!\n{}'
                  .format(format_exc()))


# Load AutoWelcome
if aut_enabled:
    welcome_msg = ''''''
    try:
        with open(aut_filename, 'r') as file:
            for line in file:
                welcome_msg += line + '''
'''
        file.close()
    except FileNotFoundError:
        print('ERROR: Unable to load \'{}\' file!\n{}'.format(aut_filename, format_exc()))
        exit()


@dclient.event
async def on_member_join(user):
    if aut_enabled:
        if user.joined_at < datetime.now() - timedelta(seconds=10):
            await dclient.send_message(user, welcome_msg.replace('{USER}', get_name(user)))


# Load ChatFilter
word_blacklist = list()
if cf_enabled:
    try:
        with open(cf_filename, 'r') as file:
            for line in file:
                word_blacklist.append(line.rstrip())
    except FileNotFoundError:
        print('ERROR: Unable to load \'{}\' file!\n{}'.format(aut_filename, format_exc()))
        exit()


# Load Uptime
uptime_start = None


# Load CustomCommands
custom_commands = list()


def load_custom_commands():
    global custom_commands
    custom_commands = list()
    if cus_enabled:
        try:
            for row in db_ex.execute('SELECT command FROM custom_cmd;'):
                custom_commands.append(row[0])
            log.info('List of custom commands has been loaded from the database!')
        except sqlite3.Error:
            log.error('Unable to load list of custom commands from the database!\n{}'.format(format_exc()))


def get_custom_cmd_result(_cmd, _mention):
    try:
        message = ''
        for row in db_ex.execute('SELECT message FROM custom_cmd WHERE command=?;', (_cmd, )):
            message = row[0]
            break
        log.info('Loaded message for {} custom command from the database!'.format(_cmd))
        return message
    except sqlite3.Error:
        log.error('Unable to load message for {} custom command from the database!\n{}'.format(_cmd, format_exc()))
        return ':warning: {} Unable to load message for `{}` custom command! Please notify an admin.'.format(_mention,
                                                                                                             _cmd)


# Load remindme/remindall system
async def check_reminders():
    await dclient.wait_until_ready()
    while True:
        try:
            for row in db_ex.execute('SELECT id, loc_id, channel_user, message FROM reminder WHERE send_remind <= '
                                     'Datetime(?);', (datetime.now().strftime('%Y-%m-%d %X'), )):
                if row[2] == 'C':  # remindall
                    reminder_id = row[0]
                    channel = dclient.get_channel(row[1])
                    message = row[3]
                    await dclient.send_message(channel, message)
                    db_ex.execute('DELETE FROM reminder WHERE id=?;', (reminder_id, ))
                    db.commit()
                    log.info('Reminder ID {} has been removed from the database!'.format(reminder_id))
                else:  # remindme
                    reminder_id = row[0]
                    user = discord.User(id=row[1])
                    message = row[3]
                    await dclient.send_message(user, message)
                    db_ex.execute('DELETE FROM reminder WHERE id=?;', (reminder_id, ))
                    db.commit()
                    log.info('Reminder ID {} has been removed from the database!'.format(reminder_id))
        except sqlite3.Error:
            log.error('Unable to load reminders from the database!\n{}'.format(format_exc()))
        await asyncio.sleep(1)


# On ready event
@dclient.event
async def on_ready():
    global music_player

    log.info('BOOT: Getting Jinux ready...')
    await dclient.change_presence(game=discord.Game(name=gen_playing))

    # uptime data
    global uptime_start
    uptime_start = datetime.now()

    # bot's welcome message
    if gen_channelid != 0:
        await dclient.send_message(discord.Object(id=gen_channelid), gen_welcomemessage)

    # load music system
    log.info('BOOT: Loading music system...')
    try:
        text_channel = dclient.get_channel(mus_textchannelid)
        voice_channel = dclient.get_channel(mus_voicechannelid)
        if text_channel and voice_channel is not None:
            if await music_player.set(dclient, text_channel, voice_channel, mus_playlistnamecharlimit, gen_cmdchar,
                                      db, db_ex):
                log.info('BOOT: Connected to voice channel!')
            else:
                log.error('ERROR: Unable to join voice channel!')
                exit()
        else:
            log.error('ERROR: Channel ID for text/voice for music system is invalid!')
            exit()
    except Exception:
        print('ERROR: Unable to load channels for music player!\n{}'.format(format_exc()))
        exit()
    log.info('BOOT: Successfully loaded music system!')
    log.info('BOOT: Jinux is ready!')
    load_custom_commands()


# Load needed objects
poll_system = poll.Poll()
xkcd = XKCD()
tempch = TempCh(db, db_ex, tch_timelimit, tch_channelnamecharlimit)
remind = Reminders(db, db_ex)
cust_cmd = CustCmd(db, db_ex)


# Manage commands
@dclient.event
async def on_message(msg):
    if msg.content.startswith(gen_cmdchar) and not msg.channel.is_private and msg.author.id != gen_userid:
        cmd = msg.content[1:].split(' ')[0]
        log.info('Command {}{} executed by {}.'.format(gen_cmdchar, cmd, get_name(msg)))
        try:
            if data.commands.get(cmd) is not None:
                # Validates if command is enabled
                if not config.getboolean(data.commands[cmd]['title'], data.commands[cmd]['value']):
                    await dclient.send_message(msg.channel, ':warning: <@{}>, this command is currently disabled!'
                                               .format(msg.author.id))
                    log.info('User {} tried to execute command {}{} but it is disabled!'.format(get_name(msg),
                                                                                                gen_cmdchar,
                                                                                                cmd))
                else:
                    await dclient.send_typing(msg.channel)
                    # Execute the command

                    # Music related commands
                    if cmd in ['play', 'playing', 'pause', 'stop', 'shuffle', 'queue', 'clear', 'skip', 'playlist',
                               'volume']:
                        global music_player
                        if msg.channel.id == mus_textchannelid:
                            if cmd == 'play':
                                await music_player.play(msg.content, get_mention(msg))
                            elif cmd == 'playing':
                                await music_player.play_status(get_mention(msg))
                            elif cmd == 'pause':
                                await music_player.pause(get_mention(msg))
                            elif cmd == 'stop':
                                await music_player.stop(get_mention(msg))
                            elif cmd == 'shuffle':
                                await music_player.shuffle(get_mention(msg))
                            elif cmd == 'queue':
                                await music_player.queue(msg.content, get_mention(msg))
                            elif cmd == 'clear':
                                await music_player.clear()
                            elif cmd == 'skip':
                                await music_player.skip(get_mention(msg))
                            elif cmd == 'playlist':
                                await music_player.playlist(msg.content, get_mention(msg), msg.author)
                            elif cmd == 'volume':
                                await music_player.volume(msg.content, get_mention(msg))
                        else:
                            await dclient.send_message(msg.channel, ':warning: {} You can only do it in <#{}> channel!'
                                                       .format(get_mention(msg), mus_textchannelid))

                    # General commands
                    elif cmd == 'gif':
                        await general.gif(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'cat':
                        await general.cat(dclient, msg.channel)
                    elif cmd == 'choose':
                        await general.choose(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'dice':
                        await general.dice(dclient, msg.channel, get_mention(msg))
                    elif cmd == 'dict':
                        await general.dict(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'purge':
                        await general.purge(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                            msg.author, msg.channel.server)
                    elif cmd == 'rps':
                        await general.rps(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                          get_name(msg))
                    elif cmd == 'temp':
                        await general.temp(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'time':
                        await general.time(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'uptime':
                        await general.uptime(dclient, msg.channel, get_mention(msg), uptime_start)

                    # Poll commands
                    elif cmd == 'poll':
                        await poll_system.poll(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content)
                    elif cmd == 'vote':
                        await poll_system.vote(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                               msg.author)

                    # Custom commands
                    elif cmd == 'custcmd':
                        await cust_cmd.execute(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                               msg.author, custom_commands, cus_cmdcharlimit)
                        load_custom_commands()

                    # Reminder commands
                    elif cmd == 'remindme':
                        await remind.me(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                        msg.author)
                    elif cmd == 'remindall':
                        await remind.all(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                         msg.author)

                    # Temporary channel commands
                    elif cmd == 'tempch':
                        await tempch.execute(dclient, msg.channel, msg.channel.server, get_mention(msg), gen_cmdchar,
                                             msg.content, msg.author)

                    # XKCD commands
                    elif cmd == 'xkcd':
                        await xkcd.execute(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content[6:])

                    # Help command
                    elif cmd == 'help':
                        await fake_help.execute(dclient, msg.channel, get_mention(msg), gen_cmdchar, msg.content,
                                                msg.author)
            elif cmd in custom_commands:
                await dclient.send_message(msg.channel, get_custom_cmd_result(cmd, get_mention(msg)))
            else:
                await dclient.send_message(msg.channel, ':warning: {} Command `{}{}` is unknown! Please try again.'
                                           .format(get_mention(msg), gen_cmdchar, cmd))
        except Exception:
            await dclient.send_message(msg.channel, ':warning: {} Unable to execute command! Please notify an '
                                                    'admin.'.format(get_mention(msg)))
            log.error('Unable to execute command {}{}!\n{}'.format(gen_cmdchar, cmd, format_exc()))
    
    # Chat filtering system
    elif not msg.channel.is_private and msg.author.id != gen_userid:
        trigger = False
        for word in word_blacklist:
            if word in msg.content.lower():
                trigger = True
                break
        if trigger:
            if not msg.channel.permissions_for(msg.author).administrator:
                await dclient.send_message(msg.channel, ':warning: {} Watch what you\'re saying, bud. You can\'t use'
                                                        ' that word!'.format(get_mention(msg)))
                await dclient.delete_message(msg)

# Start loops
if mus_enabled:
    dclient.loop.create_task(play_music())
if tch_enabled:
    dclient.loop.create_task(sync_tempch())
dclient.loop.create_task(check_reminders())

# Activate the bot
dclient.run(gen_tokenid)
