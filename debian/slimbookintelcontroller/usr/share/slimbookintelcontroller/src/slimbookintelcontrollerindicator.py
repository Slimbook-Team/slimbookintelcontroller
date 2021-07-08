#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import gettext
import signal
import subprocess
import os
import gi
import configparser
import gettext, locale
import sys


gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, GdkPixbuf, AppIndicator3

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from configparser import ConfigParser
from os.path import expanduser


srcpath = '/usr/share/slimbookintelcontroller/src'
sys.path.insert(1, srcpath)

currpath = os.path.dirname(os.path.realpath(__file__))

#Variables
user_name = subprocess.getoutput("logname")
user = subprocess.getoutput("echo ~"+user_name)
directorio = '~/.config/slimbookintelcontroller'

config_file = user + '/.config/slimbookintelcontroller/slimbookintelcontroller.conf'
#config_file = currpath + '/slimbookintelcontroller.conf'
config_object = ConfigParser()
config = ConfigParser()
config.read(config_file)

pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename = currpath+'/images/slimbookintelcontroller_header.png',
			width = 200,
			height = 150,
			preserve_aspect_ratio=True)


print(config_file)

iconapp = currpath+'/amd.png'

low_img = currpath+'/images/amd-1.png'

medium_img = currpath+'/images/logo-blue.png'

high_img = currpath+'/images/amd-3.png'

entorno_usu = locale.getlocale()[0]

try:
	if entorno_usu.find("en") >= 0 or entorno_usu.find("es") >= 0:
		idiomas = [entorno_usu]
	else: 
		idiomas = ['en_EN'] 
except:
	idiomas = ['en_EN'] 

# Configurar el acceso al catálogo de mensajes
t = gettext.translation('slimbookintelcontrollerindicator', 
                        currpath+'/locale', 
                        languages=idiomas,
                        fallback=True,)
_ = t.gettext



#Menu
class Indicator():
	modo_actual="none"
	parameters=('','','')
	icono_actual = iconapp

	def __init__(self):
		self.app = 'show_proc'
		iconpath = currpath+'/amd.png'
		# after you defined the initial indicator, you can alter the icon!
		self.testindicator = AppIndicator3.Indicator.new(
			self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER)

		self.testindicator.set_icon_theme_path(currpath+'/images/')
		self.testindicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)       
		self.testindicator.set_menu(self.create_menu())
		self.inicio()

	def create_menu(self):
		Gtk.Image.new_from_pixbuf(pixbuf)

		menu = Gtk.Menu()
	
		icon_bajo = Gtk.Image()
		icon_bajo.set_from_file(currpath+'/images/intel-green.png')

		icon_medio = Gtk.Image()
		icon_medio.set_from_file(currpath+'/images/intel-blue.png')

		icon_alto = Gtk.Image()
		icon_alto.set_from_file(currpath+'/images/intel-red.png')


		item_bajo = Gtk.ImageMenuItem(label=_('Low performance'), image = icon_bajo)
		item_bajo.connect('activate', self.bajorendimiento)
		item_bajo.set_always_show_image(True)

		item_medio = Gtk.ImageMenuItem(label=_('Medium performance'), image=icon_medio)
		item_medio.connect('activate', self.mediorendimiento)

		item_medio.set_always_show_image(True)

		item_alto = Gtk.ImageMenuItem(label=_('High performance'), image= icon_alto)
		item_alto.connect('activate', self.altorendimiento)
		item_alto.set_always_show_image(True)

		item_ventana = Gtk.MenuItem(label=_('Preferences'))
		item_ventana.connect('activate', self.openWindow)

		item_separador = Gtk.SeparatorMenuItem()

		item_quit = Gtk.MenuItem(label=_('Exit'))
		item_quit.connect('activate', self.exit)

		
		menu.append(item_bajo)
		menu.append(item_medio)
		menu.append(item_alto)
		menu.append(item_separador)
		menu.append(item_ventana)
		menu.append(item_quit)
		menu.show_all()

		return menu

	
	def exit(self, source):
		Gtk.main_quit()

	def openWindow(self, source):
		os.system("slimbookintelcontroller")

	def inicio(self):

		config = configparser.ConfigParser()
		config.read(config_file)

		print('Loading data from .conf:\n')

		#Mostramos indicador, o no :):

		self.testindicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.testindicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)

		if config.get('CONFIGURATION', 'show-icon') == 'on':
			self.testindicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
			print('- Autostart enabled')
		else:
			self.testindicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
			print('- Autostart disabled')
 		

		#Cargamos los parametros de la CPU
		params = config.get('PROCESSORS', config.get('CONFIGURATION', 'CPU')).split('/')
		self.parameters = params
		
		print('- CPU Parameters: '+ str(self.parameters))


		if config.get('CONFIGURATION', 'mode') == "low":
			print('- Low\n')
			self.bajorendimiento('x')
		else:
			if config.get('CONFIGURATION', 'mode') == "medium":
				print('- Medium\n')
				self.mediorendimiento('x')
			else:
				print('- High\n')
				self.altorendimiento('x')
		
		print("\nData loaded from .conf\n")


	def update_config_file(self, variable, value):
		# We change our variable: config.set(section, variable, value)
		config.set('CONFIGURATION', str(variable), str(value))

		# Writing our configuration file 
		with open(config_file, 'w') as configfile:
				config.write(configfile)

		print("Variable |"+variable+"| updated, actual value: "+value+"\n")

	#Funcion para configuracion de bajo rendimiento
	def bajorendimiento(self, widgets):
		self.modo_actual="low"
		self.icono_actual= low_img
		self.testindicator.set_icon_full('intel-green', 'icon_low')
		print('Updating '+self.modo_actual+' to : '+self.parameters[0].split('@')[0]+' '+self.parameters[1].split('@')[1]+'\n')
            
		self.update_config_file("mode", self.modo_actual)
		os.system('pkexec slimbookintelcontroller-pkexec')

	#Funcion para configuracion de medio rendimiento
	def mediorendimiento(self, widget):
		self.modo_actual="medium"
		self.icono_actual=medium_img
		self.testindicator.set_icon_full('intel-blue', 'icon_medium')
		print('Updating '+self.modo_actual+' to : '+self.parameters[1].split('@')[0]+' '+self.parameters[1].split('@')[1]+'.\n')
		
		self.update_config_file("mode", self.modo_actual)
		os.system('pkexec slimbookintelcontroller-pkexec')

	#Funcion para configuracion de alto rendimiento
	def altorendimiento(self, widget):
		self.modo_actual="high"
		self.icono_actual=high_img
		self.testindicator.set_icon_full('intel-red', 'icon_high')
		print('Updating '+self.modo_actual+' to : '+self.parameters[2].split('@')[0]+' '+self.parameters[2].split('@')[1]+'.\n')

		self.update_config_file("mode", self.modo_actual)
		os.system('pkexec slimbookintelcontroller-pkexec')

	

	

	

Indicator()

signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()