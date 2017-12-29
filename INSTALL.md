## Setup
[Ubuntu/Debian](#ubuntudebian-installation) [CentOS/RedHat](#centosredhat-installation) [Windows](#windows-installation)
### Ubuntu/Debian Installation
Ubuntu 16.04+ have Python version 3.5+ installed by default. Otherwise, do this to install latest Python 3.5 version:

1) Python version 3.5+:
```Bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt update
sudo apt install python3.5
```

2) Python pip (so we can install packages) & ffmpeg (to play music):
```Bash
sudo apt-get install -y python3-pip ffmpeg
```

3) Development tools needed to run Python scripts:
```Bash
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
```

4) Install Python packages with PIP:
```Bash
sudo python3 -m pip install discord.py geopy pytube configparser asyncio pynacl youtube_dl bs4 pydictionary
```

5) Download the github files and export it to anywhere you want to store on your computer.

7) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

8) After you get it created, you need to enable that app as a bot so this bot can perform the job.

9) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in config.ini file:
```Ini
TokenID = PASTE_OVER_THIS
```

10) Copy the Client ID and paste it to the UserID variable in config.ini file:
```Ini
UserID = PASTE_OVER_THIS
```

11) Now we need to register that app to a specific server so that way the bot can find it's path to your server. Copy the 18-digit code from Client ID and follow the URL (replace the YOUR_CLIENT_ID_HERE with the Client ID code):
```
https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
```

12) Run the bot:
```Bash
python3 /path/to/app.py
```


### CentOS/RedHat Installation

1) Python version 3+:
```Bash
sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
sudo yum update
sudo yum install -y python35u python35u-libs python35u-devel python35u-pip
```

2) Python pip (so we can install packages) & ffmpeg (to play music):
```Bash
sudo yum install python35u-pip ffmpeg
```

3) Install Python packages with PIP:
```Bash
sudo python3.5 -m pip install discord.py geopy pytube configparser asyncio pynacl youtube_dl bs4 pydictionary
```

4) Download the github files and export it to anywhere you want to store on your computer.

5) Create a new application with the name of bot you want to appear on your server through https://discordapp.com/developers/applications/me

6) After you get it created, you need to enable that app as a bot so this bot can perform the job.

7) Copy the token through clicking on 'click to reveal' link and paste it to the token variable in config.ini file:
```Ini
TokenID = PASTE_OVER_THIS
```

8) Copy the Client ID and paste it to the UserID variable in config.ini file (Needed to allow bot to respond to @mentions):
```Ini
UserID = PASTE_OVER_THIS
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
## TODO
