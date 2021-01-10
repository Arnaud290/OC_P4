"""new tournament control module"""
from . import controller


class NewTournamentControl(controller.Controller):
    """ New tournament control class"""
  
    def __call__(self):
        self.menu = views.menu_view.MenuView()
        self.new_tournament_control_menu()

    def new_tournament_control_menu(self):   
        self.menu.add_menu_line('key', 'modify existing players')
        self.menu.add_menu_line('key', 'modify existing players')
        self.menu.add_menu_line('key', 'Return to main menu')
        while True:
            choice = self.menu.display_menu()
            choice.lower()
            if choice not in ('1', '2', 'q'):
                continue
            if choice == '1':
                pass
            if choice == '2':
                pass
            if choice == 'q' or 'Q':
                control = main_menu_control.MainMenuControl()
                control()
