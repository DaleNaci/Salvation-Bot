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
        self.update_weekly_gexp.start()


    @tasks.loop(seconds=604800)
    async def update_weekly_gexp(self):
        data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
            .format(self.key, "Salvation")).json()

        members = data["guild"]["members"]

        t = datetime.now()
        year = t.year
        month = t.month if t.month>=10 else "0{}".format(t.month)
        day = t.day if t.day>=10 else "0{}".format(t.day)
        date = "{}-{}-{}".format(year, month, day)

        exps = []

        for m in members:
            exps.append([m["uuid"], sum(m["expHistory"].values())])

        exps.sort(key=lambda x: x[1], reverse=True)

        desc = ""
        for i in range(20):
            player_data = requests.get("https://api.hypixel.net/player?key={}&uuid={}"
                    .format(self.key, exps[i][0])).json()
            name = player_data["player"]["displayname"]
            line = "{}. {} - {}\n".format(i+1, name, exps[i][1])
            desc += line

        desc = desc.replace("_", "\_")

        embed = Embed(
                    title="Top Weekly Guild Experience",
                    description=desc,
                    color=Color.dark_green()
                )

        channel = self.bot.get_channel(714229812310573087)
        await channel.send(embed=embed)


    @update_weekly_gexp.before_loop
    async def wait_to_midnight(self):
        await self.bot.wait_until_ready()

        now = datetime.now()
        weekday = datetime.today().weekday()
        if weekday == 6:
            weekday = -1

        sec_left = ((6 - weekday) * 86400
                    - now.hour * 3600
                    - now.minute * 60
                    - now.second
                    - 60)

        await asyncio.sleep(sec_left)



def setup(bot):
    bot.add_cog(Gweekly(bot))
