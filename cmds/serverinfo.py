import discord


# Convert Role Object to String
def get_string_roles(roles):
    s_roles = list()
    for r in roles:
        s_roles.append(r.name)
    return s_roles


# Get List of Specific Channels
def channel_list(server, channel_type):
    channels = list()
    for ch in server.channels:
        if ch.type == channel_type:
            channels.append(ch)
    return channels


# Server Info Command
async def ex(dclient, private_channel, public_channel, mention):
    server = discord.utils.get(dclient.servers, id=private_channel.server.id)
    r = '''```Markdown
# Server Information #
[ID]:             {}
[Name]:           {}
[Owner]:          {}
[Members]:        {}
[Text Channels]:  {}
[Voice Channels]: {}
[Region]:         {}
[Roles]:          {}
[Icon]:           {}```'''.format(server.id, server.name, discord.utils.get(server.members, id=server.owner.id).name,
                                  len(server.members), len(channel_list(server, discord.ChannelType.text)),
                                  len(channel_list(server, discord.ChannelType.voice)), server.region,
                                  ', '.join(get_string_roles(server.roles)), server.icon)
    await dclient.send_message(private_channel, r)
    msg = await dclient.send_message(public_channel, '{}, the server information has been sent in a private message.'
                               .format(mention))
    return msg
