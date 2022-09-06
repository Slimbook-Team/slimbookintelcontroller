from configparser import ConfigParser

import gi
import os
import utils

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

USER_NAME = utils.get_user()
HOMEDIR = os.path.expanduser("~")

CONFIG_FILE = "{}/.config/slimbookintelcontroller/slimbookintelcontroller.conf".format(
    HOMEDIR
)

config = ConfigParser()
config.read(CONFIG_FILE)

_ = utils.load_translation("slimbookintelcontroller")

cpu, model_cpu, version, number, line_suffix = utils.get_cpu_info("name")

MODEL_CPU = version + "-" + number + line_suffix


class WarnDialog(Gtk.Dialog):
    def __init__(self, parent, label):
        super().__init__(title=_("Warning"), transient_for=parent)
        self.set_name("warn")
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(500, 100)

        label.set_line_wrap(True)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class SettingsDialog(Gtk.Dialog):
    FIELDS = {
        "H": "35@40/40@45/45@54/ 35/45 w",
        "U": "10@12/12@18/15@28/ 10/15/25 w",
        "G1": "13@15/13@18/15@28/ 13/15/25 w",
        "P": "20@28/24@32/28@64/ 20/28/64 w",
    }

    def __init__(self, parent):
        if (
            config.has_option("CONFIGURATION", "cpu-parameters")
            and config["CONFIGURATION"]["cpu-parameters"] != ""
        ):
            values = config["CONFIGURATION"]["cpu-parameters"]
            print("Loads:  " + str(values) + " from file.")
            print("1", values)
        elif (
            config.has_option("PROCESSORS", model_cpu)
            and config["PROCESSORS"][model_cpu] != ""
        ):
            values = config["PROCESSORS"][model_cpu]
            print("Loads:  " + str(values) + " from file.")
            print("2", values)
        else:
            values = (
                self.FIELDS.get(line_suffix)
                if self.FIELDS.get(line_suffix)
                else "0@0/0@0/0@0/ 0/0/0 w"
            )
            print("3", values)

        values = values.split(" ")
        values = list(filter(str.strip, values))

        for count, value in enumerate(values):
            values[count] = value.split("/")
            try:
                values[count].pop(values[count].index(""))
            except:
                pass

        values, default_values = values[0], values[1]
        # print(values, default_values)
        if len(default_values) == 2:
            self.low_default = float(default_values[0])
            self.mid_default = float(default_values[1])
            self.high_default = float(default_values[1])

        elif len(default_values) == 3:
            self.low_default = float(default_values[0])
            self.mid_default = float(default_values[1])
            self.high_default = float(default_values[2])

        self.values_str = "/{}/ {} w".format(
            ("/").join(values), ("/").join(default_values)
        )

        lowmode = values[0].split("@")
        midmode = values[1].split("@")
        highmode = values[2].split("@")

        super().__init__(
            title="Slimbook Intel Controller Settings", transient_for=parent
        )
        self.set_name("dialog")
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        # WINDOW
        self.set_name("settings")
        center = Gtk.Align.CENTER
        left = Gtk.Align.START
        right = Gtk.Align.END

        win_grid = Gtk.Grid(
            column_homogeneous=False,
            row_homogeneous=True,
            column_spacing=10,
            row_spacing=10,
        )

        grid = Gtk.Grid(
            column_homogeneous=False,
            row_homogeneous=True,
            column_spacing=20,
            row_spacing=10,
        )

        self.get_content_area().add(win_grid)

        # Mantained TDP Column
        if self.low_default < 20:
            min = self.low_default - self.low_default / 2
        else:
            min = self.low_default - 3 * (self.low_default / 4)
        max = self.high_default * 2

        label1 = Gtk.Label(label=_("Mantained TDP"))

        self.entry1 = _create_gui_element(float(lowmode[0]), min, max)
        self.entry2 = _create_gui_element(float(midmode[0]), min, max)
        self.entry3 = _create_gui_element(float(highmode[0]), min, max)

        grid.attach(self.entry1, 1, 1, 1, 1)
        grid.attach(self.entry2, 1, 2, 1, 1)
        grid.attach(self.entry3, 1, 3, 1, 1)
        grid.attach(label1, 1, 0, 1, 1)

        # High Power TDP Column

        label2 = Gtk.Label(label=_("High Power TDP"))

        self.entry4 = _create_gui_element(float(lowmode[1]), min, max)
        self.entry5 = _create_gui_element(float(midmode[1]), min, max)
        self.entry6 = _create_gui_element(float(highmode[1]), min, max)

        grid.attach(self.entry4, 2, 1, 1, 1)
        grid.attach(self.entry5, 2, 2, 1, 1)
        grid.attach(self.entry6, 2, 3, 1, 1)
        grid.attach(label2, 2, 0, 1, 1)

        # Modes Column
        low_lbl = Gtk.Label(label=_("Low"), halign=left)

        mid_lbl = Gtk.Label(label=_("Medium"), halign=left)

        high_lbl = Gtk.Label(label=_("High"), halign=left)

        grid.attach(low_lbl, 0, 1, 1, 1)
        grid.attach(mid_lbl, 0, 2, 1, 1)
        grid.attach(high_lbl, 0, 3, 1, 1)

        separator = Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_valign(center)
        win_grid.attach(separator, 0, 4, 5, 1)

        # Recommended Values
        recommended_lbl = Gtk.Label(label=_("Recommended values:"), halign=left)

        win_grid.attach(recommended_lbl, 0, 5, 1, 1)

        low_lbl = Gtk.Label(
            label=_("Low: {} watts".format(self.low_default)), halign=left
        )

        mid_lbl = Gtk.Label(
            label=_("Medium: {} watts".format(self.mid_default)), halign=left
        )

        high_lbl = Gtk.Label(
            label=_("High: {} watts.".format(self.high_default)), halign=left
        )

        values_box = Gtk.VBox()
        values_box.add(low_lbl)
        values_box.add(mid_lbl)
        values_box.add(high_lbl)

        win_grid.attach(values_box, 0, 6, 2, 2)

        win_grid.attach(grid, 0, 0, 5, 4)

        self.show_all()


class DialogWin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Slimbook Intel Controller")

        if cpu.find("Intel") != -1:
            if not config.has_option("PROCESSORS", MODEL_CPU):
                label = Gtk.Label(
                    label=_(
                        "Your processor is not supported yet. Do you want to add {} to the list?\n"
                        + "If this is the case, you should go to the Intel page and get information about your TDP values."
                    ).format(MODEL_CPU)
                )

                dialog = WarnDialog(self, label)
                response = dialog.run()
                dialog.close()
                dialog.destroy()

            dialog = SettingsDialog(self)
            dialog.show_all()
            response = dialog.run()
            config.read(CONFIG_FILE)

            if response == Gtk.ResponseType.OK:
                self.accept(dialog)
                dialog.close()
                dialog.destroy()

            elif response == Gtk.ResponseType.CANCEL:
                dialog.close()
                dialog.destroy()
        else:
            label = Gtk.Label(label=_("Any Intel processor detected!"))
            dialog = WarnDialog(self, label)
            response = dialog.run()
            if response:
                dialog.close()
                dialog.destroy()

    def accept(self, dialog):
        new_values = "{}@{}/{}@{}/{}@{}/  {}/{}/{}/".format(
            dialog.entry1.get_text(),
            dialog.entry4.get_text(),
            dialog.entry2.get_text(),
            dialog.entry5.get_text(),
            dialog.entry3.get_text(),
            dialog.entry6.get_text(),
            int(dialog.low_default),
            int(dialog.mid_default),
            int(dialog.high_default),
        )

        if config.has_option("PROCESSORS", MODEL_CPU):
            print("Processor values modified.")
            config.set("CONFIGURATION", "cpu-parameters", new_values)
        else:
            print("Processor added")
            config.set("PROCESSORS", MODEL_CPU, dialog.values_str)
            config.set("CONFIGURATION", "cpu-parameters", new_values)
            print(config["PROCESSORS"][MODEL_CPU])

        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)


def _create_gui_element(value, low, max):
    spin_button = Gtk.SpinButton()
    spin_button.set_adjustment(
        Gtk.Adjustment(
            value=value,
            lower=low,
            upper=max,
            step_increment=1,
            page_increment=10,
        )
    )
    spin_button.set_numeric(True)
    return spin_button


style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH + "/css/style.css")

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
if __name__ == "__main__":
    DialogWin()
    Gtk.main()
