import discord
import requests
import json
from ClientID_TokenID import TOKEN_ID, CLIENT_ID
from Data import LANG_LIST, CURR_LIST, HELP, HELP_CAT, HELP_TRANS, HELP_CHUCKNORRIS, HELP_CONVERT, HELP_POLL,\
    HELP_YES, HELP_NO, HELP_BALL, HELP_TEMP
from translate import Translator
from cleverbot import Cleverbot

client = discord.Client()

# Variables for poll system
poll = False
q = ""
yes = 0
no = 0
voted = []


# Checks to make sure the string currency can be converted to float data value
def chk_curr(msg):
    try:
        float(msg)
        return True
    except ValueError:
        return False


# Checks to make sure the string temperature can be converted to int data value
def chk_temp(msg):
    try:
        int(msg)
        return True
    except ValueError:
        return False


# Returns the mention of the author that the bot will reply to
def get_mention(msg):
    return '<@' + msg.author.id + '> '


# Automatically called everytime a player sends a message to any channel
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
            # Help Guide
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
                    elif arg == '8ball':
                        await client.send_message(msg.channel, HELP_BALL)
                    elif arg == 'temp':
                        await client.send_message(msg.channel, HELP_TEMP)
                    else:
                        await client.send_message(msg.channel, HELP)
                else:
                    await client.send_message(msg.channel, HELP)
            # Posts random picture/gif of cat through -cat command
            elif cmd == '-cat':
                r = requests.get('http://random.cat/meow')
                d = json.loads(r.text)
                await client.send_message(msg.channel, d['file'])
            # Translate message to language of user choice through -trans command
            elif cmd == '-trans':
                args = msg.content.split(' ')
                if len(args) >= 3:
                    if args[1].upper() in LANG_LIST:
                        s = msg.content[10:]
                        tr = Translator(to_lang=args[1])
                        tn = tr.translate(s)
                        await client.send_message(msg.channel, tn)
                    else:
                        await client.send_message(msg.channel, 'Invalid language input! Please checkhttps://www.site' +
                                                  'point.com/web-foundations/iso-2-letter-language-codes/ for correct' +
                                                  'language code! Ex: en for English or de for German')
                else:
                    await client.send_message(msg.channel, get_mention(msg) + 'Usage: -trans <language> ' +
                                              '<to translate...>')
            # Posts random Chuck Norris joke through -chucknorris command
            elif cmd == '-chucknorris':
                r = requests.get('https://api.chucknorris.io/jokes/random')
                d = json.loads(r.text)
                await client.send_message(msg.channel, d['value'])
            # Converts money between different currencies through -convert command
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
                            await client.send_message(msg.channel, get_mention(msg) + 'Invalid currency code! Please ' +
                                                      'check https://currencysystem.com/codes/!')
                    else:
                        await client.send_message(msg.channel, get_mention(msg) + 'Currency must be in numeric/' +
                                                  'decimal value! Like 100 or 54.42!')
                else:
                    await client.send_message(msg.channel, get_mention(msg) + 'Usage: -convert <amount> <current-' +
                                              'currency> <currency-to-convert-to>')
            # Poll system through -poll command
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
                                await client.send_message(msg.channel, get_mention(msg) + 'Usage: -poll start <' +
                                                          'Question...?>')
                        elif args[1] == 'stop':
                            if not poll:
                                await client.send_message(msg.channel, "Poll isn't running, <@" + msg.author.id + ">!")
                            else:
                                poll = False
                                await client.send_message(msg.channel, '[Poll Closed]: ' + q)
                                await client.send_message(msg.channel, 'Result: `Yes: ' + str(yes) + '`    `No: ' +
                                                          str(no) + '`')
                        else:
                            await client.send_message(msg.channel, get_mention(msg) + 'Usage: -poll <start|stop> ' +
                                                      '(Question...?)')
                    else:
                        await client.send_message(msg.channel, get_mention(msg) + 'Usage: -poll <start|stop> ' +
                                                  '(Question...?)')
                else:
                    await client.send_message(msg.channel, 'You must be an administrator, <@' + msg.author.id + '>!')
            elif cmd == '-yes':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        yes += 1
                        await client.send_message(msg.channel, '[Question]: ' + q)
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
                        await client.send_message(msg.channel, '[Question]: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: ' + str(yes) + '`    `No: ' + str(no) +
                                                  '`')
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud <@' + msg.author.id
                                                               + '>?')
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say no for, <@' + msg.author.id
                                                           + '>?')
            # Magic eight ball through -8ball command
            elif cmd == '-8ball':
                if len(msg.content.split(' ')) > 1:
                    q = msg.content[7:]
                    q.replace(' ', '%')
                    q.replace('?', '%3F')
                    q.replace(',', '%2C')
                    r = requests.get('https://8ball.delegator.com/magic/JSON/' + q)
                    d = json.loads(r.text)
                    await client.send_message(msg.channel, get_mention(msg) + d['magic']['answer'])
                else:
                    await client.send_message(msg.channel, get_mention(msg) + 'Usage: -8ball <Question...>')
            # Convert temperature between F and C through -temp command
            elif cmd == '-temp':
                args = msg.content.split(' ')
                if len(args) == 3:
                    if chk_temp(args[1]):
                        t = int(args[1])
                        if args[2].upper() == 'F':
                            ft = (t * 1.8) + 32
                            await client.send_message(msg.channel, str('%.0f' % t) + ' C`  >   ' + str('%.0f' % ft)
                                                      + ' F`')
                        elif args[2].upper() == 'C':
                            ft = (t - 32) * .5556
                            await client.send_message(msg.channel, str('%.0f' % t) + ' F`  >   ' + str('%.0f' % ft)
                                                      + ' C`')
                        else:
                            await client.send_message(msg.channel,
                                                      'Bruh. You can only convert the temperature between ' +
                                                      ' F or C, <@' + msg.author.id + '>!')
                    else:
                        await client.send_message(msg.channel, 'Temperature to convert must be in whole #,  <@'
                                                  + msg.author.id + '>!')
                else:
                    await client.send_message(msg.channel, get_mention(msg) + 'Usage: -temp <temp #> <F|C>')
        else:
            # Automatic response to mention. Running on CleverBot API
            if msg.content.startswith('<@' + CLIENT_ID + '>'):
                m = msg.content[22:]
                r = Cleverbot().ask(m)
                await client.send_message(msg.channel, '<@' + msg.author.id + '> ' + r)

client.run(token)
