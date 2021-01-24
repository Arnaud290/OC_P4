"""base view module"""
import os
from pandas import DataFrame


class View:
    """General view class"""
    key = None 
    @classmethod
    def get_choice(cls):
        """user get choice method"""
        choice = input(">> ")
        return choice
    @staticmethod
    def _clear():
        """clear screen method"""
        os.system('cls' if os.name == 'nt' else 'clear')
    @classmethod
    def add_title_menu(cls, title):
        """value for title menu"""
        cls._clear()
        stars = '*'*len(title)
        print()
        print(stars)
        print(title)
        print(stars)
        print()
        cls.key = 1
    @classmethod
    def add_menu_line(cls, value):
        """options and values for menu lines"""
        print("{} : {}".format(cls.key, value))
        print()
        cls.key += 1
    @classmethod
    def quit(cls):
        """screen quit method"""
        cls._clear()
    @classmethod
    def request(cls, question):
        """ask questions method"""
        print()
        print(question)
        print()
        choice = cls.get_choice()
        return choice
    @classmethod
    def tab_view(cls, title, elements_list, elements_columns):
        """table view method"""
        print()
        print(title)
        print('_'*(len(title)))
        print()
        index = []
        for element in elements_list:
            index.append('')
        tab = DataFrame(elements_list, index=index, columns=elements_columns)
        if elements_list:
            print(tab)
        print()
        print()
    @classmethod
    def indication(cls, indication):
        """display indications method"""
        print()
        print(indication)
    @classmethod
    def pause(cls):
        """display pause method"""
        input("\nPress enter to continue")
