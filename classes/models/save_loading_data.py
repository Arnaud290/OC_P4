"""save and restore module"""
from tinydb import TinyDB


class SaveLoadingData:
    db = TinyDB('db.json')
    players_table = db.table('players')
    """Class for save and loading players and tournaments"""
    @classmethod
    def save_player(cls, serialized_player):
        cls.players_table.truncate()
        if type(serialized_player) == dict:
            cls.players_table.insert(serialized_player)
        else:
            cls.players_table.insert_multiple(serialized_player)
    @classmethod
    def load_players(cls):
        serialized_players = cls.players_table.all()
        return serialized_players
