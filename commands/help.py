import asyncio

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Color, Embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_descs = {
            "!help": "Provides information about all commands.",
            "!gexp": "Guild exp earned by a player in the last week.",
            "!reqs": "Determines if a player meets the guild requirements."
        }


    @commands.command()
    async def help(self, ctx):
        desc = ""
        for k, v in self.command_descs.items():
            desc += "`{}`: {}\n".format(k, v)

        embed = Embed(title="Commands", color=Color.blue(), description=desc)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))
