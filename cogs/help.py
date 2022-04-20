from discord.ext import commands
from config.config import *
from discord import Embed
import discord
# from config.embeds import Embeds

class Help(commands.Cog):
    '''Help Command'''

    def __init__(self, client: commands.Bot):
        self.client = client
        self.loaded_role = False

    def define_roles(self, ctx):
        self.dev_role = discord.utils.get(ctx.guild.roles, id=DEVELOPER_ROLE_ID)
        self.admin_role = discord.utils.get(ctx.guild.roles, id=ADMIN_ROLE_ID)
        self.mod_role = discord.utils.get(ctx.guild.roles, id=MODERATOR_ROLE_ID)
        self.loaded_role = True

    def all_role_check(self, ctx):
        roles = ctx.author.roles
        if self.dev_role in roles or self.admin_role in roles or self.mod_roles in roles:
            return True

    def role_check(self, ctx, role, extra_help):
        if role == 'dev':
            if not extra_help: return False
            if self.dev_role in ctx.author.roles:
                return True
        elif role == 'mod':
            if not extra_help: return False
            if self.dev_role in ctx.author.roles or self.mod_role in ctx.author.roles:
                return True
        elif role == 'none': return False
        else: return True

    @commands.command()
    async def help(self, ctx, *entry):
        '''show help for dedicated entry ||/cc help (entry(s))'''
        if not self.loaded_role: self.define_roles(ctx)
        #how is cmd desc confiured?
        # desc ||usage ||check
        #check=> dev: has dev role, mod: has permission, owner: is owner
        if not entry or entry[0] == '++':
            extra_help = True if entry else False
            embed = Embed(title='Help', description='Description for all Categories', color=0xffaec8)
            embed.set_footer(text='Do `/cc help (Categoty)` or `/cc help (Command)` for more help on it.')
            for cog in self.client.cogs:
                desc = self.client.cogs[cog].__doc__.split('||')
                if not self.role_check(ctx, desc[-1], extra_help): continue
                value = desc[0]
                if cog.lower() == 'help' and self.all_role_check(ctx): value += '\nAdd **`++`** at the end of help cmd to show Mod help\n`/cc help ++` `/cc help (category|command) ++`'
                lst = [command.name for command in self.client.get_cog(cog).get_commands() if self.role_check(ctx, command.help.split("||")[-1], extra_help)]
                if lst: value += f'\nCommands: **`{"` `".join(lst)}`**'
                embed.add_field(name=cog, value=value, inline=False)
            await ctx.send(embed=embed, reference=ctx.message)

        elif len(entry) == 1 or (len(entry)==2 and entry[-1]=='++'):
            extra_help = True if entry[-1] == '++' else False
            for cog in self.client.cogs:
                if cog.lower() == entry[0].lower():
                    desc = self.client.cogs[cog].__doc__.split('||')
                    if not self.role_check(ctx, desc[-1], extra_help): return
                    extra_desc = desc[0]
                    if cog.lower() == 'help' and self.all_role_check(ctx): extra_desc += '\nAdd **`++`** at the end of help cmd to show Mod help\n`/cc help ++` `/cc help (category|command) ++`'
                    embed = Embed(title=cog, description=extra_desc, color=0xffaec8)
                    embed.set_footer(text='Do `/cc help (Categoty)` or `/cc help (Command)` for more help on it.')
                    for command in self.client.get_cog(cog).get_commands():
                        if not self.role_check(ctx, command.help.split("||")[-1], extra_help): continue
                        embed.add_field(name=command.name, value=command.help.split("||")[0], inline=False)
                    await ctx.send(embed=embed, reference=ctx.message)
                    break

            else:
                for cog in self.client.cogs:
                    for command in self.client.get_cog(cog).get_commands():
                        if command.name.lower() == entry[0].lower():
                            desc = command.help.split("||")
                            if not self.role_check(ctx, desc[-1], extra_help): return
                            value = f'{desc[0]}\nUsage: **`{desc[1]}`**'
                            embed = Embed(title=command.name, description=value, color=0xffaec8)
                            await ctx.send(embed=embed, reference=ctx.message)
                            return


def setup(client):
    client.add_cog(Help(client))