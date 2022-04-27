#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess

import gi

import utils

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf

# IDIOMAS ----------------------------------------------------------------

# pygettext -d slimbookamdcontrollercopy slimbookamdcontrollercopy.py

CURRRENT_PATH = os.path.dirname(os.path.realpath(__file__))

_ = utils.load_translation('slimbookintelcontrollerinfo')

USER_NAME = utils.get_user()
HOMEDIR = subprocess.getoutput("echo ~" + USER_NAME)

# Adding CSS
style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRRENT_PATH + '/css/style.css')

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


class PreferencesDialog(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title='')

        ICON = os.path.join(CURRRENT_PATH + '/images/slimbookintelcontroller.svg')

        try:
            self.set_icon_from_file(ICON)
        except Exception:
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
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRRENT_PATH + '/images/logo-sb.png',
            width=200,
            height=100,
            preserve_aspect_ratio=True)
        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.set_name('logo')

        info = Gtk.Label()
        info.set_markup('<span>{}</span>'.format(
            _("The Slimbook Intel Controller app is capable of setting several TDP "
              "power levels for your Intel mobile processor. "
              "Switching between the different performance presets will give you the ability to control "
              "both performance and battery life with a single click. "
              "Bear in mind that the higher you set your performance level, "
              "your processor will also run hotter and drain your battery faster, so keep that in mind! \n\n"
              "Slimbook Intel Controller uses the third party software intel-undervolt from kitsunyan.")
        ))
        info.set_line_wrap(True)
        info.set_name('label')

        info2 = Gtk.Label()
        info2.set_markup("<span>{}<a href='https://www.patreon.com/slimbook'> patreon </a>{}</span>".format(
            _('If you want to support the Slimbook team with the development of this app and several more to come, '
              'you can do so by joining our '),
            _(' or buying a brand new Slimbook.')
        ))
        info2.set_line_wrap(True)
        info2.set_name('label')

        info3 = Gtk.Label()

        info3.set_markup("<span><b>{}</b>{}</span>".format(
            _("Note: "),
            _("Many laptops limit the power of the CPU, when working without the charger connected. "
              "Therefore, if you want to take advantage of the high-performance mode of this application, "
              "you may need to connect the charger.")
        ))
        info3.set_line_wrap(True)
        info3.set_name('label')

        warning = Gtk.Label(label=_('This software is provided * as is * without warranty of any kind..'))
        warning.set_name('label')

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRRENT_PATH + '/images/cc.png',
            width=100,
            height=50,
            preserve_aspect_ratio=True)

        licencia = Gtk.Image.new_from_pixbuf(pixbuf)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRRENT_PATH + '/images/cross.png',
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
        enlaces_box = Gtk.Box(spacing=5)
        enlaces_box.set_halign(Gtk.Align.CENTER)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=CURRRENT_PATH + '/images/twitter.png',
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
            filename=CURRRENT_PATH + '/images/facebook.png',
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
            filename=CURRRENT_PATH + '/images/insta.png',
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

        # WEB
        web_link = ''
        idiomas = utils.get_languages()[0]
        if idiomas.find('es') >= 0:
            web_link = 'https://slimbook.es/es/'
        else:
            web_link = 'https://slimbook.es/en/'

        # TUTORIAL
        tutorial_link = ''
        if idiomas.find('es') >= 0:
            tutorial_link = 'https://slimbook.es/es/tutoriales/aplicaciones-slimbook/515-slimbook-intel-controller'
        else:
            tutorial_link = 'https://slimbook.es/en/tutoriales/aplicaciones-slimbook/514-en-slimbook-intel-controller'

        label77 = Gtk.LinkButton(uri=web_link, label=_("Visit @Slimbook web"))
        label77.set_halign(Gtk.Align.CENTER)
        link_box2.add(label77)

        label77 = Gtk.LinkButton(uri=tutorial_link, label=_("@SlimbookIntelController Tutorial"))
        label77.set_halign(Gtk.Align.CENTER)
        link_box2.add(label77)

        label77 = Gtk.LinkButton(uri="https://github.com/slimbook/slimbookintelcontroller/tree/developing/src/translations",
                                 label=_('Help us with translations!'))
        label77.set_halign(Gtk.Align.CENTER)
        link_box2.add(label77)

        email = Gtk.Label()
        email.set_markup("<span><b>" + _("Send an e-mail to: ") + "dev@slimbook.es</b></span>")
        email.set_justify(Gtk.Justification.CENTER)
        email.set_name('label')

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(CURRRENT_PATH, 'images', 'GitHub_Logo_White.png'),
            width=150,
            height=30,
            preserve_aspect_ratio=True)

        img = Gtk.Image()
        img.set_from_pixbuf(pixbuf)

        github = Gtk.LinkButton(uri="https://github.com/slimbook/slimbookintelcontroller")
        github.set_name('link')
        github.set_halign(Gtk.Align.CENTER)
        github.set_image(img)

    # PACKKING ----------------------------------------------------------------------

        win_grid.attach(evnt_close, 9, 0, 1, 1)

        win_grid.attach(iconApp, 0, 0, 10, 1)

        win_grid.attach(info_grid, 0, 1, 10, 15)

        info_grid.attach(info, 1, 2, 1, 1)

        info_grid.attach(enlaces_box, 1, 3, 1, 1)

        info_grid.attach(link_box2, 1, 4, 1, 1)

        info_grid.attach(github, 1, 5, 1, 1)

        info_grid.attach(email, 1, 6, 1, 1)

        info_grid.attach(warning, 1, 7, 1, 1)

        info_grid.attach(info2, 1, 11, 1, 1)

        info_grid.attach(info3, 1, 12, 1, 1)

        info_grid.attach(licencia, 1, 13, 1, 1)

        # SHOW
        self.show_all()

    def on_button_close(self, button, state):
        self.close()
        self.hide()
        self.destroy()
