# Configuration
## config.ini file for Jinux bot.
```Ini
[Jinux]
Channel = 0
```

ID of the channel where Jinux will "wave" in (meaning that it's online and working).
```Ini
Character = -
```
Starting character of the command. Default is `-`. If you change it to `=` for example, all commands have to start with that. (ex: =help).
```Ini
Playing = -help | Jinux v4.0
```
Playing status of the bot.
```Ini
Logging = On
```
Toggle the logging of the commands/bot replies the users execute. The logs gets stored in `jinux.log` file.
```Ini
Auto_Welcome = On
```
Toggle `Auto_Welcome` between `On` or `Off` to tell Jinux to send a private welcome message (from `welcome_message.txt` file) directly to the new user who recently joined the server.
```Ini
[Twitch]
Enabled = No
```
Toggle between `Yes` or `No` to run the Twitch live stream notifications.
```Ini
Interval = 300
```
How long between each job task for Jinux to check each user for live stream status.
```Ini
Users =
```
List of Twitch users separated by `,` comma. 
```Ini
Channel = 0
```
The channel where Jinux will post Twitch live stream notifications in. If not set, Jinux will use the default channel from `Channel` config value.
```Ini
[Temporary_Channel]
Enabled = Yes
```
Toggle `Yes` or `No` to allow users to create new temporary channels.
```Ini
Time_Limit = 1d
```
Time limit on how long the temporary channels can last when created by a user. Default is `1d` which means 1 day. You can assign multiple options separated by a comma: `1d,4h` means 1 day and 4 hours.
>s = seconds, m = minutes, d = days
```Ini
Channel_Name_Limit = 10
```
The character limit of the temporary channel names that any user can make up to. Default is `10` characters.
