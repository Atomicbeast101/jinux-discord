import discord
import sqlite3
from datetime import datetime, timedelta
from time import localtime, strftime


# Count # of letters in money value
def num_letters(v):
    count = 0
    for char in v:
        if char.isalpha():
            count += 1
    return count


# Get the new date from string time/date
def get_date(time):
    now = datetime.now()
    if ',' in time:
        times = time.split(',')
        for t in times:
            val = t
            if 's' in val and num_letters(val) == 1:
                val = val.replace('s', '')
                now += timedelta(seconds=int(val))
            elif 'm' in val and num_letters(val) == 1:
                val = val.replace('m', '')
                now += timedelta(minutes=int(val))
            elif 'h' in val and num_letters(val) == 1:
                val = val.replace('h', '')
                now += timedelta(hours=int(val))
            elif 'd' in val and num_letters(val) == 1:
                val = val.replace('d', '')
                now += timedelta(days=int(val))
            else:
                return -1
    else:
        val = time
        if 's' in val and num_letters(val) == 1:
            val = val.replace('s', '')
            now += timedelta(seconds=int(val))
        elif 'm' in val and num_letters(val) == 1:
            val = val.replace('m', '')
            now += timedelta(minutes=int(val))
        elif 'h' in val and num_letters(val) == 1:
            val = val.replace('h', '')
            now += timedelta(hours=int(val))
        elif 'd' in val and num_letters(val) == 1:
            val = val.replace('d', '')
            now += timedelta(days=int(val))
        else:
            return -1
    return now


# Tempch Command
async def ex(dclient, public_channel, private_channel, mention, a, author, time_limit, channel_name_limit, server, con,
             con_ex, log_file, cmd_char):
    a = a.split(' ')
    if len(a) == 3:
        channel_type = a[0].lower()
        time = a[1].lower()
        channel_name = a[2].lower()
        try:
            if channel_type == 'voice' or channel_type == 'text':
                if channel_type == 'voice':
                    channel_type = discord.ChannelType.voice
                elif channel_type == 'text':
                    channel_type = discord.ChannelType.text
                if 'd' in time or 'h' in time or 'm' in time or 's' in time or ',' in time:
                    date = get_date(time)
                    date_limit = get_date(time_limit)
                    if date != -1 and date_limit != -1:
                        # Prevents from creating temporary channels with time exceeding the time limit set by server
                        # owner
                        if date <= date_limit:
                            if len(channel_name) <= channel_name_limit:
                                new_channel = await dclient.create_channel(server, channel_name, type=channel_type)
                                try:
                                    con_ex.execute("INSERT INTO temp_channel VALUES (?, ?, ?, ?);",
                                                   (new_channel.id, channel_name, author.id,
                                                    date.strftime('%Y-%m-%d %X')))
                                    con.commit()
                                    await dclient.send_message(public_channel,
                                                               '{}, channel created! You can reach it at <#{}>!'
                                                               .format(mention, new_channel.id))
                                except sqlite3.Error as e:
									embed=discord.Embed(title="Error", description="Error when trying to insert data to SQLite.", color=0xff0000)
									embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
									embed.add_field(name="Reason", value=e.args[1], inline=False)
									await dclient.send_message(channel, embed=embed)
                                    return True, 'SQLITE', 'Error when trying to insert data to SQLite. ERROR: {}'.format(e.args[1])
                            else:
                                await dclient.send_message(public_channel,
                                                           '{}, the channel name `{}` is `{}` characters long! It '
                                                           'must be `{}` or less!'.format(mention, channel_name,
                                                                                          len(channel_name),
                                                                                          channel_name_limit))
                        else:
                            await dclient.send_message(public_channel,
                                                       '{}, you cannot exceed the time limit! The time limit is '
                                                       '`{}`.'.format(mention, time_limit))
                    else:
                        await dclient.send_message(public_channel, '{}, the time must be in #time format (ex: 1h or 2h,'
                                                                   '5m).'.format(mention))
                else:
                    await dclient.send_message(public_channel, '{}, the time must be in #time format (ex: 1h or 2h,'
                                                               '5m).'.format(mention))
            else:
                await dclient.send_message(public_channel, '{}, channel type `{}` invalid! You must choose between '
                                                           '`voice` or `text`.'.format(mention, channel_type))
        except discord.Forbidden:
            await dclient.send_message(public_channel, "{}, I don't have access to `manage_channels`! Please notify an "
                                                       "admin!".format(mention))
    elif len(a) == 1:
        if a[0].lower() == 'list':
            try:
                response = '''Remaining Temporary Channels:'''
                for channel in con_ex.execute("SELECT id, date FROM temp_channel;"):
                    channel_id = dclient.get_channel(channel[0]).name
                    if dclient.get_channel(channel[0]).type == discord.ChannelType.text:
                        channel_type = 'text'
                    else:
                        channel_type = 'voice'
                    expire_date = datetime.strptime(channel[1], '%Y-%m-%d %X')
                    diff_date = expire_date - datetime.now()
                    rem_days = diff_date.days
                    if rem_days == 0:
                        rem_time = datetime.strptime(str(expire_date - datetime.now()), "%H:%M:%S.%f")
                        response += '''
    `#{}` - **{}** & time remaining: `{} hours`, `{} minutes`, and `{} seconds`.'''.format(channel_id, channel_type,
                                                                                           rem_time.hour,
                                                                                           rem_time.minute,
                                                                                           rem_time.second)
                    elif rem_days == 1:
                        rem_time = datetime.strptime(str(expire_date - datetime.now()), "%d day, %H:%M:%S.%f")
                        response += '''
    `#{}` - **{}** & time remaining: `{} day`, `{} hours`, `{} minutes`, and `{} seconds`.'''.format(channel_id,
                                                                                                     channel_type,
                                                                                                     rem_days,
                                                                                                     rem_time.hour,
                                                                                                     rem_time.minute,
                                                                                                     rem_time.second)
                    elif rem_days > 1:
                        rem_time = datetime.strptime(str(expire_date - datetime.now()), "%d days, %H:%M:%S.%f")
                        response += '''
    `#{}` - **{}** & time remaining: `{} days`, `{} hours`, `{} minutes`, and `{} seconds`.'''.format(channel_id,
                                                                                                      channel_type,
                                                                                                      rem_days,
                                                                                                      rem_time.hour,
                                                                                                      rem_time.minute,
                                                                                                      rem_time.second)
                await dclient.send_message(private_channel, response)
                await dclient.send_message(public_channel,
                                           '{}, I sent the list in a private message.'.format(mention))
            except sqlite3.Error as e:
				embed=discord.Embed(title="Error", description="Error when trying to retrieve data from SQLite.", color=0xff0000)
				embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
									embed.add_field(name="Reason", value=e.args[1], inline=False)
									await dclient.send_message(channel, embed=embed)
                                    return True, 'SQLITE', 'Error when trying to retrieve data from SQLite. ERROR: {}'.format(e.args[1])
        else:
            await dclient.send_message(public_channel, '{}, **USAGE** {}tempch <voice|text|list> <time> <channel-name>'
                                       .format(mention, cmd_char))
    else:
        await dclient.send_message(public_channel, '{}, **USAGE** {}tempch <voice|text|list> <time> <channel-name>'
                                   .format(mention, cmd_char))
    return False