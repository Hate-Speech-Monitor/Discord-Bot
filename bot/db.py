import pymongo
from utils import UserMessage


class MongoDbHandler:

    def __init__(self, connection_string: str, password: str):
        self.conn_str = connection_string.replace('<password>', password)
        self.client = pymongo.MongoClient(self.conn_str)
        self.db = self.client["db"]

    def updateUserScore(self, message: UserMessage) -> bool:
        try:
            existsUser = self.db.users.find_one({
                "author": message.author,
                "server": message.server
            })
            if existsUser:
                self.db.users.update_one({
                    "author": existsUser['author'],
                    "server": existsUser['server']
                }, {
                    "$set": {"score": existsUser['score'] + message.score} # TODO
                })
            else:
                self.db.users.insert_one({
                    "author": message.author,
                    "server": message.server,
                    "score": message.score
                })
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
