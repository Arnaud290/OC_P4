""" general model module"""
from tinydb import TinyDB, Query
import types
import sys

class Model:
    """general model class"""
    db = TinyDB('app/database/db.json')

    def __init__(self):
        self.db = TinyDB('app/database/db.json')

    def save(self):
        """save instance model"""
        table = self.db.table(self.__class__.__name__)
        table.insert(self.__dict__)

    @classmethod
    def get_serialized(cls):
        """get all instances model"""
        table = cls.db.table(cls.__name__)
        serialized_table = table.all()
        return serialized_table

    @classmethod
    def get_id_serialized(cls, player_id):
        """get instance with id"""
        table = cls.db.table(cls.__name__)
        serialized_table = table.all()
        return serialized_table[player_id]

    @classmethod
    def delete_all(cls):
        """delete all instances model"""
        table = cls.db.table(cls.__name__)
        table.truncate()
    
    def delete(self):
        """delete instance with id"""
        table = self.db.table(self.__class__.__name__)
        query = Query() 
        table.remove(query.id == self.id)

    def update(self, key, value):
        """update value into db"""
        table = self.db.table(self.__class__.__name__)
        query = Query()
        table.update({key: value}, query.id == self.id)

    @classmethod
    def get_number(cls):
        """get numbers of instances model saved"""
        table = cls.db.table(cls.__name__)
        number = len(table)
        return number

