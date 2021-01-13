"""menu view module"""
from . import view


class MenuView(view.View):
    """Menu view class"""
    pass

    def __init__(self):
        self._title = ''
        self._entries = []
        self.key = None

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
        print()
        choice = self.get_choice()
        return choice

    def quit(self):
        self.clear()