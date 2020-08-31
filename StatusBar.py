from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
#from Inputparameters import InputParameters


ver = ''
class InputParameters(GridLayout):
    verfahren =ObjectProperty(None)

    def on_state(self, togglebutton):
        tb = togglebutton
        global ver
        if tb.state == 'down':
            self.verfahren = tb.text
            ver = tb.text
            print(self.verfahren, ver)
            return self.verfahren


class StatusBar(BoxLayout):
    #InputGrößen
    group_mode = False
    prozess = ObjectProperty(None)
    vorbehandlung = ObjectProperty(None)
    material = ObjectProperty(None)
    haerte = ObjectProperty(None)
    rauheit = ObjectProperty(None)
    verfahren = ObjectProperty(None)

    #OutputGrößen
    frequency = StringProperty(None)
    speed = StringProperty(None)
    hub = StringProperty(None)

    def btn_submit(self):
        global ver
        ip = App.get_running_app().root.get_screen('peenomat').ids._input_parameters
        op = App.get_running_app().root.get_screen('peenomat').ids._output_parameters
        ap = App.get_running_app().root.get_screen('additional').ids._additional

        print(u"Härte:", ip.haerte.value, "Rauheit:", ip.rauheit.value, "Material:", ip.material.text, "Vorbehandlung:", ip.vorbehandlung.text, ver, ap.step1.text )

        frequenz = 0
        if ip.haerte.value < 50:
            op.frequency = str(180) +" Hz"
            op.speed = str(2.4) +" mm/s"
            op.hub = str(3.4) + " mm"
        elif ip.haerte.value < 60:
            op.frequency = str(200) +" Hz"
            op.speed = str(3.5) + " mm/s"
            op.hub = str(5.23) + " mm"
        else:
            op.frequency = str(220) +" Hz"
            op.speed = str(1.2) + " mm/s"
            op.hub = str(7.2) + " mm"
        #control to see if right value is taken
        print(op.frequency)

    def btn_clear(self):
        ip = App.get_running_app().root.get_screen('peenomat').ids._input_parameters
        op = App.get_running_app().root.get_screen('peenomat').ids._output_parameters
        ip.pro1.state = "normal"
        ip.pro2.state = "normal"
        ip.pro3.state = "normal"
        ip.material.text = "Auswahl treffen"
        ip.vorbehandlung.text = "Auswahl treffen"
        ip.haerte.value = 55
        ip.rauheit.value = 5.5
        op.frequency = "---"
        op.speed = "---"
        op.hub = "---"