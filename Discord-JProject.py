import discord
import requests
import json
from ClientID_TokenID import TOKEN_ID, CLIENT_ID
from Data import LANG_LIST, CURR_LIST, HELP, HELP_CAT, HELP_TRANS, HELP_CHUCKNORRIS, HELP_CONVERT, HELP_POLL,\
    HELP_YES, HELP_NO, HELP_BALL, HELP_TEMP, HELP_YOUTUBE, HELP_GIF
from translate import Translator
from cleverbot import Cleverbot
from bs4 import BeautifulSoup

# Setting up bot
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
    return '<@{}>'.format(msg.author.id)


# Automatically called every time a player sends a message to any channel
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
                    elif arg == 'youtube':
                        await client.send_message(msg.channel, HELP_YOUTUBE)
                    elif arg == 'gif':
                        await client.send_message(msg.channel, HELP_GIF)
                    else:
                        await client.send_message(msg.channel, HELP)
                else:
                    await client.send_message(msg.channel, HELP)
            # Posts random picture/gif of cat through -cat command
            elif cmd == '-cat':
                r = requests.get('http://random.cat/meow')
                d = json.loads(r.text)
                await client.send_message(msg.channel, '{}'.format(d['file']))
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
                        await client.send_message(msg.channel, '{} Invalid language input! Please check https://www' +
                                                  '.sitepoint.com/web-foundations/iso-2-letter-language-codes/ for' +
                                                  'correct language code! Ex: en for English or de for German'
                                                  .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: -trans <language> <to translate...>'
                                                           .format(get_mention(msg)))
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
                    cc = args[2].upper()
                    ct = args[3].upper()
                    if chk_curr(b):
                        b = float(b)
                        if cc in CURR_LIST and ct in CURR_LIST:
                            r = requests.get('http://free.currencyconverterapi.com/api/v3/convert?q={}_{}&compact=y'
                                             .format(cc, ct))
                            d = json.loads(r.text)
                            nb = b * float(d[cc + '_' + ct]['val'])
                            await client.send_message(msg.channel, '`{}: {:.2f}` > `{}: {:.2f}`'.format(cc, b, ct, nb))
                        else:
                            await client.send_message(msg.channel, '{} Invalid currency code! Please check https://' +
                                                                   'currencysystem.com/codes/!'
                                                                   .format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, '{} Currency must be in numeric/decimal value! Like ' +
                                                               '100 or 54.42!'.format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: -convert <amount> <current-currency> <currency' +
                                                           '-to-convert-to>'.format(get_mention(msg)))
            # Poll system through -poll command
            elif cmd == '-poll':
                if msg.channel.permissions_for(msg.author).administrator:
                    args = msg.content.split(' ')
                    if len(args) >= 2:
                        if args[1].lower() == 'start':
                            if len(args) >= 3:
                                if poll:
                                    await client.send_message(msg.channel, '{} poll already running! Please close '
                                                                           'the current one with: -poll stop'
                                                                           .format(get_mention(msg)))
                                else:
                                    poll = True
                                    yes = 0
                                    no = 0
                                    voted = []
                                    q = msg.content[12:]
                                    await client.send_message(msg.channel, '[Poll Started]: {}'.format(q))
                                    await client.send_message(msg.channel, 'Answer: -yes OR -no')
                            else:
                                await client.send_message(msg.channel, '{} Usage: -poll start <Question...?>'
                                                                       .format(get_mention(msg)))
                        elif args[1].lower() == 'stop':
                            if not poll:
                                await client.send_message(msg.channel, "Poll isn't running, {}!"
                                                                       .format(get_mention(msg)))
                            else:
                                poll = False
                                await client.send_message(msg.channel, '[Poll Closed]: {}'.format(q))
                                await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                              str(no)))
                        else:
                            await client.send_message(msg.channel, '{} Usage: -poll <start|stop> (Question...?)'
                                                                   .format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, '{} Usage: -poll <start|stop> (Question...?)'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, 'You must be an administrator, {}!'.format(get_mention(msg)))
            elif cmd == '-yes':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        yes += 1
                        await client.send_message(msg.channel, '[Question]: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                      str(no)))
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud, {}?'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say yes for, {}?'
                                                           .format(get_mention(msg)))
            elif cmd == '-no':
                if poll:
                    if msg.author.id not in voted:
                        voted.append(msg.author.id)
                        no += 1
                        await client.send_message(msg.channel, '[Question]: ' + q)
                        await client.send_message(msg.channel, 'Result: `Yes: {}`    `No: {}`'.format(str(yes),
                                                                                                      str(no)))
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud, {}?'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say no for, {}?'
                                                           .format(get_mention(msg)))
            # Magic eight ball through -8ball command
            elif cmd == '-8ball':
                if len(msg.content.split(' ')) > 1:
                    q = msg.content[7:]
                    q.replace(' ', '%')
                    q.replace('?', '%3F')
                    q.replace(',', '%2C')
                    r = requests.get('https://8ball.delegator.com/magic/JSON/' + q)
                    d = json.loads(r.text)
                    await client.send_message(msg.channel, '{} {}'.format(get_mention(msg), d['magic']['answer']))
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
                            await client.send_message(msg.channel, '`{:.2f} Celsius`  >  `{:.2f} Fahrenheit'
                                                                   .format(t, ft))
                        elif args[2].upper() == 'C':
                            ft = (t - 32) * .5556
                            await client.send_message(msg.channel, '`{:.2f} Fahrenheit`  >  `{:.2f} Celsius'
                                                      .format(t, ft))
                        else:
                            await client.send_message(msg.channel, 'You can only convert the temperature between F ' +
                                                                   'or C, {}'.format(get_mention(msg)))
                    else:
                        await client.send_message(msg.channel, 'Temperature to convert must be in whole #, {}'
                                                               .format(get_mention(msg)))
                else:
                    await client.send_message(msg.channel, '{} Usage: -temp <temp #> <F|C>'.format(get_mention(msg)))
            # Search first video from YouTube
            elif cmd == '-youtube':
                args = msg.content.split(' ')
                if len(args) >= 2:
                    se = msg.content[8:]
                    se.replace(" ", "+")
                    try:
                        s = BeautifulSoup(requests.get('https://www.youtube.com/results?search_query={}'.format(se))
                                          .text, 'html.parser')
                        vds = s.find('div', id='results').find_all('div', class_='yt-lockup-content')
                        if not vds:
                            await client.send_message(msg.channel, "{} Couldn't find any results!"
                                                      .format(get_mention(msg)))
                        i, f = 0, False
                        while not f and i < 20:
                            h = vds[i].find('a', class_='yt-uix-sessionlink')['href']
                            if h.startswith('/watch'):
                                f = True
                            i += 1
                        if not f:
                            await client.send_message(msg.channel, "{} Couldn't find any link!"
                                                      .format(get_mention(msg)))
                        await client.send_message(msg.channel, 'https://youtube.com{}'.format(h))
                    except Exception as ex:
                        await client.send_message(msg.channel, '{} Unable to search for a video!'
                                                  .format(get_mention(msg)))
                        print(ex)
                else:
                    await client.send_message(msg.channel, '{} Usage: -youtube <to-search>'.format(get_mention(msg)))
            # Posts random GIF from Giphy depending on tags players put down
            elif cmd == '-gif':
                args = msg.content.split(' ')
                if len(args) >= 2:
                    s = msg.content[6:]
                    s = s.replace(' ', '+')
                    r = requests.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(s))
                    d = json.loads(r.text)
                    await client.send_message(msg.channel, '{}'.format(
                                                                d['data']['fixed_height_downsampled_url']))
                else:
                    await client.send_message(msg.channel, '{} Usage: -gif <tags>'.format(get_mention(msg)))
        else:
            # Automatic response to mention. Running on CleverBot API
            if msg.content.startswith('<@' + CLIENT_ID + '>'):
                m = msg.content[22:]
                re = Cleverbot().ask(m)
                await client.send_message(msg.channel, '{} {}'.format(get_mention(msg), re))

client.run(TOKEN_ID)
