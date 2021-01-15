"""base view module"""
import os
from pandas import DataFrame


class View:
    """General view class"""
    def __init__(self):
        self.choice = ''

    def get_choice(self):
        """user get choice method"""
        self.choice = input(">> ")
        return self.choice

    @staticmethod
    def clear():
        """clear screen method"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def add_title_menu(self, title):
        """value for title menu"""
        self.clear()
        self._title = title
        stars = '*'*len(self._title)
        print()
        print(stars)
        print(self._title)
        print(stars)
        print()
        self.key = 1

    def add_menu_line(self, value):
        """options and values for menu lines"""
        print("{} : {}".format(self.key, value))
        print()
        self.key += 1

    def choice_menu(self):
        """user select choice method"""
        print()
        choice = self.get_choice()
        return choice

    def quit(self):
        """screen quit method"""
        self.clear()

    def request(self, question):
        """ask questions method"""
        print()
        print(question)
        print()
        choice = self.get_choice()
        return choice

    def tab_view(self, title, elements_list, elements_columns):
        """table view method"""
        print()
        print(title)
        print('_'*(len(title)))
        print()
        index = []
        for element in elements_list:
            index.append('')
        self.tab = DataFrame(elements_list, index=index, columns=elements_columns)
        if elements_list:
            print(self.tab)
        print()
        print()

    def indication(self, indication):
        """display indications method"""
        print()
        print(indication)

    def pause(self):
        """display pause method"""
        input("\nPress enter to continue")
