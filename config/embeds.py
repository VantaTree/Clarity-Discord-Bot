from discord import Embed
from .config import *

class Embeds:
    def __init__(self):
        self.WELCOME_DESC = f"Hi I am Clarity, [member.mention] Welcome to Clear Code's server\nTo get started, please go to <#{ROLES_CHANNEL_ID}> and get yourself the Competence roles\nThen you can start chatting in the Server"
        self.DEVLOG = self.logdev()
        self.MODLOG = self.logmod()
        self.CMDERROR = self.cmderror()
        self.SYSERROR = self.syserror()
        self.WELCOME = self.welcome()
        self.PING = self.ping()
        self.VERSION = self.version()
        self.TOKEN = self.token()
        self.CODE = self.code()
        self.PASTE = self.paste()
        self.SYNTAX = self.syntax()

    def logdev(self):
        embed = Embed(
            title="Dev Command Issued",
            description="lorem ipsum",
            color=0xffaec8
        )
        return embed

    def logmod(self):
        embed = Embed(
            title="Mod Command Issued",
            description="lorem ipsum",
            color=0xffaec8
        )
        return embed

    def cmderror(self):
        embed = Embed(
            title="Command Error",
            description="lorem ipsum",
            color=0xffaec8
        )
        return embed

    def syserror(self):
        embed = Embed(
            title="System Error",
            description="lorem ipsum",
            color=0xffaec8
        )
        return embed

    def welcome(self):

        embed = Embed(
            title='Welcome',
            description=self.WELCOME_DESC,
            color=0xffaec8
        )
        embed.set_footer(text='Welcome message sent automatically')
        return embed

    def ping(self):

        embed = Embed(
            title='Pong!',
            description=f'lorem ipsum',
            color=0xffaec8
        )
        return embed

    def version(self):

        embed = Embed(
            title='Bot Version',
            description=f'lorem ipsum',
            color=0xffaec8
        )
        return embed

    def token(self):

        embed = Embed(
            title='Bot Token',
            description=f'lorem ipsum',
            color=0xffaec8
        )
        return embed

    def code(self):
            
        embed = Embed(
            title='Format Code',
            description=f'You can format code on discord like so:',
            color=0xffaec8
        )
        embed.add_field(name='Syntax', value='\```py <or any other lang>\nprint ("Hello World")\n```', inline=False)
        embed.add_field(name='Output', value='```py\nprint ("Hello World")\n```', inline=False)
        return embed

    def syntax(self):
            
        embed = Embed(
            title='Syntax For My Commands',
            description=f'```</cc | /clear> <command> (args) [optional args]```\ndifferent for each command, You can see the commands and their parameters with **`/cc help (command)`**',
            color=0xffaec8
        )
        return embed

    def paste(self):
            
        embed = Embed(
            title='Paste Code Online',
            description='If you have a **large** amount of code you want to show, you can paste it on this website: **https://paste.pythondiscord.com/**. Paste your code on the website and press **Ctrl+S** to save it, then you can copy the link and send it here.',
            color=0xffaec8
        )
        return embed
