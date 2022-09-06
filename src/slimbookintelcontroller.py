#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
import gi
import math
import subprocess
import re  # Busca patrones expresiones regulares

# We want load first current location
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
if CURRENT_PATH not in sys.path:
    sys.path = [CURRENT_PATH] + sys.path

import utils
import slimbookintelcontrollerinfo as info

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from configparser import ConfigParser
from gi.repository import Gdk, Gtk, GdkPixbuf, GLib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

std_handler = logging.StreamHandler(sys.stdout)
std_handler.setLevel(logging.DEBUG)
std_formatter = logging.Formatter("%(message)s")
std_handler.setFormatter(std_formatter)

file_handler = None
try:
    file_handler = logging.FileHandler("/var/slimbookintelcontroller.log")
except PermissionError:
    logger.critical(
        "Cannot open log file /var/slimbookintelcontroller.log, using /tmp/slimbookintelcontroller.log"
    )
    file_handler = logging.FileHandler("/tmp/slimbookintelcontroller.log")
if file_handler:
    file_handler.setLevel(logging.ERROR)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
logger.addHandler(std_handler)

logger.debug("Gurrent path: {}".format(CURRENT_PATH))

USER_NAME = utils.get_user()
HOMEDIR = os.path.expanduser("~{}".format(USER_NAME))

CONFIG_FILE = os.path.join(
    HOMEDIR, ".config/slimbookintelcontroller/slimbookintelcontroller.conf"
)
LAUNCHER_DESKTOP = os.path.join(
    CURRENT_PATH, "slimbookintelcontroller-autostart.desktop"
)
AUTOSTART_DESKTOP = os.path.join(
    HOMEDIR, ".config/autostart/slimbookintelcontroller-autostart.desktop"
)

# IDIOMAS ----------------------------------------------------------------

_ = utils.load_translation("slimbookintelcontroller")

cpuinfo = utils.get_cpu_info("name")
cpu, model_cpu, version, number, line_suffix = (
    cpuinfo if cpuinfo else logger.critical("Cpu not found")
)
logger.debug(cpu)

config = ConfigParser()
config.read(CONFIG_FILE)

logger.debug(
    "CPU | Model: '{model_cpu}' | Version: {version} | "
    "CPU Numbers: {number} | CPU Letters: {line_suffix}.".format(
        model_cpu=model_cpu,
        version=version,
        number=number,
        line_suffix=line_suffix,
    )
)
logger.debug(CONFIG_FILE)


class SlimbookINTEL(Gtk.ApplicationWindow):

    modo_actual = ""
    indicador_actual = ""
    autostart_actual = ""
    parameters = ("", "", "")
    exec_indicator = True

    def __init__(self):
        # WINDOW
        Gtk.Window.__init__(self, title="Slimbook Intel Controller")
        icon = os.path.join(CURRENT_PATH, "images/slimbookintelcontroller.svg")
        if os.path.isfile(icon):
            self.set_icon_from_file(icon)
        else:
            logger.error("Icon not found {}".format(icon))

        self.set_decorated(False)
        # self.set_size_request(925,590) #anchoxalto
        self.set_position(Gtk.WindowPosition.CENTER)
        self.get_style_context().add_class("bg-image")

        # Movement
        self.active = True
        self.is_in_drag = False
        self.x_in_drag = 0
        self.y_in_drag = 0
        self.connect("button-press-event", self.on_mouse_button_pressed)
        self.connect("button-release-event", self.on_mouse_button_released)
        self.connect("motion-notify-event", self.on_mouse_moved)

        self.init_gui()

    def on_realize(self, widget):
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width) / 2, (monitor_height - height) / 2)

    def on_mouse_moved(self, widget, event):
        if self.is_in_drag:
            xi, yi = self.get_position()
            xf = int(xi + event.x_root - self.x_in_drag)
            yf = int(yi + event.y_root - self.y_in_drag)
            if math.sqrt(math.pow(xf - xi, 2) + math.pow(yf - yi, 2)) > 10:
                self.x_in_drag = event.x_root
                self.y_in_drag = event.y_root
                self.move(xf, yf)

    def on_mouse_button_released(self, widget, event):
        if event.button == 1:
            self.is_in_drag = False
            self.x_in_drag = event.x_root
            self.y_in_drag = event.y_root

    def on_mouse_button_pressed(self, widget, event):
        if event.button == 1 and self.active:
            self.is_in_drag = True
            self.x_in_drag, self.y_in_drag = self.get_position()
            self.x_in_drag = event.x_root
            self.y_in_drag = event.y_root
            return True
        return False

    def close_dialog(self, dialog):
        dialog.close()
        self.active = True

    def on_button_toggled(self, button, name):
        self.modo_actual = name

    def on_btnAceptar_clicked(self, widget):
        # Check secureboot
        exit_code, msg = subprocess.getstatusoutput(
            'mokutil --sb-state | grep -i "SecureBoot disabled"'
        )

        if exit_code:
            self.dialog(
                _("Secureboot Warning"),
                _(
                    "This computer has Secureboot enabled, which does not allow kernel to manage CPU parameters."
                ),
            )

        elif self.exec_indicator:
            # Comprobamos los switch
            self._inicio_automatico(self.switch1, self.switch1.get_state())
            self._show_indicator(self.switch2, self.switch2.get_state())

            # ACTUALIZAMOS VARIABLES
            config.set("CONFIGURATION", "mode", self.modo_actual)
            logger.debug(
                "Variable |   mode    | updated, actual value: {} ...".format(
                    self.modo_actual
                )
            )
            config.set("CONFIGURATION", "autostart", self.autostart_actual)
            logger.debug(
                "Variable | autostart | updated, actual value: {} ...".format(
                    self.modo_actual
                )
            )
            config.set("CONFIGURATION", "show-icon", self.indicador_actual)
            logger.debug(
                "Variable | show-icon | updated, actual value: {} ...".format(
                    self.modo_actual
                )
            )

            with open(CONFIG_FILE, "w") as configfile:
                config.write(configfile)

            logger.info("Updating: {} ...".format(CONFIG_FILE))

            if self.exec_indicator:
                self.reboot_indicator()

        else:
            self.dialog(
                _("CPU Warning"),
                _(
                    "Your CPU model is nor supported. To add it by your own, check the tutorial Link / "
                    "Github Link in the information window or contact us for more information."
                ),
            )

        Gtk.main_quit()

    def dialog(self, title, message, link=None):
        dialog = Gtk.MessageDialog(
            # transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.CLOSE,
            text=title,
        )

        dialog.format_secondary_text(message)

        dialog.set_position(Gtk.WindowPosition.CENTER)

        response = dialog.run()

        if response == Gtk.ResponseType.CLOSE:
            logger.info("WARN dialog closed by clicking CLOSE button")

        dialog.destroy()

    # Copies autostart file in directory
    def _inicio_automatico(self, switch, state):

        if switch.get_active() is True:
            os.system("pkexec slimbookintelcontroller-pkexec autostart enable")
            self.autostart_actual = "on"

        else:
            logger.info("Autostart Disabled")
            os.system("pkexec slimbookintelcontroller-pkexec autostart disable")
            self.autostart_actual = "off"

        logger.info("Autostart now: {}".format(self.autostart_actual))

    def _show_indicator(self, switch, state):

        if switch.get_active() is True:
            logger.info("Indicator Enabled")
            self.indicador_actual = "on"  # --> Luego esta variable será guardada y cargada desde el programa indicador
        else:
            logger.info("Indicator Disabled")
            self.indicador_actual = "off"

        config.set("CONFIGURATION", "show-icon", self.indicador_actual)
        logger.info("Indicator now: {}".format(self.indicador_actual))

    def init_gui(self):  # ---> UNFINISHED
        config.read(CONFIG_FILE)

        # GRIDS

        win_grid = Gtk.Grid(column_homogeneous=True, column_spacing=0, row_spacing=10)

        grid = Gtk.Grid(
            column_homogeneous=True,
            # row_homogeneous=True,
            column_spacing=0,
            row_spacing=25,
        )

        self.add(win_grid)

        # CONTENT --------------------------------------------------------------------------------

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(
                CURRENT_PATH, "images/slimbookintelcontroller_header.png"
            ),
            width=600,
            height=200,
            preserve_aspect_ratio=True,
        )

        header_img = Gtk.Image.new_from_pixbuf(pixbuf)
        header_img.set_halign(Gtk.Align.START)
        header_img.set_valign(Gtk.Align.START)

        label1 = Gtk.Label(label=_("Enable app at startup"))
        label1.set_halign(Gtk.Align.START)

        label2 = Gtk.Label(label=_("Show indicator icon"))
        label2.set_halign(Gtk.Align.START)

        button1 = Gtk.Button(label="Button 1")
        button1.set_halign(Gtk.Align.START)
        button1.get_style_context().add_class("button-none")

        button2 = Gtk.Button(label="Button 2")
        button2.set_halign(Gtk.Align.START)
        button2.get_style_context().add_class("button-none")

        self.switch1 = Gtk.Switch()
        self.switch1.set_halign(Gtk.Align.END)
        self.switch2 = Gtk.Switch()
        self.switch2.set_halign(Gtk.Align.END)

        rbutton1 = Gtk.RadioButton.new_with_label_from_widget(None, (_("Low")))
        rbutton2 = Gtk.RadioButton.new_with_mnemonic_from_widget(
            rbutton1, (_("Medium"))
        )
        rbutton3 = Gtk.RadioButton.new_with_mnemonic_from_widget(rbutton1, (_("High")))

        # Processor
        hbox_cpu = Gtk.HBox()

        cpu_name = Gtk.Label(label=cpu[cpu.find(":") + 1 :])
        cpu_name.set_halign(Gtk.Align.CENTER)
        hbox_cpu.set_name("cpu_info")

        hbox_cpu.pack_start(cpu_name, True, True, 0)

        # CPU Temp
        thermal_zones = subprocess.getstatusoutput(
            "ls /sys/class/thermal/ | grep thermal_zone"
        )[1].split("\n")

        cpu_thermal_zone = None
        for thermal_zone in thermal_zones:
            if (
                subprocess.getstatusoutput(
                    "cat /sys/class/thermal/" + thermal_zone + "/type | grep acpitz"
                )[0]
                == 0
            ):
                logger.info("Found thermal zone! ({})".format(thermal_zone))
                cpu_thermal_zone = thermal_zone

        if cpu_thermal_zone is not None:
            exit_code, cpu_temp = subprocess.getstatusoutput(
                r"cat /sys/class/thermal/{}/temp | sed 's/\(.\)..$/ °C/'".format(
                    cpu_thermal_zone
                )
            )
            if exit_code:
                label = Gtk.Label(label=cpu_temp)

                def _update_label(label: Gtk.Label):
                    label.set_label(
                        subprocess.getoutput(
                            r"cat /sys/class/thermal/{}/temp | sed 's/\(.\)..$/ °C/'".format(
                                cpu_thermal_zone
                            )
                        )
                    )
                    return True

                GLib.timeout_add_seconds(2, _update_label, label)
                hbox_cpu.pack_start(label, True, True, 0)
            else:
                logger.warning("Cpu_temp 404")
        else:
            logger.warning("Thermal_zone 404")

        separador = Gtk.Separator()
        separador.set_halign(Gtk.Align.CENTER)

        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(CURRENT_PATH, "images/cross.png"),
            width=20,
            height=20,
            preserve_aspect_ratio=True,
        )

        close = Gtk.Image.new_from_pixbuf(pixbuf1)
        close.get_style_context().add_class("close")

        evnt_close = Gtk.EventBox()
        evnt_close.set_valign(Gtk.Align.START)
        evnt_close.set_halign(Gtk.Align.END)
        evnt_close.add(close)
        evnt_close.connect("button_press_event", self.on_btnCerrar_clicked)

        menu = Gtk.Menu()
        menu.append(Gtk.MenuItem(label="lp"))
        menu.append(Gtk.MenuItem(label="pl"))

        pixbuf1 = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(CURRENT_PATH, "images/settings.png"),
            width=20,
            height=20,
            preserve_aspect_ratio=True,
        )

        settings = Gtk.Image.new_from_pixbuf(pixbuf1)
        evnt_settings = Gtk.EventBox()
        evnt_settings.set_valign(Gtk.Align.CENTER)
        evnt_settings.set_halign(Gtk.Align.END)
        evnt_settings.add(settings)
        evnt_settings.connect("button_press_event", self.settings)

        hbox_close = Gtk.HBox()
        hbox_close.set_valign(Gtk.Align.START)
        hbox_close.set_halign(Gtk.Align.END)
        hbox_close.add(evnt_settings)
        hbox_close.add(evnt_close)

        # RADIOS ---------------------------------------------------------------------------------

        modos = Gtk.Label(label="CHANGE CPU MODE")
        modos.get_style_context().add_class("modes")
        modos.set_halign(Gtk.Align.CENTER)

        # CAJA 1
        vbox1 = Gtk.VBox()
        rbutton1.connect("toggled", self.on_button_toggled, "low")
        rbutton1.set_name("radiobutton")
        rbutton1.set_halign(Gtk.Align.CENTER)

        rbutton1_img = Gtk.Image.new_from_file(
            os.path.join(CURRENT_PATH, "images/modo1.png")
        )
        rbutton1_img.set_halign(Gtk.Align.CENTER)

        vbox1.pack_start(rbutton1_img, False, False, 0)
        vbox1.pack_start(rbutton1, False, False, 0)

        # CAJA 2
        vbox2 = Gtk.VBox()
        rbutton2.connect("toggled", self.on_button_toggled, "medium")
        rbutton2.set_name("radiobutton")
        rbutton2.set_halign(Gtk.Align.CENTER)

        rbutton2_img = Gtk.Image.new_from_file(
            os.path.join(CURRENT_PATH, "images/modo2.png")
        )
        rbutton2_img.set_halign(Gtk.Align.CENTER)

        vbox2.pack_start(rbutton2_img, False, False, 0)
        vbox2.pack_start(rbutton2, False, False, 0)

        # CAJA 3
        vbox3 = Gtk.VBox()
        rbutton3.connect("toggled", self.on_button_toggled, "high")
        rbutton3.set_name("radiobutton")
        rbutton3.set_halign(Gtk.Align.CENTER)

        rbutton3_img = Gtk.Image.new_from_file(
            os.path.join(CURRENT_PATH, "images/modo3.png")
        )
        rbutton3_img.set_halign(Gtk.Align.CENTER)

        vbox3.pack_start(rbutton3_img, False, False, 0)
        vbox3.pack_start(rbutton3, False, False, 0)

        hbox_radios = Gtk.HBox()
        hbox_radios.add(vbox1)
        hbox_radios.add(vbox2)
        hbox_radios.add(vbox3)

        # BUTTONS --------------------------------------------------------------------------------

        botonesBox = Gtk.Box(spacing=10)
        botonesBox.set_name("botonesBox")
        botonesBox.set_halign(Gtk.Align.CENTER)
        botonesBox.set_name("buttons")

        # ACEPTAR
        btnAceptar = Gtk.ToggleButton(label=_("ACCEPT"))
        btnAceptar.set_size_request(125, 30)
        btnAceptar.connect("toggled", self.on_btnAceptar_clicked)
        botonesBox.pack_start(btnAceptar, True, True, 0)

        # CERRAR
        btnCancelar = Gtk.ToggleButton(label=_("CANCEL"))
        btnCancelar.set_size_request(125, 30)
        btnCancelar.connect("toggled", self.on_btnCerrar_clicked, "x")
        botonesBox.pack_start(btnCancelar, True, True, 0)
        botonesBox.set_valign(Gtk.Align.END)

        # BTNABOUT_US ----------------------------------------------------------------------------

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=os.path.join(CURRENT_PATH, "images/question.png"),
            width=20,
            height=20,
            preserve_aspect_ratio=True,
        )

        iconApp = Gtk.Image.new_from_pixbuf(pixbuf)
        iconApp.get_style_context().add_class("help")
        iconApp.set_halign(Gtk.Align.END)

        evnt_box = Gtk.EventBox()
        evnt_box.add(iconApp)

        evnt_box.connect("button_press_event", self.about_us)
        evnt_box.set_valign(Gtk.Align.END)
        evnt_box.set_halign(Gtk.Align.END)

        version_tag = Gtk.Label(label="")
        version_tag.set_halign(Gtk.Align.START)
        version_tag.set_valign(Gtk.Align.END)
        version_tag.set_name("version")

        version_parser = ConfigParser()
        # Try load system version
        version_parser.read("/usr/share/applications/slimbookintelcontroller.desktop")
        # Overwrite system version with local one (For develop version)
        version_parser.read(
            os.path.join(CURRENT_PATH, "../slimbookintelcontroller.desktop")
        )

        version = "Unknown"
        if version_parser.has_option("Desktop Entry", "Version"):
            version = version_parser.get("Desktop Entry", "Version")
            logger.info(version)

        version_tag.set_markup('<span font="10">Version {}</span>'.format(version))

        version_tag.set_justify(Gtk.Justification.CENTER)

        # GRID ATTACH ----------------------------------------------------------------------------

        grid.attach(label1, 1, 3, 3, 1)
        grid.attach(label2, 1, 4, 3, 1)

        grid.attach(self.switch1, 6, 3, 3, 1)
        grid.attach(self.switch2, 6, 4, 3, 1)

        grid.attach(hbox_cpu, 0, 5, 10, 1)

        grid.attach(modos, 0, 6, 10, 1)

        grid.attach(hbox_radios, 1, 7, 8, 1)

        # WIN GRID ATTACH ------------------------------------------------------------------------

        win_grid.attach(grid, 1, 2, 8, 10)
        win_grid.attach(header_img, 1, 0, 7, 4)
        win_grid.attach(hbox_close, 8, 0, 1, 1)
        win_grid.attach(evnt_box, 8, 12, 1, 1)
        win_grid.attach(version_tag, 1, 12, 2, 1)
        win_grid.attach(botonesBox, 1, 12, 8, 1)

        # Inicio automatico :):
        if config.getboolean("CONFIGURATION", "autostart"):
            # autostart
            self.autostart_actual = "on"
            self.switch1.set_active(True)
            logger.info("- Autostart enabled")
        else:
            self.autostart_actual = "off"
            self.switch2.set_active(False)
            logger.info("- Autostart disabled")

        # Mostramos indicador, o no :):
        if config.getboolean("CONFIGURATION", "show-icon"):
            self.indicador_actual = "on"
            self.switch2.set_active(True)
            logger.info("- Indicator enabled")

        else:
            self.indicador_actual = "off"
            self.switch2.set_active(False)
            logger.info("- Indicator disabled")

        # RadiobuttonSelection
        if config.get("CONFIGURATION", "mode") == "low":

            self.modo_actual = "low"
            rbutton1.set_active(True)

        elif config.get("CONFIGURATION", "mode") == "medium":

            self.modo_actual = "medium"
            rbutton2.set_active(True)

        else:
            self.modo_actual = "high"
            rbutton3.set_active(True)

        logger.info("- {}".format(self.modo_actual.capitalize()))

        self.show_all()
        logger.debug(model_cpu)
        # CPU Parameters
        if config.has_option("PROCESSORS", model_cpu):
            params = config.get("PROCESSORS", model_cpu).split("/")
            self.parameters = params
            logger.info("- CPU Parameters: {}".format(self.parameters))
            logger.info(".conf data loaded succesfully!")
        else:
            logger.error("Processor not found in list")
            self.exec_indicator = False
            self.settings()
            try:
                config.read(CONFIG_FILE)
                params = config.get("PROCESSORS", model_cpu).split("/")
                self.parameters = params
            except:
                self.exec_indicator = False

    def reboot_indicator(self):
        logger.info("Process PID")
        indicator = subprocess.getoutput("pgrep -f slimbookintelcontrollerindicator")
        logger.info(indicator)

        os.system("kill -9 " + indicator)
        logger.info(self.exec_indicator)
        if self.exec_indicator:
            logger.info("Starting indicator...")
            os.system(
                "python3 " + CURRENT_PATH + "/slimbookintelcontrollerindicator.py  &"
            )
        else:
            logger.error("Not launching indicator, exceptions found")

    def about_us(self, widget, x):
        logger.debug("About us ...")
        # Abre la ventana de info
        self.active = False
        dialog = info.PreferencesDialog()
        dialog.connect("destroy", self.close_dialog)
        dialog.show_all()

    def settings(self, widget=None, x=None):
        import settings

        self.active = False
        settings.DialogWin()

    def on_btnCerrar_clicked(self, widget=None, x=None):
        Gtk.main_quit()

    def update_config_file(self, variable, value):
        config.set("CONFIGURATION", str(variable), str(value))
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
        print("Variable |'{}' updated, actual value: {}\n".format(variable, value))

    def exit(self):
        Gtk.main_quit()
        sys.exit(0)


def main():
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path(os.path.join(CURRENT_PATH, "css/style.css"))

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    win = SlimbookINTEL()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()


if __name__ == "__main__":
    main()
