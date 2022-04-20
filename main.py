import discord
from os import listdir
from discord.ext import commands
from config.config import *

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=PREFIXES, intents=intents)
client.remove_command('help')
[client.load_extension(f'cogs.{filename[:-3]}') for filename in listdir('./cogs') if filename.endswith('.py')]

client.run(TOKEN) #Bot to be used in a single Server(Configured in config.py)