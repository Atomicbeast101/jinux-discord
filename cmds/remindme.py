from datetime import datetime, timedelta
from time import localtime, strftime
import sqlite3


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


# RemindMe command
async def ex_me(dclient, channel, mention, con, con_ex, author_id, a, log_file, cmd_char):
    a = a.split(' ')
    if len(a) >= 2:
        time = a[0].lower()
        msg = ''
        for i in range(1, len(a)):
            msg += a[i] + ' '
        if 'd' in time or 'h' in time or 'm' in time or 's' in time or ',' in time:
            date = get_date(time)
            try:
                con_ex.execute("INSERT INTO reminder (type, channel, message, date) VALUES ('0', ?, ?, ?);",
                               (author_id, msg, date.strftime('%Y-%m-%d %X')))
                con.commit()
                await dclient.send_message(channel, '{}, will remind you.'.format(mention))
            except sqlite3.Error as e:
                embed=discord.Embed(title="Error", description="Error when trying to insert data to SQLite.", color=0xff0000)
                embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
                embed.add_field(name="Reason", value=e.args[1], inline=False)
                await dclient.send_message(channel, embed=embed)
                return True, 'SQLITE', 'Error when trying to insert data to SQLite. ERROR: {}'.format(e.args[1])
        else:
            await dclient.send_message(channel, '{}, the time must be in #time format (ex: 1h or 2h,5m).'
                                       .format(mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}remindme <time> <message...>'.format(mention, cmd_char))
    return False


# RemindAll command
async def ex_all(dclient, channel, mention, con, con_ex, channel_id, a, log_file, cmd_char):
    a = a.split(' ')
    if len(a) >= 2:
        time = a[0].lower()
        msg = ''
        for i in range(1, len(a)):
            msg += a[i] + ' '
        if 'd' in time or 'h' in time or 'm' in time or 's' in time or ',' in time:
            date = get_date(time)
            try:
                con_ex.execute("INSERT INTO reminder (type, channel, message, date) VALUES ('1', ?, ?, ?);",
                               (channel_id, msg, str(date)))
                con.commit()
                await dclient.send_message(channel, '{}, will remind you.'.format(mention))
            except sqlite3.Error as e:
                embed=discord.Embed(title="Error", description="Error when trying to insert data to SQLite.", color=0xff0000)
                embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
                embed.add_field(name="Reason", value=e.args[1], inline=False)
                await dclient.send_message(channel, embed=embed)
                return True, 'SQLITE', 'Error when trying to insert data to SQLite. ERROR: {}'.format(e.args[1])
        else:
            await dclient.send_message(channel, '{}, The time must be in #time format (ex: 1h or 2h,5m).'
                                       .format(mention, cmd_char))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}remindall <time> <message...>'.format(mention, cmd_char))
    return False
