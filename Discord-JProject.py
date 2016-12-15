import discord
import requests
import json
from Token import token
from translate import Translator
from currency_converter import CurrencyConverter
from cleverbot import Cleverbot

client = discord.Client()
LANG_LIST = ['AB', 'AA', 'AF', 'SQ', 'AM,' 'AR', 'HY', 'AS', 'AY', 'AZ', 'BA', 'EU', 'BN', 'DZ', 'BH', 'BI', 'BR', 'BG',
             'MY', 'BE', 'KM', 'CA', 'ZH', 'CO', 'HR', 'CS', 'DA', 'NL', 'EN', 'EO', 'ET', 'FO', 'FJ', 'FI', 'FR', 'FY',
             'GD', 'GL', 'KA', 'DE', 'EL', 'KL', 'GN', 'GU', 'HA', 'IW', 'HI', 'HU', 'IS', 'IN', 'IA', 'IE', 'IK', 'GA',
             'IT', 'JA', 'JW', 'KN', 'KS', 'KK', 'RW', 'KY', 'RN', 'KO', 'KU', 'LO', 'LA', 'LV', 'LN', 'LT', 'MK', 'MG',
             'MS', 'ML', 'MT', 'MI', 'MR', 'MO', 'MN', 'NA', 'NE', 'NO', 'OC', 'OR', 'OM', 'PS', 'FA', 'PL', 'PT', 'PA',
             'QU', 'RM', 'RO', 'RU', 'SM', 'SG', 'SA', 'SR', 'SH', 'ST', 'TN', 'SN', 'SD', 'SI', 'SS', 'SK', 'SL', 'SO',
             'ES', 'SU', 'SW', 'SV', 'TL', 'TG', 'TA', 'TT', 'TE', 'TH', 'BO', 'TI', 'TO', 'TS', 'TR', 'TK', 'TW', 'UK',
             'UR', 'UZ', 'VI', 'VO', 'CY', 'WO', 'XH', 'JI', 'YO', 'ZU']
CURR_LIST = ['AFA', 'ALL', 'DZD', 'AOR', 'ARS', 'AMD', 'AWG', 'AUD', 'AZN', 'BSD', 'BHD', 'BDT', 'BBD', 'BYN', 'BZD',
             'BMD', 'BTN', 'BOB', 'BWP', 'BRL', 'GBP', 'BND', 'BGN', 'BIF', 'KHR', 'CAD', 'CVE', 'KYD', 'XOF', 'XAF',
             'XPF', 'CLP', 'CNY', 'COP', 'KMF', 'CDF', 'CRC', 'HRK', 'CUP', 'CZK', 'DKK', 'DJF', 'DOP', 'XCD', 'EGP',
             'SVC', 'ERN', 'EEK', 'ETB', 'EUR', 'FKP', 'FJD', 'GMD', 'GEL', 'GHS', 'GIP', 'XAU', 'XFO', 'GTQ', 'GNF',
             'GYD', 'HTG', 'HNL', 'HKD', 'HUF', 'ISK', 'XDR', 'INR', 'IDR', 'IRR', 'IQD', 'ILS', 'JMD', 'JPY', 'JOD',
             'KZT', 'KES', 'KWD', 'KGS', 'LAK', 'LVL', 'LBP', 'LSL', 'LRD', 'LYD', 'LTL', 'MOP', 'MKD', 'MGA', 'MWK',
             'MYR', 'MVR', 'MRO', 'MUR', 'MXN', 'MDL', 'MNT', 'MAD', 'MZN', 'MMK', 'NAD', 'NPR', 'ANG', 'NZD', 'NIO',
             'NGN', 'KPW', 'NOK', 'OMR', 'PKR', 'XPD', 'PAB', 'PGK', 'PYG', 'PEN', 'PHP', 'XPT', 'PLN', 'QAR', 'RON',
             'RUB', 'RWF', 'SHP', 'WST', 'STD', 'SAR', 'RSD', 'SCR', 'SLL', 'XAG', 'SGD', 'SBD', 'SOS', 'ZAR', 'KRW',
             'LKR', 'SDG', 'SRD', 'SZL', 'SEK', 'CHF', 'SYP', 'TWD', 'TJS', 'TZS', 'THB', 'TOP', 'TTD', 'TND', 'TRY',
             'TMT', 'AED', 'UGX', 'XFU', 'UAH', 'UYU', 'USD', 'UZS', 'VUV', 'VEF', 'VND', 'YER', 'ZMK', 'ZWL']
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
            # Commands goes here
            if cmd == '-help':
                await client.send_message(msg.channel, 'List of commands:')
                await client.send_message(msg.channel, '1) -cat = Random pic/gif of any cat.')
                await client.send_message(msg.channel, '2) -trans <lang> <msg> = Translate message to any language ' +
                                                       'of choice.')
                await client.send_message(msg.channel, '  Languages: https://www.sitepoint.com/web-foundations/' +
                                                       'iso-2-letter-language-codes/')
                await client.send_message(msg.channel, '3) -chucknorris = Random Chuck Norris jokes.')
                await client.send_message(msg.channel, '4) -$convert <amount> <current-currency> <currency-to-convert' +
                                                       '-to> = Convert currency.')
                await client.send_message(msg.channel, '5) -poll <start|stop> (Question...) Create poll, only admins ' +
                                                       'can create/stop them.')
                await client.send_message(msg.channel, '       -yes = Answer yes to poll question.')
                await client.send_message(msg.channel, '       -no = Answer no to poll question.')
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
            elif cmd == '-$currency':
                args = msg.content.split(' ')
                if len(args) == 4:
                    b = args[1]
                    cc = args[2]
                    ct = args[3]
                    if chk_curr(b):
                        b = float(b)
                        if cc in CURR_LIST and ct in CURR_LIST:
                            fc = CurrencyConverter().convert(b, cc, ct)
                            await client.send_message(msg.channel, cc + ': ' + str(b) + '   ' + ct + ': ' + str(fc))
                        else:
                            await client.send_message(msg.channel, 'Invalid currency code! Please check https://' +
                                                                   'currencysystem.com/codes/, <@' + msg.author.id +
                                                                   '>!')
                    else:
                        await client.send_message(msg.channel, 'Currency must be in numeric/decimal value! Like 100' +
                                                               'or 54.42, <@' + msg.author.id + '>!')
                else:
                    await client.send_message(msg.channel, 'Usage: -$convert <amount> <current-currency> <currency-' +
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
