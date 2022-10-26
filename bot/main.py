import os

import discord
from db import MongoDbHandler
from dotenv import load_dotenv
from utils import get_message_details

load_dotenv()

DB = None

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message: discord.Message):
        message_details = get_message_details(message=message)
        is_successful = DB.updateUserScore(message_details)
        if is_successful : 
            print("Updated user info")
        else : 
            print("User update failed")


intents = discord.Intents.default()
intents.message_content = True

if __name__ == "__main__":
    DB = MongoDbHandler(os.environ["DB_URL"], os.environ["DB_PASSWORD"])
    client = MyClient(intents=intents)
    client.run(os.environ["DISCORD_CLIENT_SECRET"])
