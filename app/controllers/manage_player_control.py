"""manage player control module"""
from . import controller
from .. import views
from . import main_menu_control


class ManagePlayerControl(controller.Controller):
    """Manage player control class"""
 
    def __call__(self):
        self.menu = views.menu_view.MenuView()
        self.player_control_menu()

    def player_control_menu(self):
        self.menuu.add_title_menu("CHESS MANAGE PLAYERS")   
        self.menu.add_menu_line('1', 'Add player')
        self.menu.add_menu_line('2', 'modify existing players')
        self.menu.add_menu_line('q', 'Return to main menu')
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
                return True
