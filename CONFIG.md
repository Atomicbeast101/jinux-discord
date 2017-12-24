# Configuration
## config.ini file for Jinux bot.
### General
```Ini
UserID = 
```
ID of the user for Jinux.
```Ini
TokenID =
```
Token ID for Jinux to connect to Discord server(s).
```Ini
ChannelID = 
```
ID of the channel where Jinux will say a welcome message in (shows it's online and working).
```Ini
Playing = -help | Jinux v5.0
```
"Playing" message that will be displayed underneath Jinux on right side of Discord chat application.
```Ini
WelcomeMessage = :wave: hey everyone!
```
Welcome message where Jinux will say in `ChannelID` channel on end of bootup mode.
```Ini
CommandCharacter = -
```
Starting symbol to recognize Jinux's commands.

### Log
```Ini
Disabled = no
```
Enable/Disable logging.
```Ini
Level = ERROR
```
Choose log level between INFO/WARNING/ERROR to display/show in log file.
```Ini
FileName = jinux.log
```
Name of log file to store logs to.

### Data
```Ini
DataFile = data.db
```
Name of SQLite database file to store data in.

### Music
```Ini
Enabled = yes
```
Enable music player for Jinux.
```Ini
TextchannelID = 
```
Channel ID to allow music-only commands in.
```Ini
VoiceChannelID = 
```
Channel ID where Jinux will play music in.
```Ini
PlaylistnameCharLimit = 10
```
Character limit for playlist names.

### TemporaryChannel
```Ini
Enabled = yes
```
Enable/Disable ability to create temporary channels.
```Ini
TimeLimit = 1d
```
Maximum time limit a temporary channel can last up to.
```Ini
ChannelNameCharLimit = 12
```
Character limit for temporary channel names.

### AutoWelcome
```Ini
Enabled = yes
```
Enable/Disable auto welcome messages by Jinux to new joiners through private/direct message.
```Ini
FileName = welcome.txt
```
Name of file to load welcome message in.

### ChatFilter
```Ini
Enabled = yes
```
Enable/Disable chat filtering system.
```Ini
FileName = blacklist.txt
```
Name of file to load the list of blacklisted words in.

### CustomCommands
```Ini
Enabled = yes
```
Enable/Disable ability to create/use custom commands.
```Ini
CommandCharaterLimit = 10
```
Character limit for custom commands.

### Commands
```Ini
Cat = yes
Choose = yes
Dice = yes
Dictionary = yes
Gif = yes
Poll = yes
Purge = yes
RemindMe = yes
RemindAll = yes
Rps = yes
Tempch = yes
Temp = yes
Time = yes
Uptime = yes
Xkcd = yes
Help = yes
```
Enable/Disable commands.
