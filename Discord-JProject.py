import discord
import requests
import json
from Token import token
from translate import Translator
from cleverbot import Cleverbot

client = discord.Client()
LANG_LIST = ['AB', 'AA', 'AF', 'SQ', 'AM,' 'AR', 'HY', 'AS', 'AY', 'AZ', 'BA', 'EU', 'BN', 'DZ', 'BH', 'BI', 'BR', 'BG',
 'MY', 'BE', 'KM', 'CA', 'ZH', 'CO', 'HR', 'CS', 'DA', 'NL', 'EN', 'EO', 'ET', 'FO', 'FJ', 'FI', 'FR', 'FY', 'GD', 'GL',
 'KA', 'DE', 'EL', 'KL', 'GN', 'GU', 'HA', 'IW', 'HI', 'HU', 'IS', 'IN', 'IA', 'IE', 'IK', 'GA', 'IT', 'JA', 'JW', 'KN',
 'KS', 'KK', 'RW', 'KY', 'RN', 'KO', 'KU', 'LO', 'LA', 'LV', 'LN', 'LT', 'MK', 'MG', 'MS', 'ML', 'MT', 'MI', 'MR', 'MO',
 'MN', 'NA', 'NE', 'NO', 'OC', 'OR', 'OM', 'PS', 'FA', 'PL', 'PT', 'PA', 'QU', 'RM', 'RO', 'RU', 'SM', 'SG', 'SA', 'SR',
 'SH', 'ST', 'TN', 'SN', 'SD', 'SI', 'SS', 'SK', 'SL', 'SO', 'ES', 'SU', 'SW', 'SV', 'TL', 'TG', 'TA', 'TT', 'TE', 'TH',
 'BO', 'TI', 'TO', 'TS', 'TR', 'TK', 'TW', 'UK', 'UR', 'UZ', 'VI', 'VO', 'CY', 'WO', 'XH', 'JI', 'YO', 'ZU']
poll = False
q = ""
yes = 0
no = 0
voted = []


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
            # Commands goes here
            if cmd == '-help':
                await client.send_message(msg.channel, 'List of commands:')
                await client.send_message(msg.channel, '1) -cat = Random pic/gif of any cat.')
                await client.send_message(msg.channel, '2) -trans <lang> <msg> = Translate message to any language ' +
                                                       'of choice.')
                await client.send_message(msg.channel, '  Languages: https://www.sitepoint.com/web-foundations/' +
                                                       'iso-2-letter-language-codes/')
                await client.send_message(msg.channel, '3) -chucknorris = Random Chuck Norris jokes.')
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
                                await client.send_message(msg.channel, 'Result: Yes: ' + str(yes) + '   No: ' + str(no))
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
                        await client.send_message(msg.channel, 'Result: Yes: ' + str(yes) + '   No: ' + str(no))
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
                        await client.send_message(msg.channel, 'Result: Yes: ' + str(yes) + '   No: ' + str(no))
                    else:
                        await client.send_message(msg.channel, 'Trying to commit a voting fraud <@' + msg.author.id
                                                               + '>?')
                else:
                    await client.send_message(msg.channel, 'Why are you trying to say no for, <@' + msg.author.id
                                                           + '>?')
    else:
        # Mentions goes here
        if msg.content.startswith('<@256116246154706954>'):
            m = msg.content[22:]
            r = Cleverbot().ask(m)
            await client.send_message(msg.channel, '<@' + msg.author.id + '> ' + r)

client.run(token)
