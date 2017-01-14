from Config import CMD_CHAR

# Bot uses this data. Nothing to explain much here.
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

HELP = '''```Markdown
# List of commands #
1. help <command> = More information about the specified command.
2. {0}cat = Random picture or gif of a cat.
3. {0}trans <lang-code> <msg> = Translate message to desired language.
4. {0}chucknorris = Random Chuck Norris jokes.
5. {0}convert <amount> <currency-code> <currency-code-to> = Convert currency.
6. {0}poll <start|stop> <Question...> = Create or stop polls. Currently only for admins.
7. {0}yes = Answer yes to active poll.
8. {0}no = Answer no to active poll.
9. {0}8ball = Magic eight ball answering machine.
10. {0}temp <temp#> <from-F|K|C> <to-F|K|C> = Convert temperature to F or C.
11. {0}youtube <to-search> = Gets first video from YouTube search results.
12. {0}gif <tags> = Gets a GIF from Giphy according to the tags given.
13. {0}uptime = Bot's uptime status.
14. {0}info = Information about this bot.
15. {0}time <timezone> = Get current time according to timezone.
16. {0}rps <rock|paper|scissors> = Rock, paper, scissors game.
17. {0}twitch <add|remove|list|toggle|setchannel> <username-OR-channel-ID> = Twitch live stream notification.
18. {0}coinflip = Flip a coin to receive heads or tails.```'''.format(CMD_CHAR)

HELP_CAT = '''```Markdown
[Help Guide]: {}cat
Posts a random picture or animated gif of a cat.```'''.format(CMD_CHAR)

HELP_TRANS = '''```Markdown
[Help Guide]: {}trans <lang-code> <msg>
Translate a specified message to a supported language of choice.
<lang-code> = The language code to which the message should be translated.
<msg> = The message to be translated.```
List of supported language codes:
https://www.sitepoint.com/web-foundations/iso-2-letter-language-codes/'''.format(CMD_CHAR)

HELP_CHUCKNORRIS = '''```Markdown
[Help Guide]: {}chucknorris
Posts a random Chuck Norris joke.```'''.format(CMD_CHAR)

HELP_CONVERT = '''```Markdown
[Help Guide]: {}convert <amount> <from-currency> <to-currency>
Converts the specified amount of money to a desired currency.
<amount> = The amount to convert.
<from-currency> = The currency code from which to convert.
<to-currency> = The currency code to which the amount should be converted.```
List of supported currency codes: https://currencysystem.com/codes/'''.format(CMD_CHAR)

HELP_POLL = '''```Markdown
[Help Guide]: {}poll <start|stop> <question>
Create or stop polls. Currently only admins are allowed to use this command.
<start|stop> = Either start a new poll or stop an active poll.
<question> = Desired poll question.```'''.format(CMD_CHAR)

HELP_YES = '''```Markdown
[Help Guide]: {}yes
Vote yes on an active poll.```'''.format(CMD_CHAR)

HELP_NO = '''```Markdown
[Help Guide]: {}no
Vote no on an active poll.```'''.format(CMD_CHAR)

HELP_BALL = '''```Markdown
[Help Guide]: {}8ball <question>
Ask the magical 8ball a question and receive an answer.
<question> = Desired question.```'''.format(CMD_CHAR)

HELP_TEMP = '''```Markdown
[Help Guide]: {}temp <temp#> <from F|K|C> <to F|K|C>
Convert temperature between F, K, or C.
<temp#> = Temperature you want to convert to.
<from F|K|C> = Current temperature measurement.
<to F|K|C> = Temperature measurement to convert to.```'''.format(CMD_CHAR)

HELP_YOUTUBE = '''```Markdown
[Help Guide]: {}youtube <to-search>
Retrieves first video from YouTube search results.
<to-search> = No need to explain here.```'''.format(CMD_CHAR)

HELP_GIF = '''```Markdown
[Help Guide]: {}gif <tags>
Retrieves GIF from Giphy according to the tags given.
<tags> = Specific GIF you want to find (ex: silly OR american).```'''.format(CMD_CHAR)

HELP_UPTIME = '''```Markdown
[Help Guide]: {}uptime
Bot's uptime status.'''.format(CMD_CHAR)

HELP_INFO = '''```Markdown
[Help Guide]: {}info
Information about this bot.'''.format(CMD_CHAR)

HELP_TIME = '''```Markdown
[Help Guide]: {}time <timezone>
Get current time according to timezone.
<timezone> = Timezone to get current time from (ex: America/Chicago),
List of timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones```'''.format(CMD_CHAR)

HELP_RPS = '''```Markdown
[Help Guide]: {}rps <rock|paper|scissors>
Rock, paper, scissors game.
<rock|paper|scissors> = Choose your option to compete against the bot.'''.format(CMD_CHAR)

HELP_TWITCH = '''```Markdown
[Help Guide]: {}twitch <add|remove|list|toggle|setchannel> <username-OR-channel-ID>
Receive live status of Twitch username whenever he/she goes online.
<add|remove|list|toggle|setchannel> = List of sub-commands.
<username-OR-channel-ID> = Twitch's username OR channel's ID for bot to post notifications```'''.format(CMD_CHAR)

HELP_COINFLIP = '''```Markdown
[Help Guide]: {}coinflip
Flip a coin to receive heads or tails.'''.format(CMD_CHAR)
