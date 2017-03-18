from datetime import datetime, timedelta

# Auto Welcome
async def welcome(dclient, member, channel, mention):
    if member.joined_at < datetime.now() - timedelta(seconds=10):
        r = ''''''
        file = open('Welcome_Message.txt', 'r')
        for line in file:
            r += line + '''
'''
        file.close()
        r.replace('{USER}', mention)
        await dclient.send_message(dclient.Object(id=channel), r)
