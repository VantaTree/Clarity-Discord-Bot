from discord.ext import commands
from config.config import *
from discord import Embed
import discord
# from config.embeds import Embeds

class Help(commands.Cog):
    '''Help Command'''

    def __init__(self, client: commands.Bot):
        self.client = client

    def role_check(self, ctx, role):
        if role == 'dev':
            role = discord.utils.get(ctx.guild.roles, id=DEVELOPER_ROLE_ID)
            if role in ctx.author.roles:
                return True
        elif role == 'mod':
            role1 = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE_ID)
            role2 = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE_ID)
            if role1 in ctx.author.roles or role2 in ctx.author.roles:
                return True
        elif role == 'none': return False
        else: return True

    @commands.command()
    async def help(self, ctx, *entry):
        '''show help for dedicated entry ||/cc help (entry(s))'''
        #how is cmd desc confiured?
        # desc ||usage ||check
        #check=> dev: has dev role, mod: has permission, owner: is owner
        if not entry:
            embed = Embed(title='Help', description='Description for all Categories', color=0xffaec8)
            for cog in self.client.cogs:
                desc = self.client.cogs[cog].__doc__.split('||')
                if not self.role_check(ctx, desc[-1]): continue
                value = desc[0]
                lst = [command.name for command in self.client.get_cog(cog).get_commands() if self.role_check(ctx, command.help.split("||")[-1])]
                if lst: value += f'\nCommands: **`{"` `".join(lst)}`**'
                embed.add_field(name=cog, value=value, inline=False)
            await ctx.send(embed=embed, reference=ctx.message)

        elif len(entry) == 1:
            for cog in self.client.cogs:
                if cog.lower() == entry[0].lower():
                    desc = self.client.cogs[cog].__doc__.split('||')
                    if not self.role_check(ctx, desc[-1]): return
                    embed = Embed(title=cog, description=desc[0], color=0xffaec8)
                    for command in self.client.get_cog(cog).get_commands():
                        if not self.role_check(ctx, command.help.split("||")[-1]): continue
                        embed.add_field(name=command.name, value=command.help.split("||")[0], inline=False)
                    await ctx.send(embed=embed, reference=ctx.message)
                    break

            else:
                for cog in self.client.cogs:
                    for command in self.client.get_cog(cog).get_commands():
                        if command.name.lower() == entry[0].lower():
                            desc = command.help.split("||")
                            if not self.role_check(ctx, desc[-1]): return
                            value = f'{desc[0]}\nUsage: **`{desc[1]}`**'
                            embed = Embed(title=command.name, description=value, color=0xffaec8)
                            await ctx.send(embed=embed, reference=ctx.message)
                            return


def setup(client):
    client.add_cog(Help(client))