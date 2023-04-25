import discord
from os import getenv
import asyncio
# import uptime
from discord import app_commands
from discord.ext import commands
from config.config import *

TOKEN = getenv("TOKEN")

intents = discord.Intents.all()

client = commands.Bot(command_prefix=PREFIXES, intents=intents)
client.remove_command('help')

async def load_all_extensions():
    for filename in COGS:
        await client.load_extension(f'cogs.{filename}')


if __name__ == "__main__":
    # uptime.keep_alive()
    asyncio.run(load_all_extensions())
    client.run(TOKEN) #Bot to be used in a single Server(Configured in config.py)
