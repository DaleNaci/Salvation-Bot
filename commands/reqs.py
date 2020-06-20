import asyncio
import json
import requests

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Reqs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("api_key.txt", "r") as f:
            lines = f.readlines()
            self.key = lines[0].strip()


    @commands.command()
    async def reqs(self, ctx, player=None):
        if player is None:
            await ctx.send("Please provide a username!")
            return

        data = requests.get("https://api.hypixel.net/player?key={}&name={}"
            .format(self.key, player)).json()

        if data["player"] is None:
            await ctx.send("Invalid username!")
            return

        info = data["player"]["stats"]

        stats = {
            "skywars": {
                "wins": info["SkyWars"]["wins"],
                "kills": info["SkyWars"]["kills"]
            },
            "bedwars": {
                "wins": info["Bedwars"]["wins_bedwars"],
                "level": data["player"]["achievements"]["bedwars_level"]
            },
            "general": {
                "level": round(((data["player"]["networkExp"] + 15312.5) ** .5 - (125 / (2 ** .5)))
                               / (25 * (2 ** .5)), 2),
                "AP": data["player"]["achievementPoints"]
            }
        }

        requirements = {
            "SW Wins": [stats["skywars"]["wins"] >= 500, "skywars wins"],
            "SW Kills": [stats["skywars"]["kills"] >= 1000, "skywars kills"],
            "Level": [stats["general"]["level"] >= 25, "general level"],
            "BW Wins": [stats["bedwars"]["wins"] >= 150, "bedwars wins"],
            "BW Stars": [stats["bedwars"]["level"] >= 25, "bedwars level"],
            "Achievement Points": [stats["general"]["AP"] >= 1000, "general AP"]
        }

        sw_req = requirements["SW Wins"][0] and requirements["SW Kills"][0]
        bw_req = requirements["BW Wins"][0] and requirements["BW Stars"][0]
        gen_req = requirements["Level"][0] and requirements["Achievement Points"][0]

        color = Color.green() if (sw_req or bw_req) and gen_req else Color.red()

        embed = Embed(title=player, color=color)

        for k, v in requirements.items():
            valid, path = v
            path = path.split(" ")
            emoji = ":green_square:" if valid else ":red_square:"
            message = "{} {}".format(emoji, stats[path[0]][path[1]])

            embed.add_field(name=k, value=message)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Reqs(bot))
