#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import gi
import subprocess
import gettext, locale

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from pathlib import Path
from gi.repository import Gtk, Gdk, GdkPixbuf     
from os.path import expanduser   


# AÑADIR CLASE --> .get_style_context().add_class("button-none")

#IDIOMAS ----------------------------------------------------------------

# pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py

currpath = os.path.dirname(os.path.realpath(__file__))
entorno_usu = locale.getlocale()[0]
try: 
    if entorno_usu.find("en") >= 0 or entorno_usu.find("es") >= 0:
	    idiomas = [entorno_usu]
    else: 
        idiomas = ['en_EN'] 
except:
    idiomas = ['en_EN'] 


print('Language: ', idiomas)
t = gettext.translation('slimbookintelcontrollerinfo',
						currpath+'/locale',
						languages=idiomas,
						fallback=True,) 
_ = t.gettext


user_name = subprocess.getoutput("logname")
user = subprocess.getoutput("echo ~"+user_name)


style_provider = Gtk.CssProvider()
style_provider.load_from_path(currpath+'/css/style.css')

Gtk.StyleContext.add_provider_for_screen (
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

class PreferencesDialog(Gtk.Window):
	
    def __init__(self):
		
        Gtk.Window.__init__(self,
			title='',
            parent=None)

        ICON = os.path.join(currpath+'/images/slimbookintelcontroller.svg')
        #print('Icon route: '+ICON)
        
        try: 
            self.set_icon_from_file(ICON)
        except:
            print("Icon not found")

        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)     
        self.get_style_context().add_class("bg-color")
        self.set_default_size(800, 400)     
        self.set_decorated(False)
        self.set_name('info_win')

        win_grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=0,
                         row_spacing=0)

        info_grid = Gtk.Grid(column_homogeneous=True,
                         column_spacing=0,
                         row_spacing=20)

        info_grid.set_name('info_grid')
        
        self.add(win_grid)

    # COMPONETS
        # Icono APP
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename= currpath+'/images/logo-sb.png',
			width=200,
			height=100,
			preserve_aspect_ratio=True)
        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.set_name('logo')


        info = Gtk.Label()
        info.set_markup('<span>'+(_("The Slimbook Intel Controller app is capable of setting several TDP power levels for your Intel mobile processor. Switching between the different performance presets will give you the ability to control both performance and battery life with a single click. Bear in mind that the higher you set your performance level, your processor will also run hotter and drain your battery faster, so keep that in mind! \n\nSlimbook Intel Controller uses the third party software intel-undervolt from kitsunyan."))+'</span>')
        info.set_line_wrap(True)
        info.set_name('label')

        
        info2 = Gtk.Label()
        info2.set_markup('<span>'+_('If you want to support the Slimbook team with the development of this app and several more to come, you can do so by joining our ') + "<a href='https://www.patreon.com/slimbook'> patreon </a>" +_(' or buying a brand new Slimbook.')+'</span>')
        info2.set_line_wrap(True)
        info2.set_name('label')


        info3 = Gtk.Label()
        info3.set_markup("<span><b>"+_("Note: ")+"</b>"+_("Many laptops limit the power of the CPU, when working without the charger connected. Therefore, if you want to take advantage of the high-performance mode of this application, you may need to connect the charger.")+"</span>")
        info3.set_line_wrap(True)
        info3.set_name('label')


        enlaces_box = Gtk.Box(spacing=5)
        enlaces_box.set_halign(Gtk.Align.CENTER)

        salvavidas = Gtk.Label(label=_('This software is provided * as is * without warranty of any kind..'))
        salvavidas.set_name('label')

        license1 = Gtk.Label()
        license1.set_markup("<span><b>"+_("You are free from:")+"</b></span>")
        license1.set_name('label')

        license2 = Gtk.Label()
        license2.set_markup("<span><b><small>"+_("Share: ")+"</small></b><small>"+_("copy and redistribute the material in any medium or format\nSlimbook Copyright - License Creative Commons BY-NC-ND")+"</small></span>")
        license2.set_name('label')

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/cc.png',
			width=100,
			height=50,
			preserve_aspect_ratio=True)

        licencia = Gtk.Image.new_from_pixbuf(pixbuf)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/cross.png',
			width=20,
			height=20,
			preserve_aspect_ratio=True)

        close = Gtk.Image.new_from_pixbuf(pixbuf)
        
        close.set_halign(Gtk.Align.END)
        close.set_valign(Gtk.Align.START)

        evnt_close = Gtk.EventBox()
        evnt_close.add(close)
        evnt_close.set_name("close")
        evnt_close.connect("button_press_event", self.on_button_close)

    # REDES SOCIALES --------------------------------------------------------------
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/twitter.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        itwitter = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(itwitter, False, False, 0)

        twitter = Gtk.Label()
        twitter.set_markup("<span><b><a href='https://twitter.com/SlimbookEs'>@SlimbookEs</a></b>    </span>")
        twitter.set_justify(Gtk.Justification.CENTER)
        
        enlaces_box.pack_start(twitter, False, False, 0)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/facebook.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        ifacebook = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(ifacebook, False, False, 0)

        facebook = Gtk.Label()
        facebook.set_markup("<span><b><a href='https://www.facebook.com/slimbook.es'>slimbook.es</a></b>    </span>")
        facebook.set_justify(Gtk.Justification.CENTER)
        enlaces_box.pack_start(facebook, False, False, 0)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
			filename=currpath+'/images/insta.png',
			width=25,
			height=25,
			preserve_aspect_ratio=True)

        iinstagram = Gtk.Image.new_from_pixbuf(pixbuf)
        enlaces_box.pack_start(iinstagram, False, False, 0)

        instagram = Gtk.Label()
        instagram.set_markup("<span><b><a href='https://www.instagram.com/slimbookes'>@slimbookes</a></b></span>")
        instagram.set_justify(Gtk.Justification.CENTER)
        enlaces_box.pack_start(instagram, False, False, 0)

    # Enlaces --------------------------------------------------------------------------
        
        link_box2 = Gtk.HBox()
        link_box2.set_halign(Gtk.Align.CENTER)

        #WEB
        web_link=''
        if entorno_usu.find('es') >= 0:
            web_link = 'https://slimbook.es/es/'
        else:
            web_link = 'https://slimbook.es/en/'

        web = Gtk.Label()
        web.set_markup("<span><b><a href='"+web_link+"'>"+_("@Visit Slimbook web")+"</a></b>    </span>")
        link_box2.pack_start(web , True, True, 0)

        #TUTORIAL
        tutorial_link=''
        if entorno_usu.find('es') >= 0:
            tutorial_link = 'https://slimbook.es/es/tutoriales/aplicaciones-slimbook/515-slimbook-intel-controller'
        else:
            tutorial_link = 'https://slimbook.es/en/tutoriales/aplicaciones-slimbook/514-en-slimbook-intel-controller'

        tutorial = Gtk.Label()
        tutorial.set_markup("<span><b><a href='"+tutorial_link+"'>"+(_("@SlimbookIntelController Tutorial")+"</a></b>    </span>"))
        tutorial.set_justify(Gtk.Justification.CENTER)
        link_box2.pack_start(tutorial , True, True, 0)

        email = Gtk.Label()
        email.set_markup("<span><b>"+_("Send an e-mail a: ")+"dev@slimbook.es</b></span>")
        email.set_justify(Gtk.Justification.CENTER)
        email.set_name('label')
    
    # PACKKING ----------------------------------------------------------------------

        win_grid.attach(evnt_close,9,0,1,1)

        win_grid.attach(iconApp,0,0,10,1)

        win_grid.attach(info_grid,0,1,10,15)

        


        info_grid.attach(info,1,2,1,1)

        info_grid.attach(enlaces_box,1,3,1,1)

        info_grid.attach(link_box2,1,4,1,1)

        info_grid.attach(email,1,5,1,1)

        info_grid.attach(link_box2,1,6,1,1)

        info_grid.attach(salvavidas,1,7,1,1)

        info_grid.attach(license1,1,8,1,1)

        info_grid.attach(license2,1,9,1,1)

        info_grid.attach(licencia,1,10,1,1)

        info_grid.attach(info2,1,11,1,1)

        info_grid.attach(info3,1,12,1,1)


        #SHOW
        self.show_all()
    
    def on_buttonCopyEmail_clicked(self, buttonCopyEmail):
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.set_text('dev@slimbook.es', -1)
        os.system("notify-send 'Slimbook AMD Controller' "+_("'The email has been copied to the clipboard'") + " -i '" + currpath + "/images/icono.png'")

    def on_button_close(self, button, state):
        self.close()
        self.hide()
        self.destroy()
        Gtk.main_quit

dialog = PreferencesDialog()
dialog.connect("destroy", Gtk.main_quit)
dialog.show_all()
Gtk.main()



