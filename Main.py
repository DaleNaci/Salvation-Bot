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
    "commands.reqs",
    "commands.gexp",
    "tasks.gdaily",
    "tasks.gweekly"
]

if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    print("Bot is ready!")


with open("token.txt", "r") as f:
    lines = f.readlines()
    token = lines[0].strip()

bot.run(token)
