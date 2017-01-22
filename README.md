# Discord-JProject (Jinux) - v2.2
*Personal bot for Discord server(s).*

[<img src="https://img.shields.io/badge/build-passing-brightgreen.svg">](https://github.com/Atomicbeast101/Discord-JProject) [<img src="https://img.shields.io/badge/API-discord.py-551A8B.svg">](https://github.com/Rapptz/discord.py) [<img src="https://img.shields.io/badge/python-3.5%2B-blue.svg">](https://www.python.org/downloads/release/python-360/)

## Commands
| Command | Description | Example |
|:-------:|-------------|---------|
| `-help <cmd>` | Lists commands and description for each.  | -help cat |
| `-cat` | Posts a random picture/gif of a cat. | N/A |
| `-trans <lang-code> <msg>` | Translate message to desired language. | -trans de How are you? |
| `-chucknorris` | Posts a random Chuck Norris joke. | N/A |
| `-convert <amount> <from-code> <to-code>` | Convert currency. | -convert 100 USD EUR |
| `-poll <start|stop> <question>` | Create or stop polls. | -poll start Is gaming fun? |
| `-yes` | Answer yes to active poll. | N/A |
| `-no` | Answer no to active poll. | N/A |
| `-8ball` | Magic eight ball answering machine. | N/A |
| `-temp <temp#> <from-F|K|C> <to-F|K|C>` | Convert temperature between F, K, or C. | -temp 30 F C |
| `-youtube <to-search>` | Gets first video from YouTube search results. | -youtube best game ever |
| `-gif <tags>` | Gets a GIF from Giphy according to the tags given. | -gif american |
| `-uptime` | Bot's uptime status. | N/A |
| `-info` | Information about this bot. | N/A |
| `-time <timezone>` | Get current time according to timezone. | -timezone America/Chicago |
| `-rps <rock|paper|scissors>` | Rock, paper, scissors game. | -rps rock |
| `-twitch <add|remove|list| toggle|setchannel> <username-OR-channel-ID>` | Twitch live stream notification. | -twitch add atomicbeast101 OR -twitch toggle OR -twitch setchannel #CHANNEL_ID# |
| `-coinflip` | Flip a coin to receive heads or tails. | N/A |

> Administrators only have access to `-poll <start|stop>` and `-twitch <add|remove|toggle|setchannel>`. Users can do -twitch list. Bot checks for any Twitch users that are live streaming every 60 seconds.

List of translate codes: [https://www.sitepoint.com/web-foundations/iso-2-letter-language-codes/](https://www.sitepoint.com/web-foundations/iso-2-letter-language-codes/)

List of currency codes: [https://currencysystem.com/codes/](https://currencysystem.com/codes/)

List of timezones: [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Requirements
- Python v3.5+ (This was tested with Python v3.5.2. Python version 3.4 and below WILL not work.)
- Python packages: discord.py, asyncio, cleverbot, translate, bs4, pytz & python-twitch
- Linux or Windows OS (Standard server version is recommended.)
- Strong internet speed with minimal latency (Latency effects the response time from the bot.)
- Sudo access (Linux) or Administrator access (Windows)

## Setup
### Ubuntu/Debian Installation
In most cases, Python is usually installed by default in Ubuntu, but may not be in latest version you need to run Jinux bot.

1) Python version 3.5+:
```Bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5
```

2) Python pip (so we can install packages):
```Bash
sudo apt-get install -y python3.5-pip
```

3) Development tools needed to run Python scripts:
```Bash
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
```

4) Install Python packages with PIP:
```Bash
sudo python3.5 -m pip install discord.py asyncio cleverbot translate bs4 pytz python-twitch
```

5) Download the github files and export it to anywhere you want to store on your computer.

7) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

8) After you get it created, you need to enable that app as a bot so this bot can perform the job.

9) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in ClientID_TokenID.py Python script:
```Python
TOKEN_ID = 'tokenidgoeshere...'
```

10) Copy the Client ID and paste it to the CLIENT_ID variable in ClientID_TokenID.py Python script (Needed to allow bot to respond to @mentions):
```Python
CLIENT_ID = 'clientidgoeshere...'
```

11) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

12) Run the script:
```Bash
python3.5 /path/to/Discord-JProject.py
```


### CentOS Installation

1) Python version 3+:
```Bash
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python35u python35u-libs python35u-devel python35u-pip
```

2) Python pip (so we can install packages):
```Bash
sudo yum install python35u-pip
```

3) Install Python packages with PIP:
```Bash
sudo python3.5 -m pip install discord.py asyncio cleverbot translate bs4 pytz python-twitch
```

4) Download the github files and export it to anywhere you want to store on your computer.

5) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

6) After you get it created, you need to enable that app as a bot so this bot can perform the job.

7) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in ClientID_TokenID.py Python script:
```Python
TOKEN_ID = 'tokenidgoeshere...'
```

8) Copy the Client ID and paste it to the CLIENT_ID variable in ClientID_TokenID.py Python script (Needed to allow bot to respond to @mentions):
```Python
CLIENT_ID = 'clientidgoeshere...'
```

9) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

10) Run the script:
```Bash
python3.5 /path/to/Discord-JProject.py
```


### Windows Installation

1) Download latest Python version 3.5+: https://www.python.org/downloads/windows/, then double click on the .exe file to start the installation.

2) Open up the Command Prompt through Administrator mode.
Click on start menu and type down 'cmd' and then right click on the Command Prompt and run it as Administrator. (Administrator mode is needed in order to do any installations through Python.)

3) Run the command in Command Prompt to install the Discord Python API:
```PowerShell
python -m pip install discord.py asyncio cleverbot translate bs4 pytz python-twitch
```

4) Download the github files and export it to anywhere you want to store on your computer.

5) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

6) After you get it created, you need to enable that app as a bot so this bot can perform the job.

7) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in ClientID_TokenID.py Python script:
```Python
TOKEN_ID = 'tokenidgoeshere...'
```

8) Copy the Client ID and paste it to the CLIENT_ID variable in ClientID_TokenID.py Python script (Needed to allow bot to respond to @mentions):
```Python
CLIENT_ID = 'clientidgoeshere...'
```

9) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

10) Run the script:
```PowerShell
python /path/to/Discord-JProject.py
```


## Change Log:
- [v2.2] = Fixed bot's roasting program to work with Cleverbot's v2.0.0 update.
- [v2.1] = Bot kept talking to himself so I told him not to. (bug happens when doing -trans en @BotName Hello!).
- [v2.0] = Added following commands: -uptime, -time, -info, -coinflip, -rps & -twitch. Added Kelvin to -temp command.
- [v1.5] = Improved chat formatting, can do -help gif OR -help -gif, & has game status `Playing Bot | -help`
- [v1.4.1] = Fixed formatting and implemented proper error handling for -gif
- [v1.4] = Added -gif feature
- [v1.3] = Added -youtube feature
