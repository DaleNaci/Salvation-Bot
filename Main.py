import asyncio
import json
import requests

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


client = discord.Client()
bot = commands.Bot(command_prefix = "!")

with open("api_key.txt", "r") as f:
    lines = f.readlines()
    key = lines[0].strip()


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def reqs(ctx, player):
    data = requests.get("https://api.hypixel.net/player?key={}&name={}"
        .format(key, player)).json()

    info = data["player"]["stats"]

    stats = {
        "skywars": {
            "wins": info["SkyWars"]["wins"],
            "kills": info["SkyWars"]["kills"],
            "kdr": round(info["SkyWars"]["kills"]
                            / info["SkyWars"]["deaths"], 2)
        },
        "bedwars": {
            "wins": info["Bedwars"]["wins_bedwars"],
            "level": data["player"]["achievements"]["bedwars_level"],
            "fkdr": round(info["Bedwars"]["final_kills_bedwars"]
                            / info["Bedwars"]["final_deaths_bedwars"], 2)
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
        "SW KDR": [stats["skywars"]["kdr"] >= 1, "skywars kdr"],
        "BW Wins": [stats["bedwars"]["wins"] >= 150, "bedwars wins"],
        "BW Stars": [stats["bedwars"]["level"] >= 25, "bedwars level"],
        "BW FKDR": [stats["bedwars"]["fkdr"] >= 3.5, "bedwars fkdr"],
        "Level": [stats["general"]["level"] >= 25, "general level"],
        "Achievement Points": [stats["general"]["AP"] >= 1000, "general AP"]
    }

    color = Color.green() if any(not b for b in requirements.values()) else Color.red()

    embed = Embed(title=player, color=color)

    for k, v in requirements.items():
        valid, path = v
        path = path.split(" ")
        emoji = ":green_square:" if valid else ":red_square:"
        message = "{} {}".format(emoji, stats[path[0]][path[1]])

        embed.add_field(name=k, value=message)

    await ctx.send(embed=embed)


with open("token.txt", "r") as f:
    lines = f.readlines()
    token = lines[0].strip()

bot.run(token)
