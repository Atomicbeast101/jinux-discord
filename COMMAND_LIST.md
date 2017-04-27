## Commands
> Keywords: cmd = command, msg = message, curr = currency

> Command Syntax: <..> means it's required while (...) means it's optional

> If <option1|option2> means you have to choose between option1 or option2.

| Command | Access | Description |
|:-------:|--------|-------------|
| `cat` | User | Random picture or gif of a cat. |
| `channelinfo` | User | Information about the channel you are in. |
| `choose <options>` | User | Random chooses an option from the list. |
| `chucknorris` | User | Random Chuck Norris jokes. |
| `coinflip` | User | Flip a coin to receive heads or tails. |
| `conspiracy` | User | Random conspiracy. |
| `custcmd <cmd> <msg...>` | Admin | Create a custom `command` with a custom message! |
| `convert <amount#> <curr-code> <curr-code>` | User | Convert currency. |
| `dice` | User | Randomly chooses a number between 1 to 6. |
| `dictionary <term>` | User | Grab meaning of a given term. |
| `8ball <question...>` | User | Magic eight ball answering machine. |
| `gif (tags)` | User | Gets a GIF from Giphy according to the tags given. |
| `help (command)` | User | Lists commands and description for each. |
| `info` | User | Information about this bot. |

| `poll <start|stop> <question...>` | Admin | Create or stop polls. |
| `vote <option>` | User | Vote an option to the poll. |
| `reddit <#-subs OR subreddit> <#-subs>` | User | Get hottest submissions from front page or subreddit. |
| `remindall <time> <msg...>` | User | Set a reminder for everyone in the same channel you sent the message in. |
| `remindme <time> <msg...>` | User | Set a reminder for Jinux to message you through private message. |
| `rps <rock|paper|scissors>` | User | Rock, paper, scissors game. |
| `serverinfo` | User | Information about the server you are in. |
| `temp <temp-#> <K|F|C> <K|F|C>` | User | Convert temperature between F, K, or C. |
| `tempch <voice|text> <time> <channel-name>` | User | Create a temporary channel that'll be public for a time limit! |
| `time <location>` | User | Get current time according to timezone. |
| `trans <language-code> <msg-to-translate>` | User | Translate message to desired language. |
| `twitch <add|remove|list|toggle|setchannel> <userID OR channelID>` | User/Admin | Twitch live stream notification. |
| `uptime` | User | Jinux's uptime status. |
| `xkcd <comicID OR latest>` | User | Gets random or latest comic from xkcd.com website. |
| `youtube <to-search>` | User | Gets first video from YouTube search results. |

> Administrators only have access to . Users can do `-twitch list`. 

List of translate codes: [https://www.sitepoint.com/web-foundations/iso-2-letter-language-codes/](https://www.sitepoint.com/web-foundations/iso-2-letter-language-codes/)

List of currency codes: [https://currencysystem.com/codes/](https://currencysystem.com/codes/)

Timezone is based on user's location input (uses google maps to determine the timezone).
