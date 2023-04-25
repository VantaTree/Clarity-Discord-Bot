import discord
from pytube import YouTube, Channel, Playlist, exceptions
from random import choice
from asyncio import sleep
from .config import *
from .embeds import Embeds
from discord.ext import commands
from discord import app_commands as app_cmds


async def sync_bot(client: commands.Bot):
    
    try:        
        synced = await client.tree.sync()
        msg = F"Synced {len(synced)} command(s)"
    except Exception as e:
        msg = str(e)

    return msg

def is_dev() -> bool:

    def predicate(interaction: discord.Interaction) -> bool:
        return  interaction.user.get_role(DEVELOPER_ROLE_ID)
    return app_cmds.check(predicate)

def is_owner() -> bool:

    def predicate(interaction: discord.Interaction) -> bool:
        return  interaction.user.id == OWNER_ID
    return app_cmds.check(predicate)