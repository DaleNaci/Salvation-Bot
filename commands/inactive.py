import asyncio
import json
import requests

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Inactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("api_key.txt", "r") as f:
            lines = f.readlines()
            self.key = lines[0].strip()
        self.weekly_requirement = 20000
        self.uuid_name_pairs = {}
        with open("data/uuids.txt", "r") as f:
            for line in f.readlines():
                lst = line.split()
                self.uuid_name_pairs[lst[0]] = lst[1]


    @commands.command()
    async def inactive(self, ctx):
        guild_data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
                        .format(self.key, "Salvation")).json()

        members = guild_data["guild"]["members"]

        inactive_members = []
        for m in members:
            total_exp = sum(m["expHistory"].values())
            if total_exp < self.weekly_requirement:
                inactive_members.append((m["uuid"], total_exp))

        desc = ""
        counter = 0
        for m in inactive_members:
            counter += 1
            uuid = m[0]
            exp = m[1]

            name = ""
            if uuid in self.uuid_name_pairs:
                name = self.uuid_name_pairs[uuid]
            else:
                player_data = requests.get("https://api.hypixel.net/player?key={}&uuid={}"
                                .format(self.key, uuid)).json()
                name = player_data["player"]["displayname"]

            desc += "{}. `{}`: {}\n".format(counter, name, exp)

        embed = Embed(
                    title="Inactive Members",
                    description=desc,
                    color=Color.dark_red()
                )

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Inactive(bot))
