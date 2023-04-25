import discord
from config.embeds import Embeds
from discord.ext import commands
from discord import app_commands as app_cmds
from config.support import *
from config.config import *

EMBEDS = Embeds()

class Moderator(commands.Cog):
    '''Moderator Commands ||mod'''
    
    def __init__(self, client: commands.Bot):
        self.client = client
        self.no_mention = discord.AllowedMentions(users=False)

    async def send_mod_log(self, ctx: commands.Context, result = '**(Success!)**'):
        '''send command log to LOG channel when Moderator/Developer CMD issued'''
        if result == '**(Success!)**':
            pass
        elif result is None:
            result = '**Failed: UnAuthorised**'
        else:
             result = f', **Failed:** [error]({result})'
        EMBEDS.MODLOG.description = \
        f"{ctx.author.name}#{ctx.author.discriminator} has used mod command `{ctx.message.content}` in {ctx.channel.mention} in [message]({ctx.message.jump_url}) {result}"
        await discord.utils.get(ctx.guild.channels, id=MODLOG_CHANNEL_ID).send(embed=EMBEDS.MODLOG)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=5):
        '''delete a vertain amount of messages from a channel ||/cc purge [amount] ||mod'''
        if amount > 30:
            amount = 30
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{amount} messages deleted.')
        # await self.send_mod_log(ctx)

    @commands.command()
    # @commands.has_permissions(MODERATE_MEMBERS=True)
    @commands.has_permissions(ban_members=True)
    @commands.has_role(MODERATOR_ROLE_ID)
    async def mute(self, ctx, member: discord.Member):
        '''apply mute role to a memeber ||/cc mute (member) ||mod'''
        role = discord.utils.get(ctx.guild.roles, id=MUTE_ROLE_ID)
        if role in member.roles:
            reply = await ctx.send(f'{member.mention} is already muted.', reference=ctx.message, allowed_mentions=self.no_mention)
            result = reply.jump_url
        else:
            await member.add_roles(role)
            await ctx.send(f'{member.mention} has been muted.', reference=ctx.message, allowed_mentions=self.no_mention)
            result = '**(Success!)**'
        await self.send_mod_log(ctx, result)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.has_role(MODERATOR_ROLE_ID)
    async def unmute(self, ctx, member: discord.Member):
        '''remove mute role from a member ||/cc unmute (member) ||mod'''
        role = discord.utils.get(ctx.guild.roles, id=MUTE_ROLE_ID)
        if role not in member.roles:
            reply = await ctx.send(f'{member.mention} is not muted.', reference=ctx.message, allowed_mentions=self.no_mention)
            result = reply.jump_url
        else:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, id=MUTE_ROLE_ID))
            await ctx.send(f'{member.mention} has been unmuted.', reference=ctx.message, allowed_mentions=self.no_mention)
            result = '**(Success!)**'
        await self.send_mod_log(ctx, result)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, delete_message_days=7, *, reason=None):
        '''softban a member. to remove his messages from the guild ||/cc softban (member) [del msg days] [reason] ||mod'''
        await member.ban(reason=reason, delete_message_days=delete_message_days)
        await member.unban()
        await ctx.send(f'{member.mention} has been softbanned for reason {reason}', reference=ctx.message, allowed_mentions=self.no_mention)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        '''ban a member ||/cc ban (member) [reason] ||mod'''
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned for {reason}', reference=ctx.message, allowed_mentions=self.no_mention)
        await self.send_mod_log(ctx)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        '''unban a member ||/cc unban (name#discrim) ||mod'''
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            if [ban_entry.user.name, ban_entry.user.discriminator] == member.split('#'):
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(f'{member} has been unbanned.', reference=ctx.message, allowed_mentions=self.no_mention)
                await self.send_mod_log(ctx)
                break
        else:
            reply = await ctx.send(f'{member} not found, or user is not banned', reference=ctx.message)
            await self.send_mod_log(ctx, reply.jump_url)


    @purge.error
    @mute.error
    @unmute.error
    @softban.error
    @ban.error
    @unban.error
    async def cmd_error(self, ctx: commands.Context, error):
        '''on error when cmd run'''
        if not isinstance(error, commands.errors.MissingPermissions):
            #don't show error to user if user is not authorised
            reply = await ctx.send(error, reference=ctx.message)
            result = reply.jump_url
        else: result = None
        await self.send_mod_log(ctx, result)


async def setup(client: commands.Bot):
    await client.add_cog(Moderator(client))
