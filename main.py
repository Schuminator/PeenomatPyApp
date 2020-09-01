import kivy
# -*- coding: iso-8859-1 -*-
from kivy.app import App

from kivy.uix.button import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.config import Config


Builder.load_file('header.kv')
Builder.load_file('statusbar.kv')
Builder.load_file('Inputparameters.kv')
Builder.load_file('outputparameters.kv')
Builder.load_file('Extra.kv')
Builder.load_file('info.kv')
Builder.load_file('addition.kv')
#loading main kv
Builder.load_file('peenomat.kv')


#Layout
"""
class Peenomat(AnchorLayout):
    pass
"""
class Peenomat(Screen):
    pass

class Instruction(Screen):
    pass

class Additional(Screen):
    pass

class About(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(Peenomat(name='peenomat'))
sm.add_widget(Instruction(name='instruction'))
sm.add_widget(Additional(name='additional'))
sm.add_widget(About(name='about'))

#change Icon
Config.set('kivy','window_icon','icon.png')

#class WindowManager(ScreenManager):
    #pass

#Font
LabelBase.register(name='Roboto',
                   fn_regular='Roboto-Regular.ttf',
                   fn_bold ='Roboto-Bold.ttf')

LabelBase.register(name='Amatic',
                   fn_regular ="AmaticSC-Regular.ttf",
                   fn_bold = "Amatic-Bold.ttf")

LabelBase.register(name='ProFont',
                   fn_regular='ProFontWindows.ttf')

LabelBase.register(name='Com',
                   fn_regular='commando.ttf')


class PeenomatApp(App):
    def build(self):   #initialize and return root Widget
        self.icon = 'icon.png'
        #return pm
        return sm  #initializing screenmanager widget and returning
        #return Peenomat()

if __name__=="__main__":

    PeenomatApp().run()