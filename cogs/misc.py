import discord
from discord.ext import commands
from config.config import *
from asyncio import sleep

class Misc(commands.Cog):
    '''Specific Commands for Incredibelly Specific USE ||dev'''

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def run(self, ctx: commands.Context):
        '''run(Configured in Code) ||/cc run ||dev'''
        await ctx.send(f"Run Set To Announce Bot Arival", reference=ctx.message)
        embed = discord.Embed(title="Clarity Has Arrived", description="@everyone Clear Code's Personal Clarity Bot has arrived. type **`/cc help`** to start", color=0xffaec8)
        embed.set_thumbnail(url='https://i.imgur.com/9YnS9OX.jpg')

        await discord.utils.get(ctx.guild.text_channels, id=ANNOUNCEMENT_CHANNEL_ID).send(embed=embed)


async def setup(client):
    await client.add_cog(Misc(client))
