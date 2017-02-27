# Channel Info Command
async def ex(dclient, private_channel, public_channel, mention):
    channel = public_channel
    r = '''```Markdown
# Channel Information #
[ID]:             {}
[Name]:           {}
[Topic]:          {}
[Private]:        {}
[Position]:       {}
[Default]:        {}
[Created]:        {}```'''.format(channel.id, channel.name, channel.topic, str(channel.is_private),
                                  str(channel.position), str(channel.is_default), channel.created_at)
    await dclient.send_message(private_channel, r)
    await dclient.send_message(public_channel, '{}, the channel information has been sent in a private message.'
                               .format(mention))
