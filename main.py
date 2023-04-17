import discord
from os import listdir
import asyncio
# import uptime
from discord.ext import commands
from config.config import *

intents = discord.Intents.all()

client = commands.Bot(command_prefix=PREFIXES, intents=intents)
client.remove_command('help')

async def load_all_extensions():
    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

# uptime.keep_alive()
asyncio.run(load_all_extensions())
client.run(TOKEN) #Bot to be used in a single Server(Configured in config.py)