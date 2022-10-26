import os

import discord
from db import MongoDbHandler
from discord import app_commands
from dotenv import load_dotenv
from utils import create_offensive_users_prompt, get_message_details

load_dotenv()

DB = None

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Bot Ready!")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    message_details = get_message_details(message=message)
    is_successful = DB.updateUserScore(message_details)
    if is_successful:
        print("Updated user info")
    else:
        print("User update failed")


@tree.command(name="sync_commands", description="Synchronise commands to server")
async def sync_commands(interaction: discord.Interaction):
    await tree.sync(guild=interaction.guild)
    await interaction.response.send_message("Synced Commands")


@tree.command(name="get_top", description="Get top offensive users in server")
async def get_top(interaction: discord.Interaction):
    offenders = DB.getTopOffensive(client, interaction.guild.id)
    if len(offenders) == 0:
        await interaction.response.send_message("No Offenders! Server looks clean!")
    else:
        prompt = create_offensive_users_prompt(offenders)
        await interaction.response.send_message(embed=prompt)

if __name__ == "__main__":
    DB = MongoDbHandler(os.environ["DB_URL"], os.environ["DB_PASSWORD"])
    client.run(os.environ["DISCORD_CLIENT_SECRET"])
