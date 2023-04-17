from turtle import color
import discord
from os import listdir
from config.config import *
from config.embeds import Embeds
from discord.ext import commands

EMBEDS = Embeds()

class Developer(commands.Cog):
    '''Developer Commands ||dev'''

    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_mod_log(self, ctx: commands.Context, result = '**(Success!)**'):
        '''send command log to LOG channel when Moderator/Developer CMD issued'''
        if result == '**(Success!)**':
            pass
        elif result is None:
            result = '**Failed: UnAuthorised**'
        else:
             result = f', **Failed:** [error]({result})'
        EMBEDS.DEVLOG.description = \
        f"{ctx.author.name}#{ctx.author.discriminator} has used dev command `{ctx.message.content}` in {ctx.channel.mention} in [message]({ctx.message.jump_url}) {result}"
        await discord.utils.get(ctx.guild.channels, id=MODLOG_CHANNEL_ID).send(embed=EMBEDS.DEVLOG)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def load(self, ctx: commands.Context, extension):
        '''load a cog ||/cc load (cog) ||dev'''
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send(f"loaded {extension}", reference=ctx.message)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def unload(self, ctx: commands.Context, extension):
        '''unload a cog ||/cc unload (cog) ||dev'''
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"unloaded {extension}", reference=ctx.message)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def reload(self, ctx: commands.Context, extension):
        '''reload a cog ||/cc reload (cog) ||dev'''
        try:
            self.client.unload_extension(f'cogs.{extension}')
            unload=True
        except commands.ExtensionNotLoaded:
            unload=False
        finally:
            self.client.load_extension(f'cogs.{extension}')
            msg = f'reloaded {extension}' if unload else f'loaded {extension}'
            await ctx.send(msg, reference=ctx.message)
            await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def reloadall(self, ctx: commands.Context):
        '''reload all cogs ||/cc reloadall ||dev'''
        for filename in listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                except commands.ExtensionNotLoaded: pass
                self.client.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send('reloaded all cogs', reference=ctx.message)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def shutdown(self, ctx: commands.Context):
        '''shutdown the bot ||/cc shutdown ||dev'''
        await ctx.send('Shutting down...', reference=ctx.message)
        await self.send_mod_log(ctx)
        await self.client.close()
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def status(self, ctx: commands.Context, status):
        '''change bot status ||/cc status (online|idle|dnd|invisible) ||dev'''
        await self.client.change_presence(status=status)
        await ctx.send(f'Changed status to {status}', reference=ctx.message)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_role(DEVELOPER_ROLE_ID)
    async def activity(self, ctx: commands.Context, _type, *, activity):
        '''set bot activity ||/cc activity (game|song|stream) (activity) ||dev'''
        if _type == 'game':
            await self.client.change_presence(activity=discord.Game(activity))
            await ctx.send(f'Bot Playing: "{activity}"', reference=ctx.message)
        elif _type == 'song':
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
            await ctx.send(f'Bot Listning to: "{activity}"', reference=ctx.message)
        elif _type == 'stream':
            stream_name, stream_url = activity.split('|')
            await self.client.change_presence(activity=discord.Streaming(name=stream_name, url=stream_url))
            await ctx.send(f'Bot Streaming: "{stream_name}"', reference=ctx.message)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.is_owner()
    async def greet(self, ctx: commands.Context):
        '''greet owner ||/cc greet ||dev'''
        await ctx.send(f'Nice to meet you {ctx.author.mention} :heart:', reference=ctx.message)

    @load.error
    @unload.error
    @reload.error
    @reloadall.error
    @shutdown.error
    @status.error
    @activity.error
    @status.error
    async def cmd_error(self, ctx: commands.Context, error):
        '''on error when cmd run'''
        if not (isinstance(error, commands.errors.MissingRole) or isinstance(error, commands.errors.MissingPermissions)):
            #don't show error to user if user is not authorised
            reply = await ctx.send(error, reference=ctx.message)
            result = reply.jump_url
        else: result = None
        await self.send_mod_log(ctx, result)

async def setup(client: commands.Bot):
    await client.add_cog(Developer(client))