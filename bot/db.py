import datetime
from http import server

import pymongo

from bot.utils import UserMessage


class MongoDbHandler:

    def __init__(self, connection_string: str, password: str):
        self.conn_str = connection_string.replace('<password>', password)
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client["db"]

    def updateUserScore(self, message: UserMessage) -> bool:
        try:
            self.db.users.update_one({
                "author": message.author,
                "server": message.server
            }, {}, upsert=True)
            return True
        except Exception as e:
            print(e)
            return False

    def getMostOffensiveUsers(self, server_id) -> list:
        try:
            return self.db.users.find({
                "server": server_id
            }).sort("score")
        except Exception as e:
            print(e)
            return []
