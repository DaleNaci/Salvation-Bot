import asyncio
import json
import requests

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Gexp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("api_key.txt", "r") as f:
            lines = f.readlines()
            self.key = lines[0].strip()


    @commands.command()
    async def gexp(self, ctx, player=None):
        if player is None:
            await ctx.send("Please provide a username!")
            return

        guild_data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
                        .format(self.key, "Salvation")).json()
        player_data = requests.get("https://api.hypixel.net/player?key={}&name={}"
                        .format(self.key, player)).json()

        if player_data["player"] is None:
            await ctx.send("Invalid username!")
            return

        display_name = player_data["player"]["displayname"].replace("_", "\_")
        uuid = player_data["player"]["uuid"]
        print(uuid)
        gexp_data = None

        for d in guild_data["guild"]["members"]:
            if d["uuid"] == uuid:
                gexp_data = d["expHistory"]
                break

        if gexp_data is None:
            await ctx.send("Player is not in our guild!")
            return

        desc = ""
        for date, exp in gexp_data.items():
            line = "`{}:      {}`\n".format(date, exp)
            desc += line

        print(desc)

        embed = Embed(
                    title="Guild Experience: {}".format(display_name),
                    description=desc,
                    color=Color.dark_green()
                )

        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Gexp(bot))
