import discord
import sqlite3
from datetime import datetime, timedelta
from time import localtime, strftime


# Get the new date from string time/date
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


# Tempch Command
async def ex(dclient, channel, mention, a, author, time_limit, channel_name_limit, server, con, con_ex, log_file,
             cmd_char):
    a = a.split(' ')
    if len(a) == 3:
        channel_type = a[0].lower()
        time = a[1].lower()
        channel_name = a[2].lower()
        try:
            if channel_type == 'voice' or channel_type == 'text':
                if channel_type is 'voice':
                    channel_type = discord.ChannelType.voice
                elif channel_type is 'text':
                    channel_type = discord.ChannelType.text
                if 'd' in time or 'h' in time or 'm' in time or 's' in time or ',' in time:
                    date = get_date(time)
                    date_limit = get_date(time_limit)
                    # Prevents from creating temporary channels with time exceeding the time limit set by server owner
                    if date <= date_limit:
                        if len(channel_name) <= channel_name_limit:
                            new_channel = await dclient.create_channel(server, channel_name, type=channel_type)
                            try:
                                con_ex.execute("INSERT INTO temp_channel VALUES (?, ?, ?, ?);",
                                               (new_channel.id, channel_name, author.id, date.strftime('%Y-%m-%d %X')))
                                con.commit()
                                await dclient.send_message(channel, '{}, channel created! You can reach it at <#{}>!'
                                                           .format(mention, new_channel.id))
                            except sqlite3.Error as e:
                                await dclient.send_message(channel,
                                                           '{}, error when trying to add info to database! Please'
                                                           ' notifiy the admins!'.format(mention))
                                print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                             'Error when trying to insert data: ' + e.args[0]))
                                log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                                        'Error when trying to insert data: ' +
                                                                        e.args[0]))
                        else:
                            await dclient.send_message(channel, '{}, the channel name `{}` is `{}` characters long! It '
                                                                'must be `{}` or less!'.format(mention, channel_name,
                                                                                               len(channel_name),
                                                                                               channel_name_limit))
                    else:
                        await dclient.send_message(channel, '{}, you cannot exceed the time limit! The time limit is '
                                                            '`{}`.'.format(mention, time_limit))
                else:
                    await dclient.send_message(channel, '{}, the time must be in #time format (ex: 1h or 2h,5m).'
                                               .format(mention))
            else:
                await dclient.send_message(channel, '{}, channel type `{}` invalid! You must choose between `voice` or '
                                                    '`text`.'.format(mention, channel_type))
        except discord.Forbidden:
            await dclient.send_message(channel, "{}, I don't have access to `manage_channels`! Please notify an "
                                                "admin!".format(mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE** {}tempch <voice-or-text> <time> <channel-name>'
                                   .format(mention, cmd_char))