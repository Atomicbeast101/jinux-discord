from datetime import datetime, timedelta

# auto welcome
async def welcome(enabled, dclient, member, mention, welcome_msg):
    if enabled:
        if member.joined_at < datetime.now() - timedelta(seconds=10):
            welcome_msg = welcome_msg.replace('{USER}', mention)
            await dclient.send_message(member, welcome_msg)
