from datetime import datetime, timedelta
from time import localtime, strftime


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


class Old_Message:
    def __init__(self, _msg, _limit):
        self.msg = _msg
        self.expire_timestamp = get_date(_limit)
    
    def get_msg(self):
        return msg

    def is_passed_time(self):
        if datetime.now() >= self.expire_timestamp:
            return True
        return False
