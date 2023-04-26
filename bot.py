import json
import os
import platform
import random
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

"""	
Privileged Intents (Needs to be enabled on developer portal of Discord):
intents.members, intents.message_content, intents.presences
"""
intents = discord.Intents.default()

# message content for prefix commands
intents.message_content = True

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)
bot.config = config


@bot.event
async def on_ready() -> None:
    """
    The code in this event is executed when the bot is ready.
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name}) {platform.architecture()[0]}")
    print(f"CPU architecture: {platform.machine()}")
    print(f"Current directory: {os.getcwd()}")
    print("-------------------")
    print("Bot is present in the following guilds:")
    for guild in bot.guilds:
        print(f"{guild.name} (ID: {guild.id})")
    print("-------------------")
    status_task.start()


@bot.hybrid_command(name="sync", description="sync slash commands")
@commands.guild_only()
@commands.is_owner()
async def sync(ctx, scope: str = "local"):
    if scope == "local":
        guild = discord.Object(id=ctx.guild.id)
        bot.tree.copy_global_to(guild=guild)
        print(f"Syncing commands for guild: {ctx.guild.id}...")
        synced = await bot.tree.sync(guild=guild)
        await ctx.send(f"Synced {len(synced)} commands to the current guild.")

    else:
        print("Syncing commands globally...")
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands globally.")

    return


@bot.tree.command(name="slash",
                  description="My first application Command")
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot.
    """
    statuses = ["with humans!", "with my code!", "with my owner!", "with my friends!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        print(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        print(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    embed = discord.Embed(
        title="Error!",
        description=str(error).capitalize(),
        color=0xE02B2B,
    )
    await context.send(embed=embed)


bot.run(config["token"])
