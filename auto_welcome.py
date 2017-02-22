from datetime import datetime, timedelta

# Auto Welcome
async def wel(c, mbr, ch, m):
    if mbr.joined_at < datetime.now() - timedelta(seconds=10):
        r = ''''''
        file = open('Welcome_Message.txt', 'r')
        for line in file:
            r += line + '''
'''
        file.close()
        r.replace('{USER}', m)
        await c.send_message(c.Object(id=ch), r)
