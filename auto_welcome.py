from datetime import datetime, timedelta

# Auto Welcome
async def welcome(dclient, member, mention, welcome_msg):
    if member.joined_at < datetime.now() - timedelta(seconds=10):
        welcome_msg.replace('{USER}', mention)
        await dclient.send_message(member, welcome_msg)
