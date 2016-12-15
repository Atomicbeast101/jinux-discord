import discord
import requests
import json
from Token import token
from Data import LANG_LIST, CURR_LIST, HELP, HELP_CAT, HELP_TRANS, HELP_CHUCKNORRIS, HELP_CONVERT, HELP_POLL,\
    HELP_YES, HELP_NO
from translate import Translator
from cleverbot import Cleverbot

client = discord.Client()

poll = False
q = ""
yes = 0
no = 0
voted = []


def chk_curr(msg):
    try:
        float(msg)
        return True
    except ValueError:
        return False


@client.event
async def on_message(msg):
    global poll
    global q
    global yes
    global no
    global voted
    if len(msg.content) > 0:
        if msg.content[0] == '-':
            cmd = msg.content.split(' ')[0].lower()
            if cmd == '-help':
                args = msg.content.split(' ')
                if len(args) == 2:
                    arg = args[1].lower()
                    if arg == 'cat':
                        await client.send_message(msg.channel, HELP_CAT)
                    elif arg == 'trans':
                        await client.send_message(msg.channel, HELP_TRANS)
                    elif arg == 'chucknorris':
                        await client.send_message(msg.channel, HELP_CHUCKNORRIS)
                    elif arg == 'convert':
                        await client.send_message(msg.channel, HELP_CONVERT)
                    elif arg == 'poll':
                        await client.send_message(msg.channel, HELP_POLL)
                    elif arg == 'yes':
                        await client.send_message(msg.channel, HELP_YES)
                    elif arg == 'no':
                        await client.send_message(msg.channel, HELP_NO)
                    else:
                        await client.send_message(msg.channel, HELP)
                else:
                    await client.send_message(msg.channel, HELP)
            elif cmd == '-cat':
                r = requests.get('http://random.cat/meow')
                d = json.loads(r.text)
                await client.send_message(msg.channel, d['file'])
            elif cmd == '-trans':
                args = msg.content.split(' ')
                if len(args) >= 3:
                    if args[1].upper() in LANG_LIST:
                        s = msg.content[10:]
                        tr = Translator(to_lang=args[1])
                        tn = tr.translate(s)
                        await client.send_message(msg.channel, tn)
                    else:
                        await client.send_message(msg.channel, 'Invalid language input! Please check https://www.' +
                                                               'sitepoint.com/web-foundations/iso-2-letter-language-' +
                                                               'codes/ for correct language code! Ex: en for English ' +
                                                               'or de for German')
                else:
                    await client.send_message(msg.channel, 'Usage: -trans <language> <to translate...>')
            elif cmd == '-chucknorris':
                r = requests.get('https://api.chucknorris.io/jokes/random')
                d = json.loads(r.text)
                await client.send_message(msg.channel, d['value'])
            elif cmd == '-convert':
                args = msg.content.split(' ')
                if len(args) == 4:
                    b = args[1]
                    cc = args[2]
                    ct = args[3]
                    if chk_curr(b):
                        b = float(b)
                        if cc in CURR_LIST and ct in CURR_LIST:
                            r = requests.get('http://free.currencyconverterapi.com/api/v3/convert?q=' + cc + '_' + ct +
                                             '&compact=y')
                            d = json.loads(r.text)
                            nb = b * float(d[cc + '_' + ct]['val'])
                            await client.send_message(msg.channel, '`' + cc + ': ' + str('%.2f' % b) + '`  >  `' + ct +
                                                      ': ' + str('%.2f' % nb) + '`')
                        else:
                            await client.send_message(msg.channel, 'Invalid currency code! Please check https://' +
                                                                   'currencysystem.com/codes/, <@' + msg.author.id +
                                                                   '>!')
                    else:
                        await client.send_message(msg.channel, 'Currency must be in numeric/decimal value! Like 100' +
                                                               'or 54.42, <@' + msg.author.id + '>!')
                else:
                    await client.send_message(msg.channel, 'Usage: -convert <amount> <current-currency> <currency-' +
                                                           'to-convert-to>')
            elif cmd == '-poll':
                if msg.author.server_permissions.administrator:
                    args = msg.content.split(' ')
                    if len(args) >= 2:
                        if args[1] == 'start':
                            if len(args) >= 3:
                                if poll:
                                    await client.send_message(msg.channel, '<@' + msg.author.id + '> poll already ' +
                                                                           'running! Please close the current one ' +
                                                                           'with: -poll stop')
                                else:
                                    poll = True
                                    yes = 0
                                    no = 0
                                    voted = []
                                    q = msg.content[12:]
                                    await client.send_message(msg.channel, '[Poll Started]: ' + q)
                                    await client.send_message(msg.channel, 'Answer: -yes OR -no')
                            else:
                                await client.send_message(msg.channel, 'Usage: -poll start <Question...?>')
                        elif args[1] == 'stop':
                            if not poll:
                                await client.send_message(msg.channel, "Poll isn't running, <@" + msg.author.id + ">!")
                            else:
                                poll = False
                                await client.send_message(msg.channel, '[Poll Closed]: ' + q)
                                await client.send_message(msg.channel, 'Result: `Yes: ' + str(yes) + '`    `No: ' +
                                                          str(no) + '`')
                        else:
                            await client.send_message(msg.channel, 'Usage: -poll <start|stop> (Question...?)')
                    else:
                        await client.send_message(msg.channel, 'Usage: -poll <start|stop> (Question...?)')
                else:
                    await client.send_message(msg.channel, 'You must be an administrator, <@' + msg.author.id + '>!')
            elif cmd == '-yes':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        yes += 1
                        await client.send_message(msg.channel, 'Question: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: ' + str(yes) + '`    `No: ' + str(no) +
                                                  '`')
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud, <@' + msg.author.id
                                                               + '>?')
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say yes for, <@' + msg.author.id
                                                           + '>?')
            elif cmd == '-no':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        no += 1
                        await client.send_message(msg.channel, 'Question: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: ' + str(yes) + '`    `No: ' + str(no) +
                                                  '`')
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud <@' + msg.author.id
                                                               + '>?')
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say no for, <@' + msg.author.id
                                                           + '>?')
        else:
            if msg.content.startswith('<@258753582600421386>'):
                m = msg.content[22:]
                r = Cleverbot().ask(m)
                await client.send_message(msg.channel, '<@' + msg.author.id + '> ' + r)

client.run(token)
