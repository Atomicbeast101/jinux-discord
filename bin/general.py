from PyDictionary import PyDictionary
from aiohttp import ClientSession
from datetime import datetime
from geopy import geocoders
from bin import data
import random as ran
import discord
import re


# Check if value is an int
def is_int_value(_value):
    try:
        int(_value)
        return True
    except ValueError:
        return False


# Check if value is a float
def is_float_value(_value):
    try:
        float(_value)
        return True
    except ValueError:
        return False


# Check if value is ID # or @user
def is_user_value(_value):
    if re.match('^<@[0-9]{18}>$', _value):  # <@304040086482321408>
        return True
    elif re.match('^[0-9]{18}$', _value):  # 304040086482321408
        return True
    return False


# Get ID from ID # or @user
def get_user_id(_value):
    if re.match('^<@[0-9]{18}>$', _value):  # <@304040086482321408>
        return str(_value[2:-1])
    elif re.match('^[0-9]{18}$', _value):  # 304040086482321408
        return str(_value)
    return -1


def get_name(_dclient, _server, _user_id):
    return discord.utils.get(discord.utils.get(_dclient.servers,
                                               id=_server.id).members,
                             id=_user_id).name


# Construct usage messages
def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


# Gif command
async def gif(_dclient, _channel, _mention, _cmdchar, _msg):
    _msg = _msg.split(' ')
    if len(_msg) > 1:
        _msg.pop(0)
        keywords = ''
        for m in _msg:
            keywords += m + '+'
        async with ClientSession() as cs:
            async with cs.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(_msg)) \
                    as response:
                gif_data = await response.json()
                await _dclient.send_message(_channel, '{}'.format(gif_data['data']['fixed_height_downsampled_url']))
    else:
        await _dclient.send_message(_channel, usage_msg('gif <keywords...>', _mention, _cmdchar))


# Cat command
async def cat(_dclient, _channel):
    async with ClientSession() as cs:
        async with cs.get('http://random.cat/meow') as response:
            cat_data = await response.json()
            await _dclient.send_message(_channel, '{}'.format(cat_data['file']))


# Choose command
async def choose(_dclient, _channel, _mention, _cmdchar, _msg):
    options = _msg.split(' ')
    if len(options) >= 3:
        options.pop(0)
        await _dclient.send_message(_channel, '{} I choose `{}`!'.format(_mention, ran.choice(options)))
    else:
        await _dclient.send_message(_channel, usage_msg('choose <options...>', _mention, _cmdchar))


# Dice command
async def dice(_dclient, _channel, _mention):
    await _dclient.send_message(_channel, '{} *rolls dice...* I got a `{}`!'
                                .format(_mention, ran.choice([1, 2, 3, 4, 5, 6])))


# Dict command (Dictionary)
async def dict(_dclient, _channel, _mention, _cmdchar, _msg):
    _msg = _msg.split(' ')
    if len(_msg) == 2:
        word = _msg[1].lower()
        dict = PyDictionary()
        try:
            result = dict.meaning(word)
            nouns = []
            verbs = []
            adjectives = []
            if 'Noun' in result:
                for i in range(0, 2):
                    nouns.append(result['Noun'][i])
            if 'Verb' in result:
                for i in range(0, 2):
                    verbs.append(result['Verb'][i])
            if 'Adjective' in result:
                for i in range(0, 2):
                    adjectives.append(result['Adjective'][i])

            embed = discord.Embed(title='Dictionary Results', color=0xff5700)
            embed.set_author(name=word)
            embed.set_thumbnail(url='https://i.imgur.com/VCck2RQ.png')
            count = 1
            for noun in nouns:
                embed.add_field(name='{}. {}'.format(count, 'noun'), value=noun, inline=False)
                count += 1
            count = 1
            for verb in verbs:
                embed.add_field(name='{}. {}'.format(count, 'verb'), value=verb, inline=False)
                count += 1
            count = 1
            for adj in adjectives:
                embed.add_field(name='{}. {}'.format(count, 'adjective'), value=adj, inline=False)
                count += 1
            await _dclient.send_message(_channel, embed=embed)
        except Exception:
            await _dclient.send_message(_channel, ':warning: {} There is no meaning for `{}`!'.format(_mention, word))
    else:
        await _dclient.send_message(_channel, usage_msg('dict <word>', _mention, _cmdchar))


# Purge command
async def purge(_dclient, _channel, _mention, _cmdchar, _msg, _author, _server):
    _msg = _msg.split(' ')
    if _channel.permissions_for(_author).administrator:
        if len(_msg) > 1:
            _msg.pop(0)
            if _msg[0].lower() == 'all':
                if len(_msg) == 2:
                    if is_int_value(_msg[1]):
                        try:
                            value = int(_msg[1])
                            msg_list = list()
                            async for msg in _dclient.logs_from(_channel, limit=value):
                                msg_list.append(msg)
                            await _dclient.delete_messages(msg_list)
                            await _dclient.send_message(_channel, '{} `{}` messages purged from this channel!'
                                                        .format(_mention, value))
                        except discord.Forbidden:
                            await _dclient.send_message(_channel, ':warning: {} I don\'t have access to `manage_'
                                                                  'messages`! Please notify an admin!'.format(_mention))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} `{}` must be in numeric value!'
                                                    .format(_mention, _msg[1]))
                else:
                    await _dclient.send_message(_channel, usage_msg('purge all <#>', _mention, _cmdchar))
            elif _msg[0].lower() == 'user':
                if len(_msg) == 3:
                    if is_user_value(_msg[1]):
                        if is_int_value(_msg[2]):
                            try:
                                user_id = get_user_id(_msg[1])
                                value = int(_msg[2])
                                msg_list = list()
                                async for msg in _dclient.logs_from(_channel, limit=value):
                                    if msg.author.id == user_id:
                                        msg_list.append(msg)
                                await _dclient.delete_messages(msg_list)
                                await _dclient.send_message(_channel, '{} `{}` messages from `{}` has been purged from '
                                                                      'this channel!'
                                                            .format(_mention, len(msg_list),
                                                                    get_name(_dclient, _server, user_id)))
                            except discord.Forbidden:
                                await _dclient.send_message(_channel,
                                                            ':warning: {} I don\'t have access to `manage_messages`! '
                                                            'Please notify an admin!'.format(_mention))
                        else:
                            await _dclient.send_message(_channel, ':warning: {} `{}` must be in numeric value!'
                                                        .format(_mention, _msg[1]))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} `{}` must be an ID # or @user value!'
                                                    .format(_mention, _msg[1]))
                else:
                    await _dclient.send_message(_channel, usage_msg('purge user <id> <#>', _mention, _cmdchar))
            elif _msg[0].lower() == 'today':
                try:
                    time = datetime.now().replace(hour=0, minute=0, second=0)
                    msg_list = list()
                    async for msg in _dclient.logs_from(_channel, after=time):
                        msg_list.append(msg)
                    await _dclient.delete_messages(msg_list)
                    await _dclient.send_message(_channel, '{} `{}` messages sent today has been purged from this '
                                                          'channel!'.format(_mention, len(msg_list)))
                except discord.Forbidden:
                    await _dclient.send_message(_channel,
                                                ':warning: {} I don\'t have access to `manage_messages`! Please notify'
                                                ' an admin!'.format(_mention))
            else:
                await _dclient.send_message(_channel, usage_msg('purge <all|user|today>', _mention, _cmdchar))
        else:
            await _dclient.send_message(_channel, usage_msg('purge <all|user|today>', _mention, _cmdchar))
    else:
        await _dclient.send_message(_channel, ':warning: {} You must be an administrator to use this command!'
                                    .format(_mention))


# RPS command
async def rps(_dclient, _channel, _mention, _cmdchar, _msg, _name):
    _msg = _msg.split(' ')
    if len(_msg) > 1:
        _msg.pop(0)
        user_choice = _msg[0].lower()
        if user_choice in ['rock', 'paper', 'scissors']:
            bot_choice = ran.choice(['rock', 'paper', 'scissors'])
            result = data.rps_result['{}_{}'.format(user_choice, bot_choice)]
            if result['type'] == 0:
                await _dclient.send_message(_channel, result['response'].format(ran.choice(data.rps_tie_response)))
            elif result['type'] == 1:
                await _dclient.send_message(_channel, result['response'].format(ran.choice(data.rps_bot_response)))
            else:
                await _dclient.send_message(_channel, result['response'].format(ran.choice(data.rps_player_response)))
        else:
            await _dclient.send_message(_channel, ':warning: {} Please choose an option between `rock`, `paper`, and '
                                                  '`scissors`.'.format(_mention))
    else:
        await _dclient.send_message(_channel, usage_msg('rps <rock|paper|scissors>', _mention, _cmdchar))


# Temp command
async def temp(_dclient, _channel, _mention, _cmdchar, _msg):
    _msg = _msg.split(' ')
    if len(_msg) == 4 and _msg[2].upper() in ['F', 'K', 'C'] and _msg[3].upper() in ['F', 'K', 'C']:
        _msg.pop(0)
        if is_float_value(_msg[0]):
            value = float(_msg[0])
            from_metric = _msg[1].upper()
            to_metric = _msg[2].upper()
            if from_metric != to_metric:
                result = 0
                if from_metric == 'F' and to_metric == 'K':
                    result = (value + 459.67) * (5 / 9)
                elif from_metric == 'F' and to_metric == 'C':
                    result = (value - 32) * .5556
                elif from_metric == 'K' and to_metric == 'F':
                    result = (value * (9 / 5)) - 459.67
                elif from_metric == 'K' and to_metric == 'C':
                    result = (value * (9 / 5)) - 273.15
                elif from_metric == 'C' and to_metric == 'F':
                    result = (value * 1.8) + 32
                elif from_metric == 'C' and to_metric == 'K':
                    result = (value + 273.15) * (5 / 9)
                await _dclient.send_message(_channel, data.temp_response['{}_{}'.format(from_metric, to_metric)]
                                            .format(value, result))
            else:
                await _dclient.send_message(_channel, ':warning: {} You can\'t convert the temperature that way, '
                                                      'silly!'.format(_mention))
        else:
            await _dclient.send_message(_channel, ':warning: {} The temperature value must be in numeric value!'
                                        .format(_mention))
    else:
        await _dclient.send_message(_channel, usage_msg('temp <#> <from F|K|C> <to F|K|C>', _mention, _cmdchar))


# Time command
async def time(_dclient, _channel, _mention, _cmdchar, _msg):
    if len(_msg.split(' ')) > 1:
        _msg = _msg[6:]
        google_api = geocoders.GoogleV3()
        try:
            place, (lat, lng) = google_api.geocode(_msg)
            timezone = google_api.timezone((lat, lng))
            time_now = datetime.now(timezone)
            await _dclient.send_message(_channel, '{} It is `{:%H:%M:%S}` or `{:%I:%M:%S %p}` in `{}` right now.'
                                        .format(_mention, time_now, time_now, _msg))
        except Exception:
            await _dclient.send_message(_channel, '{} Location `{}` unknown! Please try to be more specific. I rely on '
                                                  'Google maps to get coordinates for the timezone!'
                                        .format(_mention, _msg))
    else:
        await _dclient.send_message(_channel, usage_msg('time <location>', _mention, _cmdchar))


# Uptime command
async def uptime(_dclient, _channel, _mention, _uptime_start):
    dtime = datetime.now() - _uptime_start
    days = dtime.days
    if days == 0:
        dtime = datetime.strptime(str(dtime), "%H:%M:%S.%f")
        await _dclient.send_message(_channel, '{} I have been up for `{:d} hours`, `{:d} minutes`, and `{:d} seconds`.'
                                    .format(_mention, dtime.hour, dtime.minute, dtime.second))
    elif days == 1:
        dtime = datetime.strptime(str(dtime), "%d day, %H:%M:%S.%f")
        await _dclient.send_message(_channel, '{} I have been up for `1 day`, `{:d} hours`, `{:d} minutes`, and `{:d} '
                                              'seconds`.'.format(_mention, dtime.hour, dtime.minute, dtime.second))
    else:
        dtime = datetime.strptime(str(dtime), "%d day, %H:%M:%S.%f")
        await _dclient.send_message(_channel, '{} I have been up for `{:d} days`, `{:d} hours`, `{:d} minutes`, and '
                                              '`{:d} seconds`.'
                                    .format(_mention, days, dtime.hour, dtime.minute, dtime.second))
