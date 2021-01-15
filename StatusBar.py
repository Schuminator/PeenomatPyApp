from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.popup import Popup
import math
from kivy.lang import Builder
#from Inputparameters import InputParameters


ver = ''   #globale Variable für Verfahren (unsauber)

class Warn(GridLayout):
    pass

class InputParameters(GridLayout):
    verfahren =ObjectProperty(None)

    def on_state(self, togglebutton):
        tb = togglebutton
        ip = App.get_running_app().root.get_screen('peenomat').ids._input_parameters
        global ver
        if tb.state == 'down':
            self.verfahren = tb.text
            ver = tb.text
            if ver == "P-MOH":
                ip.durchmesser.value = 20

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
    durchmesser = ObjectProperty(None)

    #OutputGrößen
    frequency = StringProperty(None)
    speed = StringProperty(None)
    hub = StringProperty(None)
    powpres = StringProperty(None)

    def btn_submit(self):
        global ver
        ip = App.get_running_app().root.get_screen('peenomat').ids._input_parameters
        op = App.get_running_app().root.get_screen('peenomat').ids._output_parameters
        #sb = App.get_running_app().root.get_screen('peenomat').ids._status_bar.ids._warn
        ap = App.get_running_app().root.get_screen('additional').ids._additional

        #print(u"Härte:", ip.haerte.value, "Warnung","sb.warn.text", "Rauheit:", ip.rauheit.value,"Durchmesser:", ip.durchmesser.value, ver, ap.step1.text ) #, "Vorbehandlung:", ip.vorbehandlung.text, "Material:", ip.material.text

        #initialisierung
        frequenz = 0
        ET = 0
        fr = 0
        d_impround = 0
        vf = 0
        a_S = 0
        pow =0
        E_Si =0
        pres = 0
        E_round =0
        #Parameter Schwellenergie
        mr2=ip.materialtrag.value
        rz = ip.rauheit.value
        d_moh = ip.durchmesser.value
        h_hrc = ip.haerte.value
        E_1 = 215000
        E_moh = 550000      #Emodul WC20

        d_ps = mr2/100*(rz*10**(-3)) #in milimeter
        r_1 = ((d_moh*0.5)**2-(0.5*d_moh-d_ps)**2)**0.5 #milimeter
        r_p02 = 38.89*h_hrc-233.3
        phi = math.log(r_1/(0.0683*(math.pi*r_p02*d_moh*0.5*(E_1+E_moh)/(E_1*E_moh))))
        a1 = math.pi * (r_1 ** 2) * ((0.001*0.9*10**(-3))/(0.001*rz*10**(-3)))
        a1n = math.pi*(r_1**2)*(1/(mr2/100))
        eta=0.7
        sf= 1.1 #sicherheitsfaktor
        #RpA Goldsmith
        if r_p02 <= 1000:
            n = -1.05*math.log(r_p02)+8.85
        else:
            n =85.1*r_p02**(-0.58)
        r_pa = n*r_p02
        kfm = 5 / 2 * r_pa

        #Wirkungsgrad
        if d_moh == 10 and h_hrc >= 59.5:
            eta = -0.0053*h_hrc+0.8669
        elif d_moh == 10 and h_hrc >= 57.0:
            eta = -0.1146*h_hrc+7.391
        elif d_moh == 20 and h_hrc >= 59.5:
            eta = -0.0061*h_hrc+0.7183
        elif d_moh ==20 and h_hrc >= 57.0:
            eta = -0.1104*h_hrc+6.9419
        else:
            eta = 0.7

        #Stosszahl
        e = 0.0108*h_hrc + 0.109
        #print(mr2, rz, d_moh, h_hrc,d_ps,r_1,r_p02,phi,n, r_pa,a1n,a1,eta,e,kfm)

        #Experimentelle Schwellenergie
        e_010 = -3.518 + h_hrc * 0.0675
        e_020 = -10.473 + h_hrc * 0.1959
        k_010 = 10.24 - h_hrc * 0.0836
        k_020 = 6.5406 - h_hrc*0.04504


        #Auswahl Schwellenergie
        if ap.step1.text == u'Fr\u00e4sen':
            eta = 0.7
            E_Si = (1/(1-e**2))*(1/eta)*phi*a1*d_ps*kfm*sf
            #print("ES:",E_Si)
        elif ap.step1.text == "Drehen":
            E_Si = (1/(1-e**2))*(1/eta)*phi*a1*d_ps*kfm*sf

        elif ap.step1.text == "Schleifen":
            E_Si = (1/(1-e ** 2))*(1/eta)*phi*a1n*d_ps*kfm*sf

        elif ap.step1.text == "Auswahl treffen":
            warning_popup()

        #Outputbestimmung

        if ver == "EM-MOH" and d_moh == 10:
            fr = 150
            pow = math.ceil(((E_Si + 50.031) / 107.61) * 100)
            E_round=107.61*(pow/100)-50.031
            #d_imp = math.log(E_Si/e_010)*(1/k_010)
            d_impround = math.log(E_round/e_010)*(1/k_010)
            a_S = (1/2**0.5)*d_impround*0.8   #Eindruckabstand 0.9=Sicherheitsfaktor
            vf = math.floor(fr*a_S*60)
            op.speed = str("{0:.0f}".format(vf)) +" mm/min"
            op.powpres = str("{0:.0f}".format(pow)) + " %"
            op.frequency = str(fr) + " Hz"
            op.hub = str(0.25) + " mm"
            op.line = str("{0:.3f}".format(a_S)) + " mm"

        elif ver == "EM-MOH" and d_moh == 20:
            fr = 150
            pow = math.ceil(((E_Si + 32.23) / 82.2) * 100) #aufrunden der Leistung
            E_round=82.202*(pow/100)-32.23  #Leistung gerundet, hier mit gerundeter Leistung erreichter Energieeintrag
            #d_imp = math.log(E_Si/e_020)*(1/k_020)
            d_impround= math.log(E_round/e_020)*(1/k_020) #erzielter EIndruck mit gerundeter Leistung
            a_S = ((1/2)**0.5)*d_impround*0.8  #Eindruckabstand
            vf = math.floor(fr*a_S*60)
            op.speed = str("{0:.0f}".format(vf)) + " mm/min"
            op.powpres = str("{0:.0f}".format(pow)) + " %"
            op.frequency = str(fr) + " Hz"
            op.hub = str(0.25) + " mm"
            op.line = str("{0:.3f}".format(a_S)) + " mm"

        elif ver == "P-MOH" and E_Si <= 10:
            pres = round(math.exp((E_Si-6.627)/7.603),1)
            fr = round(20.323*pres + 135.8,1)
            E_round = 7.6027*math.log(pres)+6.6272
            d_impround = math.log(E_round/e_020)*(1/k_020)
            a_S = ((1 / 2) ** 0.5) * d_impround*0.8
            vf = math.floor(fr * a_S * 60)
            op.speed = str("{0:.0f}".format(vf)) + " mm/min"
            op.powpres = str("{0:.1f}".format(pres)) + " bar"
            op.frequency = str(fr) + " Hz"
            op.hub = str(0.5) + " mm"
            op.line = str("{0:.3f}".format(a_S)) + " mm"

        elif ver == "P-MOH" and E_Si > 10:
            pres = round((E_Si-4.9225)/7.078, 1)
            fr = round(20.323 * pres + 135.8, 1)
            E_round = 7.078*pres + 4.923
            d_impround = math.log(E_round / e_020) * (1 / k_020)
            a_S = ((1 / 2) ** 0.5) * d_impround*0.8
            vf = math.floor(fr * a_S * 60)
            op.speed = str("{0:.0f}".format(vf)) + " mm/min"
            op.powpres = str("{0:.1f}".format(pres)) + " bar"
            op.frequency = str(fr) + " Hz"
            op.hub = str(1.5) + " mm"
            op.line = str("{0:.3f}".format(a_S)) + " mm"

        elif ver == " ":
            warning_popup()

        elif E_Si == 0:
            "sb.warn = Energie nicht definiert!"
            warning_popup()

        print(e_010, k_010, fr, "pres", "Exakt:", E_Si,"Gerundet:", E_round,"d_impround: ",d_impround,"a_S:",a_S,vf,op.speed,op.hub,op.frequency, pow, op.powpres)
        if pow > 100:

            op.frequency = "---"
            op.speed = "---"
            op.hub = "---"
            op.powpres = "---"
            op.line = "---"
            warning_popup()
        elif pres > 6:
            #warning_popup()
            op.frequency = "---"
            op.speed = "---"
            op.hub = "---"
            op.powpres = "---"
            op.line = "---"
            warning_popup()
        elif ver == " ":
            #warning_popup()
            op.frequency = "---"
            op.speed = "---"
            op.hub = "---"
            op.powpres = "---"
            op.line = "---"
            warning_popup()
        # Switch Outputgroeßen AppFenster
        if ver == "P-MOH":
            ip.durchmesser.value = 20
            op.txtpowpres = "Druck"
            op.txtfrequency ="ca. Frequenz"
            #op.frequency="---"

    def btn_clear(self):
        ip = App.get_running_app().root.get_screen('peenomat').ids._input_parameters
        op = App.get_running_app().root.get_screen('peenomat').ids._output_parameters
        ap = App.get_running_app().root.get_screen('additional').ids._additional
        ip.pro1.state = "normal"
        ip.pro2.state = "normal"
        #ip.pro3.state = "normal"
        #ip.material.text = "Auswahl treffen"
        #ip.vorbehandlung.text = "Auswahl treffen"
        ip.haerte.value = 60
        ip.rauheit.value = 5.5
        ip.durchmesser.value = 10
        ip.materialtrag.value = 85
        op.frequency = "---"
        op.speed = "---"
        op.hub = "---"
        op.powpres = "---"
        op.line = "---"
        op.txtfrequency ="Frequenz:"
        op.txtpowpres = "Leistung:"
        ap.step1.text="Auswahl treffen"
        ap.step2.text="Auswahl treffen"
        ap.materialneu.text="Auswahl treffen"


def warning_popup():
    show = Warn()
    popupWindow = Popup(title = "Warnung", content =show, size_hint=(None,None), size=(300,200))
    popupWindow.open()