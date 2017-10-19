import random


# manages -coinflip
class CoinFlip:
    async def flip_coin(self, log, dclient, msg):
        await dclient.send_message(msg.channel, '<@{}>, the coin says `{}`!'.format(msg.author.id,
                                                                                    random.choice(['heads', 'tails'])))
