import random
from typing import Union
from hatespeech import evaluate
import discord


class UserMessage:
    def __init__(self):
        self.content: str = ""
        self.author: int = 0
        self.server: Union[int,  None] = None
        self.score: int = 0

    def getOffensiveInfo(self):
        self.score = evaluate(self.content)


def get_message_details(message: discord.Message) -> UserMessage:
    d = UserMessage()
    d.content = message.content
    d.author = message.author.id
    if message.guild:
        d.server = message.guild.id
    d.getOffensiveInfo()
    return d


def create_offensive_users_prompt(users: list) -> discord.Embed:
    res = discord.Embed(
        title="Top Offenders of Server",
        color=discord.Color.red()
    )
    names = [str(user["name"]) for user in users]
    scores = [str(user["score"]) for user in users]
    res.add_field(name="Name", value="\n".join(names), inline=True)
    res.add_field(name="Score", value="\n".join(scores), inline=True)
    return res
