from __future__ import annotations

import json
import os

import discord
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)

@tree.command(name="test", description="my first command!")
async def test(inter: discord.Interaction):
    await inter.response.send_message(f"Hello world!")


# DO NOT CHANGE ANY INFORMATION BELOW THIS LINE
# On ready listener-- Ensuring that the commands are synced up n all

@client.event
async def on_ready():
    await tree.sync()
    print("Bot is ready.\n-----")

    game = discord.CustomActivity("Happy Holidays!")
    await client.change_presence(status=discord.Status.idle, activity=game)


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
