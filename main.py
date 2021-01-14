"""Program launch module"""
from app.controllers import main_menu_control

if __name__ == "__main__":
    main = main_menu_control.MainMenuControl()
    main()
