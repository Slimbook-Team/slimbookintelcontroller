#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import signal
import subprocess
import sys
import utils
import gi
import configuration

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import AyatanaAppIndicator3 as AppIndicator3
from gi.repository import Gtk, GdkPixbuf

srcpath = "/usr/share/slimbookintelcontroller/src"
sys.path.insert(1, srcpath)

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
USER_NAME = utils.get_user()
HOMEDIR = subprocess.getoutput("echo ~" + USER_NAME)
IMAGESPATH = os.path.join(CURRENT_PATH, "images")

config_file = os.path.join(
    HOMEDIR, ".config/slimbookintelcontroller/slimbookintelcontroller.conf"
)
config = configuration.read_conf(config_file)

pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
    filename="{}/images/slimbookintelcontroller_header.png".format(CURRENT_PATH),
    width=200,
    height=150,
    preserve_aspect_ratio=True,
)

_ = utils.load_translation("slimbookintelcontrollerindicator")

cpuinfo = utils.get_cpu_info("name")
cpu, model_cpu, version, number, line_suffix = cpuinfo if cpuinfo else exit()


class Indicator(object):
    mode = "none"
    parameters = ("", "", "")

    def __init__(self):
        self.app = "com.slimbook.intelcontroller"
        iconpath = "{}/images/".format(CURRENT_PATH)
        self.testindicator = AppIndicator3.Indicator.new(
            self.app, iconpath, AppIndicator3.IndicatorCategory.OTHER
        )

        self.testindicator.set_icon_theme_path(CURRENT_PATH + "/images/")
        self.testindicator.set_menu(self.create_menu())
        self.inicio()

    def create_menu(self):
        Gtk.Image.new_from_pixbuf(pixbuf)
        menu = Gtk.Menu()

        IMAGES = {
            "low": IMAGESPATH + "/{}".format("intel-green.png"),
            "medium": IMAGESPATH + "/{}".format("intel-blue.png"),
            "high": IMAGESPATH + "/{}".format("intel-red.png"),
        }

        low_mode_icon = Gtk.Image()
        low_mode_icon.set_from_file(IMAGES.get("low"))

        medium_mode_icon = Gtk.Image()
        medium_mode_icon.set_from_file(IMAGES.get("medium"))

        high_mode_icon = Gtk.Image()
        high_mode_icon.set_from_file(IMAGES.get("high"))

        low_mode_item = Gtk.ImageMenuItem(
            label=_("Low performance"), image=low_mode_icon
        )
        low_mode_item.connect("activate", self.lowperformance)
        low_mode_item.set_always_show_image(True)

        medium_mode_item = Gtk.ImageMenuItem(
            label=_("Medium performance"), image=medium_mode_icon
        )
        medium_mode_item.connect("activate", self.mediumperformance)
        medium_mode_item.set_always_show_image(True)

        high_mode_item = Gtk.ImageMenuItem(
            label=_("High performance"), image=high_mode_icon
        )
        high_mode_item.connect("activate", self.highperformance)
        high_mode_item.set_always_show_image(True)

        preferences_item = Gtk.MenuItem(label=_("Preferences"))
        preferences_item.connect("activate", self.openWindow)

        separator_item = Gtk.SeparatorMenuItem()

        item_quit = Gtk.MenuItem(label=_("Exit"))
        item_quit.connect("activate", self.exit)

        menu.append(low_mode_item)
        menu.append(medium_mode_item)
        menu.append(high_mode_item)
        menu.append(separator_item)
        menu.append(preferences_item)
        menu.append(item_quit)
        menu.show_all()

        return menu

    def exit(self, source):
        Gtk.main_quit()
        sys.exit(0)

    def openWindow(self, source):
        os.system("slimbookintelcontroller")

    def inicio(self):
        config.read(config_file)

        INDICATOR = {
            "on": AppIndicator3.IndicatorStatus.ACTIVE,
            "off": AppIndicator3.IndicatorStatus.PASSIVE,
        }
        option = (
            config.get("CONFIGURATION", "show-icon")
            if config.has_option("CONFIGURATION", "show-icon")
            else None
        )
        self.testindicator.set_status(INDICATOR[option])
        params = (
            config.get("PROCESSORS", model_cpu)
            if config.has_option("PROCESSORS", model_cpu)
            else None
        )

        if params:
            print("CPU Parameters: " + str(params))
            values = list(filter(str.strip, params.split(" ")))
            for count, value in enumerate(values):
                values[count] = value.split("/")
                try:
                    values[count].pop(values[count].index(""))
                except:
                    pass

            values = values[0]
            self.parameters = values

            print("\nData loaded from .conf\n")

            mode = (
                config.get("CONFIGURATION", "mode")
                if config.has_option("CONFIGURATION", "mode")
                else None
            )
            MODES = {
                "low": self.lowperformance,
                "medium": self.mediumperformance,
                "high": self.highperformance,
            }
            if mode:
                MODES.get(mode)()

        else:
            print(
                "\nProcessor parameters not defined in conf, open Preferences Window to configure.\n"
            )

    def update_config_file(self, variable, value):
        config.read(config_file)
        config.set("CONFIGURATION", str(variable), str(value))
        with open(config_file, "w") as configfile:
            config.write(configfile)
        print("Variable '{}' updated, actual value: {}\n".format(variable, value))

    def lowperformance(self, widget=None):
        mode = "low"
        values = self.parameters[0].split("@")
        self.testindicator.set_icon_full("intel-green", "Low mode")
        print(
            'Updating "{}" values: (original) {} {}'.format(mode, values[0], values[1])
        )
        self.update_config_file("mode", mode)
        os.system("pkexec /usr/bin/slimbookintelcontroller-pkexec")

    def mediumperformance(self, widget=None):
        mode = "medium"
        values = self.parameters[1].split("@")
        self.testindicator.set_icon_full("intel-blue", "Medium mode")
        print(
            'Updating "{}" values: (original) {} {}'.format(mode, values[0], values[1])
        )
        self.update_config_file("mode", mode)
        os.system("pkexec /usr/bin/slimbookintelcontroller-pkexec")

    def highperformance(self, widget=None):
        mode = "high"
        values = self.parameters[2].split("@")
        self.testindicator.set_icon_full("intel-red", "High mode")
        print(
            'Updating "{}" values: (original) {} {}'.format(mode, values[0], values[1])
        )
        self.update_config_file("mode", mode)
        os.system("pkexec /usr/bin/slimbookintelcontroller-pkexec")

if __name__=="__main__":

    pid_name = "slimbook.intel.controller.indicator.pid"
    utils.application_lock(pid_name)
    
    if utils.get_secureboot_status():
        print("Error: SecureBoot is enabled", file=sys.stderr)
        sys.exit(1)

    Indicator()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()
    
    utils.application_release(pid_name)
