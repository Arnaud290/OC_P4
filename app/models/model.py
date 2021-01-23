"""General model module"""
from tinydb import TinyDB, Query

class Model:
    """general model class"""   
    db = TinyDB('app/database/db.json')
          
    def save(self):
        """save instance model""" 
        table = Model.db.table(self.__class__.__name__)
        table.insert(self.__dict__)
    
    def delete(self):
        """delete instance model"""
        table = Model.db.table(self.__class__.__name__)
        query = Query()
        table.remove(query.id == self.id)

    def update(self, key, value):
        """update value into db"""
        table = Model.db.table(self.__class__.__name__)
        query = Query()
        table.update({key: value}, query.id == self.id)