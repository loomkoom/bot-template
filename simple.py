import discord
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = ''

"""	
Privileged Intents (Needs to be enabled on developer portal of Discord):
intents.members, intents.message_content, intents.presences
"""
intents = discord.Intents.default()

# message content for prefix commands
intents.message_content = True

bot = Bot(
    command_prefix=commands.when_mentioned_or("$$"),
    intents=intents,
    help_command=None,
)

@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    channel = bot.get_channel(12324234183172)
    await channel.send(f"Bot logged in as {bot.user.name}")


bot.run(TOKEN)
