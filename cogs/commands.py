import discord
from pytube import YouTube, Channel, Playlist, exceptions
from random import choice
from asyncio import sleep
from config.config import *
from config.embeds import Embeds
from discord.ext import commands

EMBEDS = Embeds()
ALLTEXT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-'

class General(commands.Cog):
    '''General Commands'''

    def __init__(self, client: commands.Bot):
        self.client = client
    
    @commands.command()
    async def say(self, ctx, *, message=''):
        '''repeat user's message ||/cc say (message)'''
        await ctx.send(f'{ctx.author.mention}: {message}')

    @commands.command()
    async def code(self, ctx):
        '''show how to format code on dicord ||/cc code'''
        await ctx.send(embed=EMBEDS.CODE, reference=ctx.message)

    @commands.command()
    async def paste(self, ctx):
        '''direct someone on how to show large amount of code online ||/cc paste'''
        await ctx.send(embed=EMBEDS.PASTE, reference=ctx.message)

    @commands.command()
    async def syntax(self, ctx):
        '''show syntax for my commands ||/cc syntax'''
        await ctx.send(embed=EMBEDS.SYNTAX, reference=ctx.message)

class BotInfo(commands.Cog):
    '''Bot's Information Commands'''

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        '''show bot's latency ||/cc ping'''
        EMBEDS.PING.description = f'Ping: **{round(self.client.latency * 1000)}**ms'
        await ctx.send(embed=EMBEDS.PING, reference=ctx.message)

    @commands.command()
    async def version(self, ctx):
        '''show bot's version ||/cc version'''
        EMBEDS.VERSION.description = f'**{BOT_VERSION}**'
        await ctx.send(embed=EMBEDS.VERSION, reference=ctx.message)

    @commands.command()
    async def token(self, ctx):
        '''show bot's token ||/cc token'''
        fake_token = ''.join([choice(ALLTEXT) for _ in range(55)])
        EMBEDS.TOKEN.description = f'**{fake_token}**'
        await ctx.send(embed=EMBEDS.TOKEN, reference=ctx.message)

class Fun(commands.Cog):
    '''Misc Commands'''

    def __init__(self, client: commands.Bot):
        self.client = client
        self.target_msg = None
        self.texts = ['Clear Code', 'Clarity', 'Discord.py', 'VantaTree', 'Minecraft', 'Go Study']

    def anim(self, _type):
        if _type == 'explode':
            for i in range(10, 0, -1):
                yield f"[]{'.'*i}"
            for string in ('[]', '[=]', '[==]', '[=o=]', '[=O=]', '[=0=]', '[  ()  ]', '(   .   )'):
                yield string

    @commands.command()
    async def animation(self, ctx: commands.context, animation):
        '''play an animation ||/cc animation (countdown|text)'''
        if self.target_msg: return
        if animation == 'countdown':
            self.target_msg = await ctx.send(f'5')
            for i in range(4,-1,-1):
                await sleep(1)
                await self.target_msg.edit(content=str(i))
            await sleep(1)
            await self.target_msg.edit(content='BOOM!')
            self.target_msg = None

        elif animation == 'text':
            self.target_msg = await ctx.send(f'.')
            text = choice(self.texts)
            for i in text.replace(' ', '.'):
                await self.target_msg.edit(content=i)
                await sleep(0.8)
            await self.target_msg.edit(content=text)
            self.target_msg = None

class WebInfo(commands.Cog):
    '''Get Information from Web'''

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def video(self, ctx, vid_url):
        '''show info on a Youtube video ||/cc video (url)'''
        try:
            error=None
            video = YouTube(vid_url)
            embed = discord.Embed(title=video.title, description=f"{video.description[:150]}...", color=0xff0000)
            embed.set_author(name=video.author)
            embed.set_image(url=video.thumbnail_url)
            n = '\n'
            embed.add_field(name='Info', value=f"**Duration:** {video.length//60}:{video.length%60} {n}**Views:** {video.views} {n}**Date Published:** {video.publish_date.date()} {f'{n}**Rating:** {video.rating}' if video.rating else ''}", inline=False)
            await ctx.send(embed=embed, reference=ctx.message)
        except exceptions.RegexMatchError:
            error = f'Bad Youtube video URL'
        except exceptions.MembersOnly:
            error = f'Video is restricted to members only'
        except exceptions.LiveStreamError:
            error = f"Can't get video info from live stream"
        except exceptions.VideoPrivate:
            error = f"Video is private"
        except exceptions.VideoRegionBlocked:
            error = f"Video is blocked in BOT's region"
        except exceptions.AgeRestrictedError:
            error = f"Video is age restricted"
        except exceptions.VideoUnavailable:
            error = f"Video is unavailable"
        finally:
            if error:
                await ctx.send(error, reference=ctx.message)

    # @commands.command()
    # async def channel(self, ctx, channel_url):
    #     try:
    #         error=None
    #         ch = Channel(channel_url)
    #         n = '\n'
    #         embed = discord.Embed(title=f'{ch.channel_name}', description=f"...", color=0xff0000)
    #         embed.url = channel_url
    #         embed.set_author(name='YouTube')
    #         embed.add_field(name='Info', value=f"**Videos:**{len(ch.videos)}")
    #         # embed.set_image(url=ch.thumbnail_url)
    #         await ctx.send(embed=embed, reference=ctx.message)
    #     except exceptions.RegexMatchError:
    #         error = f'Bad Youtube Channel URL'
    #     finally:
    #         if error:
    #             await ctx.send(error, reference=ctx.message)



async def setup(client: commands.Bot):
    await client.add_cog(General(client))
    await client.add_cog(Fun(client))
    await client.add_cog(BotInfo(client))
    await client.add_cog(WebInfo(client))
