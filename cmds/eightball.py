import aiohttp


# 8ball command
async def ex(dclient, channel, mention, question, cmd_char):
    if len(question.split(' ')) >= 1:
        question.replace(' ', '%')
        question.replace('?', '%3F')
        question.replace(',', '%2C')
        async with aiohttp.ClientSession() as s:
            async with s.get('https://8ball.delegator.com/magic/JSON/{}'.format(question)) as r:
                d = await r.json()
                await dclient.send_message(channel, '{}, {}'.format(mention, d['magic']['answer']))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}8ball <Question...>'.format(mention, cmd_char))
