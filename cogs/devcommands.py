from turtle import color
import discord
from os import listdir
from config.config import *
from config.embeds import Embeds
from config.support import *
from discord.ext import commands

EMBEDS = Embeds()

class Developer(commands.Cog):
    '''Developer Commands ||dev'''

    def __init__(self, client: commands.Bot):
        self.client = client

    async def send_mod_log(self, interaction: discord.Interaction):
        '''send command log to LOG channel when Moderator/Developer CMD issued'''

        if interaction.user.get_role(DEVELOPER_ROLE_ID) is None:
            result = '**(Failed: UnAuthorized)**'
        elif interaction.command_failed:
            result = '**(Failed)**' 
        else: result = '**(Success!)**'

        options = ', '.join([F'{cmd["name"]}: {cmd["value"]}' for cmd in interaction.data.get("options", [])])
        info = F"/{interaction.data['name']} { options}"
        EMBEDS.DEVLOG.description = \
        f"{interaction.user.name}#{interaction.user.discriminator} has used dev command `{info}` in {interaction.channel.mention} {result}"
        await discord.utils.get(interaction.guild.channels, id=MODLOG_CHANNEL_ID).send(embed=EMBEDS.DEVLOG)

    @app_cmds.command(description="sync slash commands")
    @is_dev()
    async def sync(self, interaction: discord.Interaction):
        '''sync slash commands ||/cc sync ||dev'''
        await interaction.response.send_message(await sync_bot(self.client), ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="load a cog")
    @app_cmds.describe(extension="cog")
    @app_cmds.choices(extension=[app_cmds.Choice(name=cog, value=cog) for cog in COGS])
    @is_dev()
    async def load(self, interaction: discord.Interaction, extension:str):
        '''load a cog ||/cc load (cog) ||dev'''
        await self.client.load_extension(f'cogs.{extension}')
        await interaction.response.send_message(f"loaded {extension}", ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="unload a cog")
    @app_cmds.describe(extension="cog")
    @app_cmds.choices(extension=[app_cmds.Choice(name=cog, value=cog) for cog in COGS])
    @is_dev()
    async def unload(self, interaction: discord.Interaction, extension:str):
        '''unload a cog ||/cc unload (cog) ||dev'''
        await self.client.unload_extension(f'cogs.{extension}')
        await interaction.response.send_message(f"unloaded {extension}", ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="reload a cog")
    @app_cmds.describe(extension="cog")
    @app_cmds.choices(extension=[app_cmds.Choice(name=cog, value=cog) for cog in COGS])
    @is_dev()
    async def reload(self, interaction: discord.Interaction, extension:str):
        '''reload a cog ||/cc reload (cog) ||dev'''
        try:
            await self.client.unload_extension(f'cogs.{extension}')
            unload=True
        except commands.ExtensionNotLoaded:
            unload=False
        finally:
            await self.client.load_extension(f'cogs.{extension}')
            msg = f'reloaded {extension}' if unload else f'loaded {extension}'
            await interaction.response.send_message(msg, ephemeral=True)
            await self.send_mod_log(interaction)

    @app_cmds.command(description="reload all cog")
    @is_dev()
    async def reloadall(self, interaction: discord.Interaction):
        '''reload all cogs ||/cc reloadall ||dev'''
        for filename in COGS:
            try:
                await self.client.unload_extension(f'cogs.{filename}')
            except commands.ExtensionNotLoaded: pass
            await self.client.load_extension(f'cogs.{filename}')
        await interaction.response.send_message('reloaded all cogs', ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="shutdown the bot")
    @is_dev()
    async def shutdown(self, interaction: discord.Interaction):
        '''shutdown the bot ||/cc shutdown ||dev'''
        await interaction.response.send_message('Shutting down...', ephemeral=True)
        await self.send_mod_log(interaction)
        await self.client.close()

    @app_cmds.command(description="change bot's presence")
    @app_cmds.describe(presence="status")
    @app_cmds.choices(presence=[
        app_cmds.Choice(name="online", value="online"),
        app_cmds.Choice(name="idle", value="idle"),
        app_cmds.Choice(name="dnd", value="dnd"),
        app_cmds.Choice(name="invisible", value="invisible"),
        ])
    @is_dev()
    async def presence(self, interaction: discord.Interaction, presence:str):
        '''change bot's presence ||/cc status (online|idle|dnd|invisible) ||dev'''
        await self.client.change_presence(status=presence)
        await interaction.response.send_message(f'Changed presence to {presence}', ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="set bot's activity")
    @app_cmds.describe(type="activity type", activity="activity")
    @app_cmds.choices(type=[
        app_cmds.Choice(name="game", value="game"),
        app_cmds.Choice(name="song", value="song"),
        app_cmds.Choice(name="stream", value="stream"),
        ])
    @is_dev()
    async def activity(self, interaction: discord.Interaction, type:str, activity:str):
        '''set bot's activity ||/cc activity (game|song|stream) (activity) ||dev'''
        msg = "Error not able to set activity"
        if type == "game":
            await self.client.change_presence(activity=discord.Game(activity))
            msg = f"Bot Playing: **{activity}**"
        elif type == 'song':
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity))
            msg = f"Bot Listning to: **{activity}**"
        elif type == 'stream':
            stream_name, stream_url = activity.split('|')
            await self.client.change_presence(activity=discord.Streaming(name=stream_name, url=stream_url))
            msg = f"Bot Streaming: **{stream_name}**"
        await interaction.response.send_message(msg, ephemeral=True)
        await self.send_mod_log(interaction)

    @app_cmds.command(description="greet owner")
    @is_owner()
    async def greet(self, interaction: discord.Interaction):
        '''greet owner ||/cc greet ||dev'''
        await interaction.response.send_message(f"Nice to meet you {interaction.user.mention} Senpai :heart:")

    @load.error
    @unload.error
    @reload.error
    @reloadall.error
    @shutdown.error
    @presence.error
    @activity.error
    # @status.error
    async def cmd_error(self, interaction: discord.Interaction, error):
        '''on error when cmd run'''
        # if not (isinstance(error, commands.errors.MissingRole) or isinstance(error, commands.errors.MissingPermissions)):
        #     #don't show error to user if user is not authorised
        #     reply = await interaction.response.send_message(error, ephemeral=True)
        #     result = reply.jump_url
        # else: result = None
        await self.send_mod_log(interaction)

async def setup(client: commands.Bot):
    await client.add_cog(Developer(client))