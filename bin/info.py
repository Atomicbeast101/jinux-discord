import discord


# converts Rrle object to string
def get_string_roles(roles):
    s_roles = list()
    for r in roles:
        s_roles.append(r.name)
    return s_roles


# gets list of specific channels
def channel_list(server, channel_type):
    channels = list()
    for ch in server.channels:
        if ch.type == channel_type:
            channels.append(ch)
    return channels


# manages -channelinfo, -info, -serverinfo
class Info:
    async def get_channel(self, log, dclient, msg):
        channel = msg.channel
        response = '''```Markdown
# Channel Information #
[ID]:         {}
[Name]:       {}
[Topic]:      {}
[Private]:    {}
[Default]:    {}
[Created]:    {}```'''.format(channel.id,
                              channel.name,
                              channel.topic,
                              str(channel.is_private),
                              str(channel.is_Default),
                              channel.created_at)
        await dclient.send_message(msg.author, response)
        await dclient.send_message(channel, '<@{}>, the channel information has been sent in a private message.'
                                   .format(msg.author.id))

    async def get_info(self, dclient, msg):
        await dclient.send_message(msg.channel, 'I\'m a bot, obviously. My creator is Atomicbeast101 and you can find '
                                                'my source files on GitHub through here: https://github.com/atomicbeas'
                                                't101/jinux-discord')

    async def get_server(self, log, dclient, msg):
        server = discord.utils.get(dclient.servers, id=msg.channel.server.id)
        response = '''```Markdown
# Server Information #
[ID]:             {}
[Name]:           {}
[Owner]:          {}
[# Members]:      {}
[Text Channels]:  {}
[Voice Channels]: {}
[Region]:         {}
[Roles]:          {}
[Icon URL]:       {}```'''.format(server.id,
                                  server.name,
                                  discord.utils.get(server.members, id=server.owner.id).name,
                                  len(server.members),
                                  len(channel_list(server, discord.ChannelType.text)),
                                  len(channel_list(server, discord.ChannelType.voice)),
                                  server.region,
                                  ', '.join(get_string_roles(server.roles)),
                                  server.icon)
        await dclient.send_message(msg.author, response)
        await dclient.send_message(msg.channel, '<@{}>, the server information has been sent in a private message.'
                                   .format(msg.author.id))
