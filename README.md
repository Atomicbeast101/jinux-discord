# Discord-JProject (Jinux) - v1.5
*Personal bot for Discord server(s).*

[<img src="https://img.shields.io/badge/discord-py-blue.svg">](https://github.com/Rapptz/discord.py)

## Requirements
- Python v3.5+ (This was tested with Python v3.5.2. Python version 3.4 and below WILL not work.)
- Python packages: discord.py, asyncio, cleverbot, translate & bs4
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
sudo python3.5 -m pip install discord.py asyncio cleverbot translate bs4
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
sudo python3.5 -m pip install discord.py asyncio cleverbot translate bs4
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
python -m pip install discord.py asyncio cleverbot translate bs4
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
- [v1.5] = Improved chat formatting, can do -help gif OR -help -gif, & has game status `Playing Bot | -help`
- [v1.4.1] = Fixed formatting and implemented proper error handling for -gif
- [v1.4] = Added -gif feature
- [v1.3] = Added -youtube feature
