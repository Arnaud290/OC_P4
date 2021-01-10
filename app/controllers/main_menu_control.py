"""main menu control module"""
from . import controller
from . import manage_player_control
from ..views import menu_view


class MainMenuControl(controller.Controller):
    """main menu control class"""
        
    def __call__(self):
        self.menu = menu_view.MenuView()
        self.main_menu()

    def main_menu(self):   
        self.menu.add_title_menu("CHESS MAIN MENU")
        self.menu.add_menu_line("1", "New tournament")
        self.menu.add_menu_line("2", "Manage players")
        self.menu.add_menu_line("3", "Rapports")
        self.menu.add_menu_line("q", "Quit")
        control = True
        while control:
            user_choice = self.menu.display_menu()
            user_choice.lower()
            if user_choice not in ('1', '2', '3', 'q'):
                continue
            if user_choice == '1':
                pass
            if user_choice == '2':
                pass
            if user_choice == 'q' or 'Q':
                break
