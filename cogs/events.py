import discord
from discord.ext import commands
from config.config import *
from config.embeds import Embeds
from asyncio import sleep as a_sleep
from time import sleep as t_sleep

EMBEDS = Embeds()

class Events(commands.Cog):
    '''Bot Listeners ||none'''

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        '''on ready to recieve information'''
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/cc help'))
        print(f'Bot Connected.')
        print('='*45)

    @commands.Cog.listener()
    async def on_disconnect(self):
        '''on disconnect. Not on close'''
        print('Bot Disconnected.')
        print('='*45)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        '''on command error. When error occurs from a command'''
        EMBEDS.CMDERROR.description = f'Error Occured: **{error}** on [message]({ctx.message.jump_url})'
        channel = discord.utils.get(ctx.guild.channels, id=CMD_ERROR_CHANNEL_ID)
        await channel.send(embed=EMBEDS.CMDERROR)
    
    @commands.Cog.listener()
    async def on_error(self, event_method, /, *args, **kwargs):
        '''on sys error'''
        embed = EMBEDS.syserror()
        embed.description = f'Error Occured: **{event_method}**'
        if args:
            embed.add_field(name='Arguments', field=f"`{'` `'.join(args)}`", inline=False)
        for key, value in kwargs.items():
            embed.add_field(name=key, value=f"{value}", inline=True)
        channel = discord.utils.get(self.client.get_guild(GUILD_ID).channels, id=SYS_ERROR_CHANNEL_ID)
        await channel.send(embed=EMBEDS.SYSERROR)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        '''on membber join a guild'''

        a_sleep(8)
        EMBEDS.WELCOME.description = EMBEDS.WELCOME_DESC.replace('[member.mention]', member.mention)
        await discord.utils.get(member.guild.channels, id=WELCOME_CHANNEL_ID).send(embed=EMBEDS.WELCOME)
        return
        role = discord.utils.get(member.guild.roles, id=NOT_INITIALIZED_ROLE_ID)
        if role not in member.roles:
            await member.add_roles(role)

async def setup(client: commands.Bot):
    await client.add_cog(Events(client))