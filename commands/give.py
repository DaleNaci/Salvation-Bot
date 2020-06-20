import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_role("External") # CHANGE TO OFFICER
    async def give(self, ctx, user:discord.Member, role:discord.Role, days=-1):
        await user.add_roles(role)
        await ctx.send(f"Added {role} role to <@{user.id}>.")



def setup(bot):
    bot.add_cog(Give(bot))
