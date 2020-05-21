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

cogs = [
    "commands.reqs"
]

if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.command()
async def getIDs(ctx):
    data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
        .format(key, "Salvation")).json()

    uuids = [d["uuid"] for d in data["guild"]["members"]]
    print(uuids)

    with open("Members.json", "r") as f:
        info = json.load(f)

    for u in uuids:
        if u not in info:
            player_data = requests.get("https://api.hypixel.net/player?key={}&player={}"
                .format(key, u)).json()


    await ctx.send("Works")


with open("token.txt", "r") as f:
    lines = f.readlines()
    token = lines[0].strip()

bot.run(token)
