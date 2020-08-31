from kivy.app import App
from kivy.uix.gridlayout import GridLayout
# -*- coding: iso-8859-1 -*-

class MyLayout(GridLayout):
    pass

class BeispielApp(App):
    def build(self):
        return MyLayout()

if __name__=="__main__":
    BeispielApp().run()
