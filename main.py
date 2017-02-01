from config import TOKEN_ID, CLIENT_ID, CMD_CHAR
import discord
from cmds import cat, choose, chucknorris, coinflip, convert, eightball, gif, bhelp, info, poll, rps, temp, time, \
    trans, uptime, xkcd, youtube
from cleverbot import Cleverbot
from datetime import datetime


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
    await c.change_presence(game=discord.Game(name='Bot v{} | {}help'.format('3.0', CMD_CHAR)))
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
        if cmd == 'cat':
            await cat.ex(c, msg.channel)
        elif cmd == 'choose':
            o = msg.content[8:].split(' ')
            await choose.ex(c, msg.channel, get_m(msg), o)
        elif cmd == 'chucknorris':
            await chucknorris.ex(c, msg.channel)
        elif cmd == 'coinflip':
            await coinflip.ex(c, msg.channel, get_m(msg))
        elif cmd == 'convert':
            await convert.ex(c, msg.channel, get_m(msg), msg.content[9:].split(' '))
        elif cmd == 'dice':
            print()
        elif cmd == '8ball':
            await eightball.ex(c, msg.channel, get_m(msg), msg.content[7:])
        elif cmd == 'gif':
            await gif.ex(c, msg.channel, msg.content[5:])
        elif cmd == 'help':
            await bhelp.ex(c, msg.author, msg.channel, get_m(msg), msg.content.split(' '))
        elif cmd == 'info':
            await info.ex(c, msg.channel)
        elif cmd == 'poll':
            pll, q, opt, vts, vtd = await poll.ex_poll(c, msg.channel, msg.author, get_m(msg), msg.content[6:],
                                                        pll, q, opt, vts, vtd)
        elif cmd == 'vote':
            pll, q, opt, vts, vtd = await poll.ex_vote(c, msg.channel, msg.author, get_m(msg), msg.content[6:],
                                                        pll, q, opt, vts, vtd)
        elif cmd == 'purge':
            print()
        elif cmd == 'reddit':
            print()
        elif cmd == 'rps':
            await rps.ex(c, msg.channel, get_m(msg), msg.content[5:])
        elif cmd == 'temp':
            await temp.ex(c, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'time':
            await time.ex(c, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'trans':
            await trans.ex(c, msg.channel, get_m(msg), msg.content[7:])
        elif cmd == 'twitch':
            print()
        elif cmd == 'uptime':
            await uptime.ex(c, msg.channel, ct)
        elif cmd == 'xkcd':
            await xkcd.ex(c, msg.channel, get_m(msg), msg.content[6:])
        elif cmd == 'youtube':
            await youtube.ex(c, msg.channel, get_m(msg), msg.content[9:])
        else:
            print()
    elif msg.content.startswith('<@{}>'.format(CLIENT_ID)):
        if int(msg.author.id) != int(CLIENT_ID):
            m = msg.content[22:]
            r = cb.ask(m)
            await c.send_message(msg.channel, '{} {}'.format(get_m(msg), r))

# Activate Bot
c.run(TOKEN_ID)
