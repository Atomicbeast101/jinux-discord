# Jinux - v3.0
*Personal bot for Discord server(s).*

[<img src="https://img.shields.io/badge/build-passing-brightgreen.svg">](https://github.com/Atomicbeast101/Discord-JProject) [<img src="https://img.shields.io/badge/API-discord.py-551A8B.svg">](https://github.com/Rapptz/discord.py) [<img src="https://img.shields.io/badge/python-3.5%2B-blue.svg">](https://www.python.org/downloads/release/python-360/)

## Requirements
- Python v3.5+ (This was tested with Python v3.5.0. Python version 3.4 and below WILL not work.)
- Python packages: `asyncio python-aiml discord.py python-twitch aiohttp PyDictionary geopy translate bs4`
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
sudo python3.5 -m pip install asyncio python-aiml discord.py python-twitch aiohttp PyDictionary geopy translate bs4
```

5) Download the github files and export it to anywhere you want to store on your computer.

7) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

8) After you get it created, you need to enable that app as a bot so this bot can perform the job.

9) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in config.ini file:
```Ini
Token = PASTE_OVER_THIS
```

10) Copy the Client ID and paste it to the Client_ID variable in config.ini file (Needed to allow bot to respond to @mentions):
```Ini
Client_ID = PASTE_OVER_THIS
```

11) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

12) Run the script:
```Bash
python3.5 /path/to/Jinux.py
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
sudo python3.5 -m pip install asyncio python-aiml discord.py python-twitch aiohttp PyDictionary geopy translate bs4
```

4) Download the github files and export it to anywhere you want to store on your computer.

5) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

6) After you get it created, you need to enable that app as a bot so this bot can perform the job.

7) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in config.ini file:
```Ini
Token = PASTE_OVER_THIS
```

8) Copy the Client ID and paste it to the Client_ID variable in config.ini file (Needed to allow bot to respond to @mentions):
```Ini
Client_ID = PASTE_OVER_THIS
```

9) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

10) Run the script:
```Bash
python3.5 /path/to/Jinux.py
```


### Windows Installation

1) Download latest Python version 3.5+: https://www.python.org/downloads/windows/, then double click on the .exe file to start the installation.

2) Open up the Command Prompt through Administrator mode.
Click on start menu and type down 'cmd' and then right click on the Command Prompt and run it as Administrator. (Administrator mode is needed in order to do any installations through Python.)

3) Run the command in Command Prompt to install the Discord Python API:
```PowerShell
python -m pip install asyncio python-aiml discord.py python-twitch aiohttp PyDictionary geopy translate bs4
```

4) Download the github files and export it to anywhere you want to store on your computer.

5) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

6) After you get it created, you need to enable that app as a bot so this bot can perform the job.

7) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in config.ini file:
```Ini
Token = PASTE_OVER_THIS
```

8) Copy the Client ID and paste it to the Client_ID variable in config.ini file (Needed to allow bot to respond to @mentions):
```Ini
Client_ID = PASTE_OVER_THIS
```

9) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

10) Run the script:
```PowerShell
python /path/to/Jinux.py
```


## Change Log:
- [v3.0] = Big update! Such wow! Such awesomeness!
- [v2.3] = Made Cleverbot API work again.
- [v2.2] = Fixed bot's roasting program to work with Cleverbot's v2.0.0 update.
- [v2.1] = Bot kept talking to himself so I told him not to. (bug happens when doing -trans en @BotName Hello!).
- [v2.0] = Added following commands: -uptime, -time, -info, -coinflip, -rps & -twitch. Added Kelvin to -temp command.
- [v1.5] = Improved chat formatting, can do -help gif OR -help -gif, & has game status `Playing Bot | -help`
- [v1.4.1] = Fixed formatting and implemented proper error handling for -gif
- [v1.4] = Added -gif feature
- [v1.3] = Added -youtube feature
