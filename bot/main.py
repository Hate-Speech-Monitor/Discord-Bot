import os
import threading

import discord
import flask
from db import MongoDbHandler
from discord import app_commands
from dotenv import load_dotenv
from flask import request
from flask_cors import CORS
from utils import create_offensive_users_prompt, get_message_details

load_dotenv()

DB = None

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

app = flask.Flask(__name__)
CORS(app)


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


@app.route('/getGuilds', methods=["GET"])
def getGuilds():
    data = []
    for guild in client.guilds:
        df = {
            "name": guild.name,
            "members": guild.member_count,
            "guild_id": str(guild.id),
            "offenders": len(DB.getTopOffensive(client, guild.id))
        }
        if guild.icon:
            df["icon"] = guild.icon.url
        data.append(df)
    return flask.jsonify({
        "status": "success",
        "data": data
    }), 200


@app.route('/guild/getTop', methods=["GET"])
def getTopOffenders():
    guild_id = request.args.get("guild")
    try:
        guild_id = int(guild_id)
    except Exception as e:
        return flask.jsonify({
            "status": "failed",
            "message": "invalid guild id"
        }), 400
    offenders = DB.getTopOffensive(client, guild_id)
    return flask.jsonify({
        "status": "success",
        "data": offenders
    }), 200


def start_server():
    print("Starting server")
    app.run(debug=False)


if __name__ == "__main__":
    DB = MongoDbHandler(os.environ["DB_URL"], os.environ["DB_PASSWORD"])
    thread = threading.Thread(target=start_server, args=[])
    thread.start()
    client.run(os.environ["DISCORD_CLIENT_SECRET"])
