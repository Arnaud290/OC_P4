"""Program launch module"""
from app.controllers import application_controller

if __name__ == "__main__":
    main = application_controller.ApplicationController()
    main.start()
