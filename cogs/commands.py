import discord
from discord import app_commands as app_cmds
from discord.ext import commands
from random import choice
from asyncio import sleep
from pytube import YouTube, Channel, Playlist, exceptions
from config.config import *
from config.embeds import Embeds
from config.support import *

EMBEDS = Embeds()

class General(commands.Cog):
    '''General Commands'''

    def __init__(self, client: commands.Bot):
        self.client = client
    
    @app_cmds.command(description="repeat user's message")
    async def say(self, interaction:discord.Interaction, message:str):
        '''repeat user's message ||/cc say (message)'''
        await interaction.response.send_message(f'<{interaction.user.mention}>: {message}')

    @app_cmds.command(description="show how to format code on dicord")
    async def code(self, interaction:discord.Interaction):
        '''show how to format code on dicord ||/cc code'''
        await interaction.response.send_message(embed=EMBEDS.CODE)

    @app_cmds.command(description="direct someone on how to show large amount of code online")
    async def paste(self, interaction:discord.Interaction):
        '''direct someone on how to show large amount of code online ||/cc paste'''
        await interaction.response.send_message(embed=EMBEDS.PASTE)

    # @app_cmds.command(description="show syntax for my command")
    # @commands.command()
    # async def syntax(self, interaction:discord.Interaction):
    #     '''show syntax for my commands ||/cc syntax'''
    #     await interaction.response.send_message(embed=EMBEDS.SYNTAX)

class BotInfo(commands.Cog):
    '''Bot's Information Commands'''

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_cmds.command(description="show bot's latency")
    async def ping(self, interaction:discord.Interaction):
        '''show bot's latency ||/cc ping'''
        EMBEDS.PING.description = f'Ping: **{round(self.client.latency * 1000)}**ms'
        await interaction.response.send_message(embed=EMBEDS.PING)

    @app_cmds.command(description="show bot's version")
    async def version(self, interaction:discord.Interaction):
        '''show bot's version ||/cc version'''
        EMBEDS.VERSION.description = f'**{BOT_VERSION}**'
        await interaction.response.send_message(embed=EMBEDS.VERSION)

    @app_cmds.command(description="show bot's token")
    async def token(self, interaction:discord.Interaction):
        '''show bot's token ||/cc token'''
        fake_token = ''.join([choice(ALLTEXT) for _ in range(55)])
        EMBEDS.TOKEN.description = f'**{fake_token}**'
        await interaction.response.send_message(embed=EMBEDS.TOKEN)

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

    @app_cmds.command(description="play an animation")
    @app_cmds.choices(animation=[
        app_cmds.Choice(name="countdown", value="countdown"),
        app_cmds.Choice(name="text", value="text"),
        ])
    async def animation(self, interaction: discord.Interaction, animation:str):
        '''play an animation ||/cc animation (countdown|text)'''
        if animation == 'countdown':
            await interaction.response.send_message("5")
            for i in range(4,-1,-1):
                await sleep(1)
                await interaction.edit_original_response(content=str(i))
            await sleep(1)
            await interaction.edit_original_response(content="BOOM!")

        elif animation == 'text':
            await interaction.response.send_message(".")
            text = choice(self.texts)
            for i in text.replace(' ', '.'):
                await interaction.edit_original_response(content=i)
                await sleep(0.8)
            await interaction.edit_original_response(content=text)

class WebInfo(commands.Cog):
    '''Get Information from Web'''

    def __init__(self, client):
        self.client = client

    @app_cmds.command(description="show info on a Youtube video")
    async def video(self, interaction: discord.Interaction, vid_url:str):
        '''show info on a Youtube video ||/cc video (url)'''
        try:
            error=None
            video = YouTube(vid_url)
            embed = discord.Embed(title=video.title, description=f"**description:**\n{video.description[:150]}...", color=0xff0000)
            embed.set_author(name=video.author)
            embed.set_image(url=video.thumbnail_url)
            n = '\n'
            embed.add_field(name='Info:-', value=f"**Duration:** {video.length//60}:{video.length%60} {n}**Views:** {video.views} {n}**Date Published:** {video.publish_date.date()} {f'{n}**Rating:** {video.rating}' if video.rating else ''}", inline=False)
            await interaction.response.send_message(embed=embed)
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
        except Exception as e:
            error = str(e)
        finally:
            if error:
                await interaction.response.send_message(error)

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
