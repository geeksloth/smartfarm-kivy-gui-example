from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
LabelBase.register(name= "Thai",
                   fn_regular='THSarabunNew.ttf',
                   fn_bold='THSarabunNew Bold.ttf',)

class FarmScreenManager(ScreenManager):
    pass

class Page2(Screen):
    pass

class Page1(Screen):
    def on_enter(self, *args):
        print("print from Page 1")

class HomeScreen(Screen):
    def on_enter(self, *args):
        print("Print from Home Screen")

class FarmApp(App):
    def build(self):
        return FarmScreenManager()
    
if __name__ == "__main__":
    FarmApp().run()