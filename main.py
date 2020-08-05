from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')
"""shift option +s to make json look nice"""

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"

    def log_in(self, uname, pword) : 
        with open('users.json') as file:
            users= json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.transition.direction = 'left'
            self.manager.current = "login_screen_success"
            self.ids.login_wrong.text = ""
        else: 
            self.ids.login_wrong.text = "Wrong username or password"
            # self.ids allows us to access features within kivy file of this class

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file : 
            users = json.load(file)
        users[uname] = {
            'username' : uname,
            'password' : pword, 
            'created' : datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }
        with open("users.json", 'w') as file : 
            json.dump(users, file)
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_complete_screen"

class SignUpCompleteScreen(Screen): 
    def to_login(self):
        self.manager.transition.direction = 'right'
        # Change the direction of transition between pages
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen) :
    def log_out(self): 
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'
    def get_quote(self, feel) :
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")
        available_feelings = [Path(filename).stem for filename in
                                 available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else: 
            self.ids.quote.text = "Try another feeling"
            

class RootWidget(ScreenManager):
    pass

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    # All this is doing is creating a class that puts together 3 objects, so
    # we can refer to it as one object from kivy file
    # The order of imports is very important as it can hide certain properties
    # button behaviour needs to be firsrt
    pass

class MainApp(App) : 
    def build(self):
        return RootWidget()

if __name__ == "__main__" :
    MainApp().run() 
