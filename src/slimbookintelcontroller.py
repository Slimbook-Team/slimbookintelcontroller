#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import gi
import subprocess
import gettext, locale, time
import shutil
import configparser
import re #Busca patrones expresiones regulares



from pathlib import Path

from applyconfig import USER_NAME

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from configparser import ConfigParser
from gi.repository import Gdk, Gtk, GdkPixbuf
from os.path import expanduser

currpath = os.path.dirname(os.path.realpath(__file__))
srcpath = '/usr/share/slimbookintelcontroller/src'
sys.path.insert(1, currpath)

user_name = subprocess.getoutput("logname")
user = subprocess.getoutput("echo ~"+user_name)
currpath = os.path.dirname(os.path.realpath(__file__))

config_object = ConfigParser()
config_file = user+'/.config/slimbookintelcontroller/slimbookintelcontroller.conf'
processors_file = currpath+'/processors/available'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAUNCHER_DESKTOP = os.path.join(BASE_DIR, "slimbookintelcontroller-autostart.desktop")
print(LAUNCHER_DESKTOP)
AUTOSTART_DESKTOP = os.path.expanduser("/home/"+USER_NAME+"/.config/autostart/slimbookintelcontroller-autostart.desktop")
print(AUTOSTART_DESKTOP)

# IDIOMAS ----------------------------------------------------------------

# CMD(Genera .pot):  pygettext -d slimbookintelcontrollercopy slimbookintelcontrollercopy.py
# CMD(Genera .mo a partir de .po):  msgfmt -o slimbookintelcontrollercopy.po slimbookintelcontrollercopy.mo
try:
    entorno_usu = locale.getlocale()[0]
    if entorno_usu.find("en") >= 0 or entorno_usu.find("es") >= 0 or entorno_usu.find("fr") >= 0:
        idiomas = [entorno_usu]
    else: 
        idiomas = ['en_EN'] 
except:
    idiomas = ['en_EN']  

print('Language: ', entorno_usu)
t = gettext.translation('slimbookintelcontroller',
						currpath+'/locale',
						languages=idiomas,
						fallback=True,) 
_ = t.gettext


#Command exit to variable
cpu = subprocess.getoutput('cat /proc/cpuinfo | grep '+'name'+'| uniq')
print(cpu)


#Read proc patron
patron = re.compile('[ ](\w\d)[-]([0-9]{4,5})(\w*)[ ]')
version = patron.search(cpu).group(1)
number = patron.search(cpu).group(2)
line_suffix = patron.search(cpu).group(3)
model_cpu = version+'-'+number+line_suffix
config = ConfigParser()
config.read(config_file)

proc_config = ConfigParser()
proc_config.read(currpath+'/processors/available.conf')


print("CPU | Model: '"+model_cpu+"' | Version: "+version,"| CPU Numbers: "+number, "| CPU Letters: "+line_suffix+".")

switch1 = Gtk.Switch()
switch1.set_halign(Gtk.Align.END)
switch2 = Gtk.Switch()
switch2.set_halign(Gtk.Align.END)

rbutton1 = Gtk.RadioButton.new_with_label_from_widget(None, (_("Low")))
rbutton2 = Gtk.RadioButton.new_with_mnemonic_from_widget(rbutton1, (_("Medium")))
rbutton3 = Gtk.RadioButton.new_with_mnemonic_from_widget(rbutton1, (_("High")))


class SlimbookINTEL(Gtk.ApplicationWindow):

    modo_actual = ""
    indicador_actual = ""
    autostart_actual = ""
    parameters=('','','')
    
    
    def __init__(self):
        
        self.creafichero()

        self.init_gui(switch1, switch2)
        

    # WINDOW

        Gtk.Window.__init__(self, title ="Slimbook Intel Controller")
        ICON = (currpath+'/images/slimbookintelcontroller.svg')      
        try: 
            self.set_icon_from_file(ICON)
        except:
            print("Icon not found"+ICON)

        self.set_decorated(False)
        self.set_size_request(925,590) #anchoxalto
        self.set_position(Gtk.WindowPosition.CENTER)
        self.get_style_context().add_class("bg-image")

    # GRIDS

        win_grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=0,
                         row_spacing=10)


        grid = Gtk.Grid(column_homogeneous=True,
                         #row_homogeneous=True,
                         column_spacing=0,
                         row_spacing=25)

        self.add(win_grid) 

    # CONTENT --------------------------------------------------------------------------------

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/slimbookintelcontroller_header.png',
			width = 700,
			height = 200,
			preserve_aspect_ratio=True)


        header_img = Gtk.Image.new_from_pixbuf(pixbuf)
        header_img.set_halign(Gtk.Align.START)
        header_img.set_valign(Gtk.Align.START)

        label1 = Gtk.Label(label=_("Enable app at startup"))
        label1.set_halign(Gtk.Align.START)    
        
        label2 = Gtk.Label(label=_("Show indicator icon"))
        label2.set_halign(Gtk.Align.START)
       
        button1 = Gtk.Button(label ="Button 1")
        button1.set_halign(Gtk.Align.START)
        button1.get_style_context().add_class("button-none")

        button2 = Gtk.Button(label ="Button 2")
        button2.set_halign(Gtk.Align.START)
        button2.get_style_context().add_class("button-none")

        # Processor
        hbox_cpu = Gtk.HBox()

        cpu_name = Gtk.Label(label=cpu[12:]) 
        cpu_name.set_halign(Gtk.Align.CENTER)
        hbox_cpu.set_name('cpu_info')

        hbox_cpu.pack_start(cpu_name, True, True, 0)

        separador = Gtk.Separator()
        separador.set_halign(Gtk.Align.CENTER)
        


        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/cross.png',
			width = 20,
			height = 20,
			preserve_aspect_ratio=True)

        close = Gtk.Image.new_from_pixbuf(pixbuf1)
        close.get_style_context().add_class("close")
        close.set_halign(Gtk.Align.END)
        close.set_valign(Gtk.Align.START)

        evnt_close = Gtk.EventBox()
        evnt_close.add(close)
        evnt_close.connect("button_press_event", self.on_btnCerrar_clicked)

    # RADIOS ---------------------------------------------------------------------------------

        img = ''

        if entorno_usu.find("es") >= 0:         #Español
            img='modos_es.png'
        else: 
            img='modos_en.png'                  #Inglés

        modos = Gtk.Label(label='CHANGE CPU MODE')
        modos.get_style_context().add_class("modes")
        modos.set_halign(Gtk.Align.CENTER)

        #CAJA 1
        vbox1 = Gtk.VBox()
        rbutton1.connect("toggled", self.on_button_toggled, "low")
        rbutton1.set_name('radiobutton') 
        rbutton1.set_halign(Gtk.Align.CENTER)

        rbutton1_img = Gtk.Image.new_from_file(currpath+'/images/modo1.png')
        rbutton1_img.set_halign(Gtk.Align.CENTER)

        vbox1.pack_start(rbutton1_img, False, False, 0)
        vbox1.pack_start(rbutton1, False, False, 0)
        
        #CAJA 2
        vbox2 = Gtk.VBox()
        rbutton2.connect("toggled", self.on_button_toggled, "medium")
        rbutton2.set_name('radiobutton')
        rbutton2.set_halign(Gtk.Align.CENTER)

        rbutton2_img = Gtk.Image.new_from_file(currpath+'/images/modo2.png')
        rbutton2_img.set_halign(Gtk.Align.CENTER)
        
        vbox2.pack_start(rbutton2_img, False, False, 0)
        vbox2.pack_start(rbutton2, False, False, 0)

        #CAJA 3
        vbox3 = Gtk.VBox()
        rbutton3.connect("toggled", self.on_button_toggled, "high")
        rbutton3.set_name('radiobutton')
        rbutton3.set_halign(Gtk.Align.CENTER)
        
        rbutton3_img = Gtk.Image.new_from_file(currpath+'/images/modo3.png')
        rbutton3_img.set_halign(Gtk.Align.CENTER)
        
        vbox3.pack_start(rbutton3_img, False, False, 0)
        vbox3.pack_start(rbutton3, False, False, 0)

    # BUTTONS --------------------------------------------------------------------------------

        botonesBox = Gtk.Box(spacing=10)
        botonesBox.set_name('botonesBox')
        botonesBox.set_halign(Gtk.Align.CENTER)
        botonesBox.set_name('buttons')

        #ACEPTAR
        btnAceptar = Gtk.ToggleButton(label=_("ACCEPT"))
        btnAceptar.set_size_request(125, 30)
        btnAceptar.connect("toggled", self.on_btnAceptar_clicked)
        botonesBox.pack_start(btnAceptar, True, True, 0)

        #CERRAR
        btnCancelar = Gtk.ToggleButton(label=_("CANCEL"))
        btnCancelar.set_size_request(125, 30)
        btnCancelar.connect("toggled", self.on_btnCerrar_clicked, 'x')
        botonesBox.pack_start(btnCancelar, True, True, 0)
        botonesBox.set_valign(Gtk.Align.END)

    # BTNABOUT_US ----------------------------------------------------------------------------

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/question.png',
			width = 20,
			height = 20,
			preserve_aspect_ratio=True)

        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.get_style_context().add_class("help")
        iconApp.set_halign(Gtk.Align.END)

        evnt_box = Gtk.EventBox()
        evnt_box.add(iconApp)
        evnt_box.set_vexpand(True)

        evnt_box.connect("button_press_event", self.about_us)

        evnt_box.set_valign(Gtk.Align.END)

    # GRID ATTACH ----------------------------------------------------------------------------

        grid.attach(label1, 1, 3, 3, 1)
        grid.attach(label2, 1, 4, 3, 1)
        
        grid.attach(switch1, 4, 3, 3, 1)
        grid.attach(switch2, 4, 4, 3, 1)

        grid.attach(hbox_cpu, 0, 5, 8, 1)
        
        grid.attach(modos, 0, 6, 8, 1)

        grid.attach(vbox1, 1, 7, 2, 1)
        grid.attach(vbox2, 3, 7, 2, 1)
        grid.attach(vbox3, 5, 7, 2, 1)
        
    # WIN GRID ATTACH ----------------------------------------------------------------------------
        
        grid.attach(header_img, 0, 0, 8, 8)       
        grid.attach(evnt_close, 7, 0, 1, 1)

        grid.attach(evnt_box, 7, 7, 1, 1)
        grid.attach(botonesBox, 1, 7, 6, 1)

        win_grid.attach(grid, 1, 1, 8, 10)

        

    def on_button_toggled(self, button, name):
        self.modo_actual = name

    def on_btnAceptar_clicked(self, widget):
        
        # SAVE THINGS        
        call = subprocess.getstatusoutput("pkexec slimbookintelcontroller-pkexec secureboot_state | grep 'Able to use intel-undervolt'")

        print(str(call))

        if not call[0] == 0:
            
            dialog = Gtk.MessageDialog(
                #transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Secureboot Warning",
            )

            dialog.format_secondary_text(
                "This computer has Secureboot enabled, which does not allow kernel to manage CPU parameters."
            )

            response = dialog.run()


            if response == Gtk.ResponseType.CLOSE:

                print("WARN dialog closed by clicking CLOSE button")

            dialog.destroy()

        else:
            #Comprobamos los switch
            self._inicio_automatico(switch1, switch1.get_state())

            self._show_indicator(switch2, switch2.get_state())

            

            #ACTUALIZAMOS VARIABLES
            self.update_config_file("mode", self.modo_actual)
            self.update_config_file("autostart", self.autostart_actual)
            self.update_config_file("show-icon", self.indicador_actual) 
            
            print("Updating: "+config_file+" ...")

            self.reboot_indicator()

        
        #CLOSE PROGRAM
        Gtk.main_quit()

    #Copies autostart file in directory
    def _inicio_automatico(self, switch, state):

        
        if switch.get_active() is True:
            os.system('pkexec slimbookintelcontroller-pkexec autostart enable')
            self.autostart_actual = 'on'

        else:
            print("\nAutostart Disabled")
            os.system('pkexec slimbookintelcontroller-pkexec autostart disable')
            self.autostart_actual = 'off'

        print('Autostart now: '+ self.autostart_actual+'')

    def _show_indicator(self, switch, state):

        if switch.get_active() is True:
            print("\nIndicator Enabled")
            self.indicador_actual = 'on' # --> Luego esta variable será guardada y cargada desde el programa indicador
        else:
            print("\nIndicator Disabled")
            self.indicador_actual= 'off'

        self.update_config_file('show-icon', self.indicador_actual)

        print('Indicador now: '+ self.indicador_actual)
        print()

    def init_gui(self, switch1, switch2): # ---> UNFINISHED
        config.read(config_file)
        #Inicio automatico :):
        if config.get('CONFIGURATION', 'autostart') == 'on':
            #autostart
            print('')
            self.autostart_actual = 'on'
            switch1.set_active(True)
            print('- Autostart enabled')
        else:
            self.autostart_actual = 'off'
            switch2.set_active(False)
            print('- Autostart disabled')

        #Mostramos indicador, o no :):
        if config.get('CONFIGURATION', 'show-icon') == 'on':
            self.indicador_actual = 'on'
            switch2.set_active(True)
            print('- Indicator enabled')

        else:
            self.indicador_actual = 'off'
            switch2.set_active(False)
            print('- Indicator disabled')

        #RadiobuttonSelection        
        if config.get('CONFIGURATION', 'mode') == "low":
            print('- Low')
            self.modo_actual = 'low'
            rbutton1.set_active(True)
            
        elif config.get('CONFIGURATION', 'mode') == "medium":
            print('- Medium')
            self.modo_actual = 'medium'
            rbutton2.set_active(True)
        else:
            print('- High')
            self.modo_actual = 'high'
            rbutton3.set_active(True)
        
        #CPU Parameters
        params = config.get('PROCESSORS', model_cpu).split('/')
        self.parameters = params
        print('- CPU Parameters: '+ str(self.parameters))       

        print("\n.conf data loaded succesfully!\n")
    
    def reboot_indicator(self):

        print('\nProcess PID')
        indicator = subprocess.getoutput('pgrep -f slimbookintelcontrollerindicator')
        print(indicator)

        os.system('kill -9 '+indicator)
        print('Starting indicator...')
        os.system('python3 '+currpath+'/slimbookintelcontrollerindicator.py  &')
        print()

    def about_us(self, widget, x):
        print('\nAbout us ...:')
        print('\n')
        #Abre la ventana de info
        from slimbookintelcontrollerinfo import PreferencesDialog

    def on_btnCerrar_clicked(self, widget, x):
        Gtk.main_quit()

    def update_config_file(self, variable, value):

        # We change our variable: config.set(section, variable, value)
        config.set('CONFIGURATION', str(variable), str(value))

        # Writing our configuration file 
        with open(config_file, 'w') as configfile:
                config.write(configfile)

        print("Variable |"+variable+"| updated, actual value: "+value+"\n")

    #Funcion crear directorio /slimbookintelcontroller y crear fichero de configuracion si no existe ya.    
    def creafichero(self):
        
        if os.path.isfile(config_file):
            print('File .conf already exists\n')           
        else:
            print ("File doesn't exist")

            if os.path.exists (user+'/.config/slimbookintelcontroller'):
                print('Directory already exists')
                os.system('touch '+config_file)
                print('\nCreating file ...')

            else:
                print("Directory doesen't exist")
                os.system('mkdir ~/.config/slimbookintelcontroller')
                os.system('touch '+config_file)
                print('Creating file ...')

            with open( config_file, 'w') as conf:
                
                if (self.fichero_conf('configuration') != -1):
                    print('Se ha escrito el conf.'+str(self.fichero_conf('processors')))
                    self.fichero_conf('configuration').write(conf)
                    #self.fichero_conf('processors').write(conf)
                
                    os.system("cat "+config_file)
                
                else: 
                    print('El procesador no esta soportado')
                    os.system('rm '+config_file)

            print('File created succesfully!\n')
        
        if os.system("cat "+config_file) != 0:
            print("Failed creating .conf")
            os.system('rm '+config_file)
    
    #Genera config_object para el .conf
    def fichero_conf(self, section):

        if section == 'configuration':

            config_object["CONFIGURATION"] = {
            "mode": "low",                
            "autostart": "off",
            "show-icon": "off",
            "cpu": model_cpu
            }
            

        elif section == 'processors':

            config_object["PROCESSORS"] = {
            'i3-10110U': '10@12/15@25/20@30/ 10/15/25/ w',
            'i3-1005G1': '10@12/15@25/20@30/ 13/15/25/ w',

            'i5-8250U': '10@12/15@20/20@35/ 10/15/25/ w',
            'i5-8265U': '10@12/15@20/20@35/ 10/15/25/ w',
            'i5-10210U': '10@12/15@20/20@30/ 10/15/25/ w',
            'i5-1035G1': '10@12/15@20/20@35/ 13/15/25/ w',

            'i7-7500U': '10@12/15@20/20@35/ 7.5/15/25/ w',
            'i7-8550U': '10@12/15@25/30@45/ 10/15/25/ w',
            'i7-8565U': '10@12/15@25/30@45/ 10/15/25/ w',
            'i7-1065G7': '10@12/15@20/25@45/ 12/15/25/ w',
            'i7-10510U': '10@12/15@25/30@50/ 10/15/25/ w',
            'i7-10750H': '15@20/30@45/54@70/ 35/45/54/ w',
            'i7-1165G7': '10@12/15@25/30@50/ 12/15/28/ w'
            }
        
            
        return config_object    



    
win = SlimbookINTEL()


style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/css/style.css')

Gtk.StyleContext.add_provider_for_screen (
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()
