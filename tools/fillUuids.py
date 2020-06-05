import os
import requests
import json

with open(os.path.join(os.getcwd(), "..", "api_key.txt"), "r") as f:
    lines = f.readlines()
    key = lines[0].strip()

guild_data = requests.get("https://api.hypixel.net/guild?key={}&name={}"
    .format(key, "Salvation")).json()

members = guild_data["guild"]["members"]

d = {}

for m in members:
    uuid = m["uuid"]
    player_data = requests.get("https://api.hypixel.net/player?key={}&uuid={}"
                    .format(key, uuid)).json()
    name = player_data["player"]["displayname"]
    d[uuid] = name


print(d)

with open(os.path.join(os.getcwd(), "..", "data", "uuids.txt"), "w") as f:
    for k, v in d.items():
        f.write("{} {}\n".format(k, v))
