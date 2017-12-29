commands = {
    'play': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'playing': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'pause': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'stop': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'shuffle': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'queue': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'clear': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'skip': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'playlist': {
        'title': 'Music',
        'value': 'Enabled'
    },
    'volume': {
        'title': 'Music',
        'value': 'Enabled'
    },

    'gif': {
        'title': 'Commands',
        'value': 'Gif'
    },
    'cat': {
        'title': 'Commands',
        'value': 'Cat'
    },
    'choose': {
        'title': 'Commands',
        'value': 'Choose'
    },
    'dice': {
        'title': 'Commands',
        'value': 'Dice'
    },
    'dict': {
        'title': 'Commands',
        'value': 'Dictionary'
    },
    'purge': {
        'title': 'Commands',
        'value': 'Purge'
    },
    'rps': {
        'title': 'Commands',
        'value': 'Rps'
    },
    'temp': {
        'title': 'Commands',
        'value': 'Temp'
    },
    'time': {
        'title': 'Commands',
        'value': 'Time'
    },
    'uptime': {
        'title': 'Commands',
        'value': 'Uptime'
    },

    'poll': {
        'title': 'Commands',
        'value': 'Poll'
    },
    'vote': {
        'title': 'Commands',
        'value': 'Poll'
    },

    'custcmd': {
        'title': 'CustomCommands',
        'value': 'Enabled'
    },

    'remindme': {
        'title': 'Commands',
        'value': 'RemindMe'
    },
    'remindall': {
        'title': 'Commands',
        'value': 'RemindAll'
    },

    'tempch': {
        'title': 'Commands',
        'value': 'Tempch'
    },

    'xkcd': {
        'title': 'Commands',
        'value': 'Xkcd'
    },

    'help': {
        'title': 'Commands',
        'value': 'Help'
    }
}

# 0 = tie, 1 = bot win, 2 = player win
rps_result = {
    'rock_rock': {
        'response': 'I chose :left_facing_fist:...{}',
        'type': 0
    },
    'rock_paper': {
        'response': 'I chose :raised_back_of_hand:...{}',
        'type': 1
    },
    'rock_scissors': {
        'response': 'I chose :v:...{}',
        'type': 2
    },
    'paper_rock': {
        'response': 'I chose :left_facing_fist:...{}',
        'type': 2
    },
    'paper_paper': {
        'response': 'I chose :raised_back_of_hand:...{}',
        'type': 0
    },
    'paper_scissors': {
        'response': 'I chose :v:...{}',
        'type': 1
    },
    'scissors_rock': {
        'response': 'I chose :left_facing_fist:...{}',
        'type': 1
    },
    'scissors_paper': {
        'response': 'I chose :raised_back_of_hand:...{}',
        'type': 2
    },
    'scissors_scissors': {
        'response': 'I chose :v:...{}',
        'type': 0
    }
}
rps_tie_response = [
    'damn\'t! Looks like it\'s a tie...',
    'can you stop copying me?',
    'damn, you read my mind...',
    'omg. It\'s a tie!'
]
rps_bot_response = [
    'HA! I win.',
    'you fail, human!',
    'nice try.',
    'looks like your mom didn\'t raise you well.'
]
rps_player_response = [
    'oh fuck you.',
    'you think you\'re better than me?',
    'oh. Looks like you win.',
    'oh.'
]

temp_response = {
    'F_K': '`{:.1f} Fahrenheit`  >  `{:.1f} Kelvin`',
    'F_C': '`{:.1f} Fahrenheit`  >  `{:.1f} Celsius`',
    'K_F': '`{:.1f} Kelvin`  >  `{:.1f} Fahrenheit`',
    'K_C': '`{:.1f} Kelvin`  >  `{:.1f} Celsius`',
    'C_F': '`{:.1f} Celsius`  >  `{:.1f} Fahrenheit`',
    'C_K': '`{:.1f} Celsius`  >  `{:.1f} Kelvin`'
}

help_guide = {
    'play': 'Play music',
    'playing': 'See what\'s playing right now',
    'pause': 'Pause the music',
    'stop': 'Stops playing music',
    'shuffle': 'Mixes up the active playlist',
    'queue': 'Adds a new song to the active playlist',
    'skip': 'Skips to the next song in the active playlist',
    'clear': 'Clears the active song queued list',
    'playlist': 'Modify the list of custom playlists',
    'volume': 'Adjust the volume for music player',

    'gif': 'Gif based on keywords given by user',
    'cat': 'Random image/gif of cat',
    'choose': 'Choose between a list of options given by user',
    'dice': 'Roll a number between 1 and 6',
    'dict': 'Find meaning for a word',
    'purge': '**Delete a list of messages from a channel',
    'rps': 'Play rock, paper, scissors with Jinux',
    'temp': 'Convert the temperature between Celsius, Fahrenheit, & Kelvin',
    'time': 'Get the current time in a location given by user',
    'uptime': 'How long Jinux has been up since it\'s boot time',

    'poll': 'Create/Delete a poll for users to vote',
    'vote': 'Vote on an option in an active poll',

    'custcmd': 'Create/Edit/Delete a custom command with a message',

    'remindme': 'Create a personal reminder',
    'remindall': 'Create a reminder for everyone in a channel',

    'tempch': 'Create a temporary text/voice channel',

    'xkcd': 'Get latest or specific XKCD comic',

    'help': 'Help guide on how to use Jinux\'s commands'
}

full_help_guide = {
    'play': {
        'desc': 'Play music',
        'usage': {
            'play': 'Play the music',
            'play <youtube_url>': 'Force play a song'
        }
    },
    'playing': {
        'desc': 'See what song Jinux is playing',
        'usage': {
            'playing': 'See current song playing'
        }
    },
    'pause': {
        'desc': 'Pause an active song in play',
        'usage': {
            'pause': 'Pause the music player'
        }
    },
    'stop': {
        'desc': 'Stop Jinux from playing any music',
        'usage': {
            'stop': 'Stop the music player'
        }
    },
    'shuffle': {
        'desc': 'Shuffle a list of active playlist',
        'usage': {
            'shuffle': 'Shuffle the active playlist'
        }
    },
    'queue': {
        'desc': 'Add a song to the active playlist to be played next',
        'usage': {
            'queue <youtube_url>': 'Add a song to the playlist'
        }
    },
    'clear': {
        'desc': 'Clears the active song queued list',
        'usage': {
            'clear': 'Clears the list'
        }
    },
    'skip': {
        'desc': 'Skip to the next song in the active playlist',
        'usage': {
            'skip': 'Skip to the next song in the playlist'
        }
    },
    'playlist': {
        'desc': 'Manage the custom playlists',
        'usage': {
            'playlist': 'List the songs in the active playlist',
            'playlist all': 'List all playlists from the database.',
            'playlist list <name>': 'List the songs in a playlist',
            'playlist load <name>': 'Load the list of songs to the active playlist',
            'playlist create <name>': 'Create a new playlist',
            'playlist remove <name>': 'Remove a playlist',
            'playlist edit <name> add <youtube_url>': 'Add a song to the playlist',
            'playlist edit <name> remove <youtube_id>': 'Remove a song from the playlist',
            'playlist empty <name>': 'Empty the songs in the playlist'
        }
    },
    'volume': {
        'desc': 'Adjust the volume level for the music player',
        'usage': {
            'volume <#>': 'Change the volume between 1 and 200'
        }
    },
    'gif': {
        'desc': 'Gif based on keywords given by user',
        'usage': {
            'gif <keywords...>': 'Find gif based on the keywords'
        }
    },
    'cat': {
        'desc': 'Random image/gif of cat',
        'usage': {
            'cat': 'Random image/gif of cat'
        }
    },
    'choose': {
        'desc': 'Choose between a list of options given by user',
        'usage': {
            'choose <options by |>': 'Have Jinux choose an option from the list'
        }
    },
    'dice': {
        'desc': 'Roll a number between 1 and 6',
        'usage': {
            'dice': 'Roll the dice and get a number between 1 and 6'
        }
    },
    'dict': {
        'desc': 'Find meaning for a word',
        'usage': {
            'dict <word>': 'Get meaning for that word'
        }
    },
    'purge': {
        'desc': 'Delete a list of messages from a channel',
        'usage': {
            'purge all <#>': 'Delete a # of messages in the current channel',
            'purge user <id> <#>': 'Delete a # of user\'s messages in the current channel',
            'purge today': 'Delete all messages that were posted today'
        }
    },
    'rps': {
        'desc': 'Play rock, paper, scissors with Jinux',
        'usage': {
            'rps <rock|paper|scissors>': 'Choose an option between rock, paper, scissors'
        }
    },
    'temp': {
        'desc': 'Convert the temperature between Celsius, Fahrenheit, & Kelvin',
        'usage': {
            'temp <#> <from F|K|C> <to F|K|C>': 'Convert temperature between C, F, and K'
        }
    },
    'time': {
        'desc': 'Get the current time in a location given by user',
        'usage': {
            'time <location>': 'Get current time in a location (Uses Google Maps)'
        }
    },
    'uptime': {
        'desc': 'How long Jinux has been up since it\'s boot time',
        'usage': {
            'uptime': 'Get Jinux\'s uptime'
        }
    },
    'poll': {
        'desc': 'Create/Delete a poll for users to vote',
        'usage': {
            'poll start <option by |> <question...>': 'Create a new poll',
            'poll stop': 'Stop the active poll'
        }
    },
    'vote': {
        'desc': 'Vote on an option in an active poll',
        'usage': {
            'vote <option>': 'Vote on an option'
        }
    },
    'custcmd': {
        'desc': 'Create/Edit/Delete a custom command with a message',
        'usage': {
            'custcmd add <name> <message>': 'Create a new custom command',
            'custcmd set <name> <message>': 'Set a new message for the custom command',
            'custcmd remove <name>': 'Remove the custom command that you made',
            'custcmd list': 'List all custom commands'
        }
    },
    'remindme': {
        'desc': 'Create a personal reminder',
        'usage': {
            'remindme <time> <message...>': 'Create a new personal reminder'
        }
    },
    'remindall': {
        'desc': 'Create a reminder for everyone in a channel',
        'usage': {
            'remindall <time> <message...>': 'Create a reminder for everyone in the current channel'
        }
    },
    'tempch': {
        'desc': 'Create a temporary text/voice channel',
        'usage': {
            'tempch create <voice|text> <time> <name>': 'Create a new temporary channel',
            'tempch remove <name>': 'Remove the temporary channel',
            'tempch list': 'List all active temporary channels'
        }
    },
    'xkcd': {
        'desc': 'Get latest or specific XKCD comic',
        'usage': {
            'xkcd latest': 'Get latest XKCD comic',
            'xkcd <comic ID>': 'Get specific comic based on ID'
        }
    },
    'help': {
        'desc': 'Help guide on how to use Jinux\'s commands',
        'usage': {
            'help': 'List all commands Jinux can do',
            'help <command>': 'Detailed help guide for specific command'
        }
    }
}
