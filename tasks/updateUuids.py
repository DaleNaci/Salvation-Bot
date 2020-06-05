import asyncio
import json
import requests
import time
import calendar
from datetime import datetime

import discord
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from discord.utils import get
from discord.utils import find
from discord import Color, Embed


class Gweekly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("api_key.txt", "r") as f:
            lines = f.readlines()
            self.key = lines[0].strip()
        self.update_uuids.start()


    @tasks.loop(seconds=3600)
    async def update_uuids(self):
        guild_data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
            .format(self.key, "Salvation")).json()

        members = guild_data["guild"]["members"]

        uuids = [m["uuid"] for m in members]
        


    @update_uuids.before_loop
    async def wait_until_bot_ready(self):
        await self.bot.wait_until_ready()




def setup(bot):
    bot.add_cog(Gweekly(bot))
