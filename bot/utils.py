from typing import Union

import discord


class UserMessage:
    def __init__(self):
        self.content: str = ""
        self.author: int = 0
        self.server: Union[int,  None] = None
        self.score: int = 0


def getOffensiveInfo(message):  # TODO
    pass


def get_message_details(message: discord.Message) -> UserMessage:
    d = UserMessage()
    d.content = message.content
    d.author = message.author.id
    if message.guild:
        d.server = message.guild.id
    return d
