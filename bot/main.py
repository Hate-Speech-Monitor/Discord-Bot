import discord
from dotenv import load_dotenv
import os

load_dotenv()

def get_message_details(message : discord.Message) :
    d = {}
    d["content"] = message.content
    d["author"] = message.author.id 
    if message.guild : 
        d["server"] = message.guild.id
    else : 
        d["server"] = None
    return d

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message : discord.Message):
        print(get_message_details(message=message))

intents = discord.Intents.default()
intents.message_content = True

if __name__=="__main__" :
    client = MyClient(intents=intents)
    client.run(os.environ["DISCORD_CLIENT_SECRET"])
