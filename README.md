# Discord-JProject
Personal bot for Discord server(s).

## Requirements
- Python v3+ (This was tested with Python v3.5.2)
- Python packages: discord.py
- Linux or Windows OS (Standard server version is recommended.)

## Setup
### Ubuntu Installation
In most cases, Python is usually installed by default in Ubuntu, but may not be latest version you need to run Jinux bot.

1) Python version 3+:
```Bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install python3
```

2) Pthon pip (so we can install packages):
```Bash
sudo apt-get install -y python3-pip
```

3) Development tools needed to run Python scripts:
```Bash
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
```

4) Discord Python API:
```Bash
sudo python3 -m pip install discord.py
```

5) Download the github files and export it to anywhere you want to store on your computer.

7) Create a new application with the name of bot you want to appear on your server through [here]https://discordapp.com/developers/applications/me

8) After you get it created, you need to enable that app as a bot so this bot can perform the job.

9) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in Token.py Python script:
```Python
token = 'tokengoeshere...
```

10) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0 
```

6) Run the script:
```Bash
python3 /path/to/Discord-JProject.py
```

### Windows installation (coming soon)
