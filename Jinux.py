import discord
from cmds import cat, choose, chucknorris, coinflip, convert, eightball, gif, bhelp, info, poll, reddit, rps, temp, \
    time, trans, uptime, xkcd, youtube, restart
from configparser import ConfigParser
from cleverbot import Cleverbot
from datetime import datetime

# Load configuration values
config = ConfigParser()
config.read('config.ini')

# Fetch config data and turn it into objects
TOKEN_ID = config.get('Jinux', 'Token')
CMD_CHAR = config.get('Jinux', 'Character')
CLIENT_ID = config.get('Jinux', 'Client_ID')

# Preparing the bot
c = discord.Client()

# Poll system variables
pll = False
q = ""
opt = []
vts = []
vtd = []

# Current time
ct = 0

# Cleverbot setup
cb = Cleverbot('Jinux')


# Sets up the game status
@c.event
async def on_ready():
    await c.change_presence(game=discord.Game(name=config.get('Jinux', 'Playing')))
    global ct
    ct = datetime.now()


# Mention function
def get_m(a):
    return '<@{}>'.format(a.author.id)


# Chatter Bot
@c.event
async def on_message(msg):
    if msg.content.startswith(CMD_CHAR):
        global pll, q, opt, vts, vtd
        cmd = msg.content[1:].split(' ')[0]
        if cmd == 'cat' and config.getboolean('Functions', 'Random_cat'):
            await cat.ex(c, msg.channel)
        elif cmd == 'choose' and config.getboolean('Functions', 'Choose'):
            o = msg.content[8:].split(' ')
            await choose.ex(c, msg.channel, get_m(msg), o, CMD_CHAR)
        elif cmd == 'chucknorris' and config.getboolean('Functions', 'Chucknorris'):
            await chucknorris.ex(c, msg.channel)
        elif cmd == 'coinflip' and config.getboolean('Functions', 'Coinflip'):
            await coinflip.ex(c, msg.channel, get_m(msg))
        elif cmd == 'convert' and config.getboolean('Functions', 'Currency'):
            await convert.ex(c, msg.channel, get_m(msg), msg.content[9:].split(' '), CMD_CHAR)
        elif cmd == 'dice' and config.getboolean('Functions', 'Dice'):
            print()
        elif cmd == '8ball' and config.getboolean('Functions', '8ball'):
            await eightball.ex(c, msg.channel, get_m(msg), msg.content[7:], CMD_CHAR)
        elif cmd == 'gif' and config.getboolean('Functions', 'Random_gif'):
            await gif.ex(c, msg.channel, msg.content[5:], get_m(msg), CMD_CHAR)
        elif cmd == 'help':
            await bhelp.ex(c, msg.author, msg.channel, get_m(msg), msg.content.split(' '), CMD_CHAR)
        elif cmd == 'info':
            await info.ex(c, msg.channel)
        elif cmd == 'poll' and config.getboolean('Functions', 'Poll'):
            pll, q, opt, vts, vtd = await poll.ex_poll(c, msg.channel, msg.author, get_m(msg), msg.content[6:],
                                                       pll, q, opt, vts, vtd, CMD_CHAR)
        elif cmd == 'vote' and config.getboolean('Functions', 'Poll'):
            pll, q, opt, vts, vtd = await poll.ex_vote(c, msg.channel, msg.author, get_m(msg), msg.content[6:],
                                                       pll, q, opt, vts, vtd, CMD_CHAR)
        elif cmd == 'purge':
            print()
        elif cmd == 'reddit' and config.getboolean('Functions', 'Reddit'):
            await reddit.ex(c, msg.author, msg.channel, get_m(msg), msg.content[8:], CMD_CHAR)
        elif cmd == 'rps' and config.getboolean('Functions', 'Rock_paper_scissors'):
            await rps.ex(c, msg.channel, get_m(msg), msg.content[5:], CMD_CHAR)
        elif cmd == 'temp' and config.getboolean('Functions', 'Temperature'):
            await temp.ex(c, msg.channel, get_m(msg), msg.content[6:], CMD_CHAR)
        elif cmd == 'time' and config.getboolean('Functions', 'Timezone'):
            await time.ex(c, msg.channel, get_m(msg), msg.content[6:], CMD_CHAR)
        elif cmd == 'trans' and config.getboolean('Functions', 'Translate'):
            await trans.ex(c, msg.channel, get_m(msg), msg.content[7:], CMD_CHAR)
        elif cmd == 'twitch' and config.getboolean('Functions', 'Twitch'):
            print()
        elif cmd == 'uptime':
            await uptime.ex(c, msg.channel, ct)
        elif cmd == 'xkcd' and config.getboolean('Functions', 'XKCD'):
            await xkcd.ex(c, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'youtube' and config.getboolean('Functions', 'Youtube'):
            await youtube.ex(c, msg.channel, get_m(msg), msg.content[9:], CMD_CHAR)
        elif cmd == 'restart':
            await restart.ex(c, msg.channel, get_m(msg), msg.author)
    elif msg.content.startswith('<@{}>'.format(CLIENT_ID)) and config.getboolean('Functions', 'Cleverbot'):
        if int(msg.author.id) != int(CLIENT_ID):
            m = msg.content[22:]
            r = cb.ask(m)
            await c.send_message(msg.channel, '{} {}'.format(get_m(msg), r))

# Activate Bot
c.run(TOKEN_ID)
