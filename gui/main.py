from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class FarmApp(App):
    def build(self):
        return FarmScreenManager()
    
class FarmScreenManager(ScreenManager):
    pass

class HomeScreen(Screen):
    def on_enter(self, *args):
        print("Welcome to the Smart Farm App!")

class Page1(Screen):
    def on_enter(self, *args):
        print("You are now on Page 1.")

if __name__ == "__main__":
    FarmApp().run()