"""menu view module"""
from . import view


class MenuView(view.View):
    """Menu view class"""
    pass

    def __init__(self):
        self._entries = {}
        self._title = ''

    def add_title_menu(self, title):
        self._title = title


    def add_menu_line(self, key, option):
        self._entries[str(key)] = option

    def display_menu(self):
        self.clear()
        print(self._title)
        print("\n\n")
        for key, option in self._entries.items():
            print("{}: {}".format(key, option))
            print()

        choice = self.get_choice()
        return choice
