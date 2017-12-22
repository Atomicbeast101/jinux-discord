from datetime import datetime, timedelta


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


class Reminders:
    def __init__(self, _db, _db_ex):
        self.db = _db
        self.db_ex = _db_ex

    async def me(self, _dclient, _channel, _mention, _cmdchar, _msg, _author):
        _msg = _msg.split(' ')
        if len(_msg) >= 3:
            _msg.pop(0)
            time = _msg[0].lower()
            msg = ''
            for i in range(1, len(_msg)):
                msg += _msg[i] + ' '
            if 'd' or 'h' or 'm' or 's' or ',' in time:
                send_remind = get_date(time)
                self.db_ex.execute('INSERT INTO reminder (send_remind, owner, loc_id, channel_user, message) VALUES '
                                   '(?, ?, ?, \'U\', ?);', (send_remind.strftime('%Y-%m-%d %X'), _author.id, _author.id,
                                                            msg))
                self.db.commit()
                await _dclient.send_message(_channel, ':loudspeaker: {} Will send you reminder!'.format(_mention))
            else:
                await _dclient.send_message(_channel, ':warning: {} Time must be in correct format! Example: 1 hour = '
                                                      '1h, 10 hours & 5 minutes = 10h,5m'.format(_mention))
        else:
            await _dclient.send_message(_channel, usage_msg('remindme <time> <message...>', _mention, _cmdchar))

    async def all(self, _dclient, _channel, _mention, _cmdchar, _msg, _author):
        _msg = _msg.split(' ')
        if len(_msg) >= 3:
            _msg.pop(0)
            time = _msg[0].lower()
            msg = ''
            for i in range(1, len(_msg)):
                msg += _msg[i] + ' '
            if 'd' or 'h' or 'm' or 's' or ',' in time:
                send_remind = get_date(time)
                self.db_ex.execute('INSERT INTO reminder (send_remind, owner, loc_id, channel_user, message) VALUES '
                                   '(?, ?, ?, \'C\', ?);', (send_remind.strftime('%Y-%m-%d %X'), _author.id,
                                                            _channel.id, msg))
                self.db.commit()
                await _dclient.send_message(_channel, ':loudspeaker: {} Will send you reminder!'.format(_mention))
            else:
                await _dclient.send_message(_channel, ':warning: {} Time must be in correct format! Example: 1 hour = '
                                                      '1h, 10 hours & 5 minutes = 10h,5m'.format(_mention))
        else:
            await _dclient.send_message(_channel, usage_msg('remindme <time> <message...>', _mention, _cmdchar))
