"""View module"""
import os
from pandas import DataFrame


class View:
    """View class"""
    key = None

    @classmethod
    def get_choice(cls):
        """Method for creating
        a prompt for users"""
        choice = input(">> ")
        return choice

    @staticmethod
    def _clear():
        """Private method to clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def add_title_menu(cls, title):
        """Method of creating titles"""
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
        """Line opening method for menus
        with automatic numbering"""
        print("{} : {}".format(cls.key, value))
        print()
        cls.key += 1

    @classmethod
    def quit(cls):
        """Method to clear the screen
        when the program is stopped"""
        cls._clear()

    @classmethod
    def request(cls, question):
        """Method for displaying questions when
        creating a model or executing a tournament"""
        print()
        print(question)
        print()
        choice = cls.get_choice()
        return choice

    @classmethod
    def tab_view(cls, title, elements_list, elements_columns):
        """Table display method"""
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
        """Method of displaying
        indications to the user"""
        print()
        print(indication)

    @classmethod
    def pause(cls):
        """Pause method"""
        input("\nPress enter to continue")
