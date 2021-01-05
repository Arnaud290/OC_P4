"""save and restore module"""
from tinydb import TinyDB


class SaveLoadingData:
    """Class for save and loading players and tournaments"""
    db = TinyDB('db.json')
    players_table = db.table('players')
    tournaments_table = db.table('tournaments')

    @classmethod
    def save_player(cls, serialized_player):
        if type(serialized_player) == dict:
            cls.players_table.insert(serialized_player)
        else:
            cls.players_table.truncate()
            cls.players_table.insert_multiple(serialized_player)

    @classmethod
    def load_player(cls):
        load_serialized_players = cls.players_table.all()
        return load_serialized_players

    @classmethod
    def nb_players(cls):
        load_serialized_players = cls.load_player()
        nb_players = len(load_serialized_players)
        return nb_players

    @classmethod
    def save_tournament(cls, serialized_tournament):
        if type(serialized_tournament) == dict:
            cls.tournaments_table.insert(serialized_tournament)
        else:
            cls.tournaments_table.truncate()
            cls.tournaments_table.insert_multiple(serialized_tournament)

    @classmethod
    def load_tournament(cls):
        load_serialized_tournaments = cls.tournaments_table.all()
        return load_serialized_tournaments

    @classmethod
    def nb_tournaments(cls):
        load_serialized_tournaments = cls.load_tournament()
        nb_tournaments = len(load_serialized_tournaments)
        return nb_tournaments
