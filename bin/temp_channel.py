from datetime import datetime, timedelta
import discord


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


def get_date(time):
    now = datetime.now()
    if ',' in time:
        times = time.split(',')
        for t in times:
            val = t
            if 's' in val:
                val = val.replace('s', '')
                now += timedelta(seconds=int(val))
            elif 'm' in val:
                val = val.replace('m', '')
                now += timedelta(minutes=int(val))
            elif 'h' in val:
                val = val.replace('h', '')
                now += timedelta(hours=int(val))
            elif 'd' in val:
                val = val.replace('d', '')
                now += timedelta(days=int(val))
    else:
        val = time
        if 's' in val:
            val = val.replace('s', '')
            now += timedelta(seconds=int(val))
        elif 'm' in val:
            val = val.replace('m', '')
            now += timedelta(minutes=int(val))
        elif 'h' in val:
            val = val.replace('h', '')
            now += timedelta(hours=int(val))
        elif 'd' in val:
            val = val.replace('d', '')
            now += timedelta(days=int(val))
    return now


def load_channel_names(_db_ex):
    _channels = []
    for row in _db_ex.execute('SELECT name FROM temp_channel;'):
        _channels.append(row[0])
    return _channels


class TempCh:
    def __init__(self, _db, _db_ex, _tch_timelimit, _tch_channelnamelimit):
        self.db = _db
        self.db_ex = _db_ex
        self.tch_timelimit = _tch_timelimit
        self.tch_channelnamelimit = _tch_channelnamelimit
        self.channels = load_channel_names(self.db_ex)

    async def execute(self, _dclient, _channel, _server, _mention, _cmdchar, _msg, _author):
        _msg = _msg.split(' ')
        if len(_msg) > 1:
            _msg.pop(0)
            if _msg[0].lower() == 'create':
                if len(_msg) == 4:
                    ch_type = _msg[1].lower()
                    time = _msg[2].lower()
                    name = _msg[3].lower()
                    if ch_type in ['voice', 'text']:
                        if ch_type == 'voice':
                            ch_type = discord.ChannelType.voice
                            db_ch_type = 'V'
                        else:
                            ch_type = discord.ChannelType.text
                            db_ch_type = 'T'
                        if 'd' or 'h' or 'm' or 's' or ',' in time:
                            expiration_date = get_date(time)
                            date_limit = get_date(self.tch_timelimit)
                            if expiration_date <= date_limit:
                                if len(name) > 25:
                                    await _dclient.send_message(_channel,
                                                                ':warning: {} Temporary channel name `{}` cannot be '
                                                                'more than `25` characters long!'.format(_mention,
                                                                                                         name))
                                else:
                                    if len(name) > self.tch_channelnamelimit:
                                        await _dclient.send_message(_channel,
                                                                    ':warning: {} Temporary channel name `{}` cannot be'
                                                                    ' more than `{}` characters long!'
                                                                    .format(_mention, name, self.tch_channelnamelimit))
                                    else:
                                        if name in self.channels:
                                            await _dclient.send_message(_channel, ':warning: {} Temporary channel name '
                                                                                  '`{}` already exists!'
                                                                        .format(_mention, name))
                                        else:
                                            new_channel = await _dclient.create_channel(_server, name, type=ch_type)
                                            self.db_ex.execute('INSERT INTO temp_channel VALUES (?, ?, ?, ?, ?);',
                                                               (name, new_channel.id, db_ch_type, _author.id,
                                                                expiration_date.strftime('%Y-%m-%d %X')))
                                            self.db.commit()
                                            await _dclient.send_message(_channel, '{} Temporary channel <#{}> created!'
                                                                        .format(_mention, new_channel.id))
                                            self.channels = load_channel_names(self.db_ex)
                            else:
                                await _dclient.send_message(_channel, ':warning: {} You cannot go over the time limit! '
                                                                      'The limit is `{} days`, `{} hours`, `{} minutes`'
                                                                      ', and `[] seconds`.'
                                                            .format(_mention, date_limit.day, date_limit.hour,
                                                                    date_limit.minute, date_limit.second))
                        else:
                            await _dclient.send_message(_channel, ':warning: {} Time must be in correct format! '
                                                                  'Example: 1 hour = 1h, 10 hours & 5 minutes = 10h,5m'
                                                        .format(_mention))
                    else:
                        await _dclient.send_message(_channel, usage_msg('tempch create <voice|text> <time> <name>',
                                                                        _mention, _cmdchar))
                else:
                    await _dclient.send_message(_channel, usage_msg('tempch create <voice|text> <time> <name>',
                                                                    _mention, _cmdchar))
            elif _msg[0].lower() == 'remove':
                if len(_msg) == 2:
                    name = _msg[1].lower()
                    if name in self.channels:
                        channel_id = 0
                        owner_id = 0
                        for row in self.db_ex.execute('SELECT id, owner FROM temp_channel WHERE name=?;', name):
                            channel_id = row[0]
                            owner_id = row[1]
                            break
                        if _author.id == owner_id or _channel.permissions_for(_author).administrator:
                            await _dclient.delete_channel(channel_id)
                            self.db_ex.execute('DELETE FROM temp_channel WHERE name=?;', name)
                            self.db.commit()
                            await _dclient.send_message(_channel, '{} Temporary channel `{}` has been removed!'
                                                        .format(_mention, name))
                            self.channels = load_channel_names(self.db_ex)
                        else:
                            await _dclient.send_message(_channel, ':warning: {} You do not own this command!'
                                                        .format(_mention))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Temporary channel `{}` doesn\'t exist!'
                                                    .format(_mention, name))
                else:
                    await _dclient.send_message(_channel, usage_msg('tempch remove <name>',
                                                                    _mention, _cmdchar))
            elif _msg[0].lower() == 'list':
                channels = {}
                for row in self.db_ex.execute('SELECT name, id, expiration_date FROM temp_channel;'):
                    channels[row[0]]['id'] = row[1]
                    channels[row[0]]['expiration'] = row[2]
                    if _dclient.get_channel(row[1]).type == discord.ChannelType.text:
                        channels[row[0]]['type'] = 'text'
                    else:
                        channels[row[0]]['type'] = 'voice'
                response = '''**Active Temporary Channels:**
'''
                for name in channels:
                    diff = channels[name]['expiration'] - datetime.now()
                    days = diff.days
                    if days == 0:
                        diff = datetime.strptime(str(channels[name]['expiration'] - datetime.now()), '%H:%M:%S.%f')
                        response += '''#{:25} - **{:5}** Expires in: `{:2} hours`, `{:2} minutes`, and `{:2} seconds`.
'''.format(name, channels[name]['type'], diff.hour, diff.minute, diff.second)
                    elif days == 1:
                        diff = datetime.strptime(str(channels[name]['expiration'] - datetime.now()),
                                                 '%d day, %H:%M:%S.%f')
                        response += '#{:25} - **{:5}** Expires in: `{:2} day`, `{:2} hours`, `{:2} minutes`, and ' \
                                    '`{:2} seconds`.\n'.format(name, channels[name]['type'], 1, diff.hour, diff.minute,
                                                               diff.second)
                    else:
                        diff = datetime.strptime(str(channels[name]['expiration'] - datetime.now()),
                                                 '%d days, %H:%M:%S.%f')
                        response += '#{:25} - **{:5}** Expires in: `{:2} days`, `{:2} hours`, `{:2} minutes`, and ' \
                                    '`{:2} seconds`.\n'.format(name, channels[name]['type'], days, diff.hour,
                                                               diff.minute, diff.second)
                await _dclient.send_message(_channel, response)
            else:
                await _dclient.send_message(_channel, usage_msg('tempch <create|remove|list>', _mention, _cmdchar))
        else:
            await _dclient.send_message(_channel, usage_msg('tempch <create|remove|list>', _mention, _cmdchar))
