from datetime import datetime, timedelta


# Uptime command
async def ex(dclient, channel, starttime):
    ut = datetime.now() - starttime

    utd = ut.days

    if ut.days == 0:
        ut = datetime.strptime(str(datetime.now() - starttime), "%H:%M:%S.%f")
        await dclient.send_message(channel,
                                   'I have been up for `{:d} hours`, `{:d} minutes`, and `{:d} seconds`.'.format(
                                       ut.hour, ut.minute, ut.second))
    elif ut.days == 1:
        ut = datetime.strptime(str(datetime.now() - starttime), "%d day, %H:%M:%S.%f")
        await dclient.send_message(channel,
                                   'I have been up for `{:d} day`, `{:d} hours`, `{:d} minutes`, and `{:d} seconds`.'.format(
                                       utd, ut.hour, ut.minute, ut.second))
    elif ut.days > 1:
        try:
            ut = datetime.strptime(str(datetime.now() - starttime), "%d days, %H:%M:%S.%f")
            await dclient.send_message(channel,
                                       'I have been up for `{:d} days`, `{:d} hours`, `{:d} minutes`, and `{:d} seconds`.'.format(
                                           utd, ut.hour, ut.minute, ut.second))
        except ValueError:
            await dclient.send_message(channel, 'I have been up for `{:d} days`'.format(utd))
