from configparser import ConfigParser

import gi
import os
import re
import utils

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

USER_NAME = utils.get_user()
HOMEDIR = os.path.expanduser('~')

CONFIG_FILE = '{}/.config/slimbookintelcontroller/slimbookintelcontroller.conf'.format(
    HOMEDIR)
PROCESSORS_FILE = '{}/processors/available'.format(CURRENT_PATH)

config = ConfigParser()
config.read(CONFIG_FILE)

_ = utils.load_translation('slimbookintelcontroller')

CPU = utils.get_cpu_info('name')

patron = re.compile('(\w\d)[-]([0-9]{4,5})(\w*)[ ]')
version = patron.search(CPU).group(1)
number = patron.search(CPU).group(2)
line_suffix = patron.search(CPU).group(3)

MODEL_CPU = version+'-'+number+line_suffix

class Add_processor(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog")
        self.parent = parent
        self.set_name('dialog')
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(500, 100)

        label = Gtk.Label(label=_(
            "Your processor is not supported yet. Do you want to add {} to the list?\n"+
            "If this is the case, you should go to the Intel page and get information about your TDP values.").format(MODEL_CPU))
        label.set_line_wrap(True)
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class Settings(Gtk.Window):
    FIELDS = {
                'H': '35@40/40@45/45@54/35/45/54/',
                'U': '10@12/12@18/15@28/10/15/25/',
            }

    print('aaaaaaaaaaaaaaaaaaaaaaaaa '+FIELDS.get(line_suffix))
        
    # for row, data in enumerate(FIELDS):
    #     data.get(line_suffix)
    
    try:
        # Array
        values = config['PROCESSORS'][MODEL_CPU].split('/')

        print('Loads:  '+str(values)+' from file.')
    except:
        try:
            values = FIELDS.get(line_suffix).split('/')
        except:
            values = ['0@0', '0@0', '0@0', '0', '0', '0']
        
        proc_found = False
        val = '{}/{}/{}/{}/{}/{}/?'.format(values[0],values[1],values[2],values[3],values[4],values[5])
        print('Creates loads:  '+val+'.')
        # 
    

    lowmode = (values[0].split('@'))
    midmode = (values[1].split('@'))
    highmode = (values[2].split('@'))

    low_default = float(values[3])
    mid_default = float(values[4])
    high_default = float(values[5])

    def __init__(self):

        # WINDOW
        Gtk.Window.__init__(self, title="Slimbook Intel Controller Settings")
        self.set_position(Gtk.WindowPosition.CENTER)
        # self.set_size_request(500, 300)  # anchoxalto
        self.set_resizable(False)
        self.set_name('settings')

        center = Gtk.Align.CENTER
        left = Gtk.Align.START
        right = Gtk.Align.END

        win_grid = Gtk.Grid(column_homogeneous=False,
                            row_homogeneous=True,
                            column_spacing=10,
                            row_spacing=10)

        grid = Gtk.Grid(column_homogeneous=False,
                        row_homogeneous=True,
                        column_spacing=20,
                        row_spacing=10)

        self.add(win_grid)

        # Mantained TDP Column

        label1 = Gtk.Label(label=_('Mantained TDP'))

        self.entry1 = _create_gui_element(
            float(self.lowmode[0]), self.low_default, self.high_default + 10)

        self.entry2 = _create_gui_element(
            float(self.midmode[0]), self.low_default, self.high_default + 10)

        self.entry3 = _create_gui_element(
            float(self.highmode[0]), self.low_default, self.high_default + 10)

        grid.attach(self.entry1, 1, 1, 1, 1)
        grid.attach(self.entry2, 1, 2, 1, 1)
        grid.attach(self.entry3, 1, 3, 1, 1)
        grid.attach(label1, 1, 0, 1, 1)

        # High Power TDP Column

        label2 = Gtk.Label(_('High Power TDP'))

        self.entry4 = _create_gui_element(
            float(self.lowmode[1]), self.low_default, self.high_default + 10)

        self.entry5 = _create_gui_element(
            float(self.midmode[1]), self.low_default, self.high_default + 10)

        self.entry6 = _create_gui_element(
            float(self.highmode[1]), self.low_default, self.high_default + 10)

        grid.attach(self.entry4, 2, 1, 1, 1)
        grid.attach(self.entry5, 2, 2, 1, 1)
        grid.attach(self.entry6, 2, 3, 1, 1)
        grid.attach(label2, 2, 0, 1, 1)

        # Modes Column

        low_lbl = Gtk.Label(label=_('Low'), halign=left)

        mid_lbl = Gtk.Label(label=_('Medium'), halign=left)

        high_lbl = Gtk.Label(label=_('High'), halign=left)

        grid.attach(low_lbl, 0, 1, 1, 1)
        grid.attach(mid_lbl, 0, 2, 1, 1)
        grid.attach(high_lbl, 0, 3, 1, 1)

        separator = Gtk.Separator.new(orientation=Gtk.Orientation.HORIZONTAL)
        win_grid.attach(separator, 0, 4, 5, 1)

        # Recommended Values

        recommended_lbl = Gtk.Label(
            label=_('Recommended values:'), halign=left)

        win_grid.attach(recommended_lbl, 0, 5, 1, 1)

        low_lbl = Gtk.Label(
            label=_('Low: {} watts'.format(self.low_default)), halign=left)

        mid_lbl = Gtk.Label(
            label=_('Medium: {} watts'.format(self.mid_default)), halign=left)

        high_lbl = Gtk.Label(
            label=_('HIgh: {} watts.'.format(self.high_default)), halign=left)

        values_box = Gtk.VBox()
        values_box.add(low_lbl)
        values_box.add(mid_lbl)
        values_box.add(high_lbl)

        win_grid.attach(values_box, 0, 6, 2, 2)

        # Buttons
        accept_btn = Gtk.Button(label=_('Accept'))
        accept_btn.connect('clicked', self.accept)

        cancel_btn = Gtk.Button(label=_('Cancel'))
        cancel_btn.connect('clicked', self.close)

        win_grid.attach(grid, 0, 0, 5, 4)
        win_grid.attach(accept_btn, 4, 7, 1, 1)
        win_grid.attach(cancel_btn, 3, 7, 1, 1)

        accept_btn.grab_focus()

    def accept(self, button):
        new_values = '{}@{}/{}@{}/{}@{}/'.format(self.entry1.get_text(),
                                           self.entry4.get_text(),
                                           self.entry2.get_text(),
                                           self.entry5.get_text(),
                                           self.entry3.get_text(),
                                           self.entry6.get_text())

        if config.has_option('PROCESSORS',MODEL_CPU):
            print('Proc added')
            config.set('CONFIGURATION','cpu', new_values)

        else: 
            print('Proc not added')
            config.set('PROCESSORS', MODEL_CPU, new_values)
            config.set('CONFIGURATION','cpu', self.val)
            print(config['PROCESSORS'][MODEL_CPU])

        with open(CONFIG_FILE, 'w') as configfile:
                config.write(configfile)

    def close(self, button=None):
        Gtk.main_quit()

class main():
    
    print(MODEL_CPU)
    # print(config.items('PROCESSORS'))
    
    if config.has_option('PROCESSORS',MODEL_CPU):
        proc_found = True
    else:
        proc_found = False

    def __init__(self):
        
        if not self.proc_found:
            dialog = Add_processor(self)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                print("The OK button was clicked")
                self.proc_found = True

            elif response == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")
            dialog.destroy()

        if self.proc_found:
            
            dialog = Settings()
            dialog.connect("destroy", Gtk.main_quit)
            dialog.show_all()


def _create_gui_element(value, low, max):

    spin_button = Gtk.SpinButton()
    spin_button.set_adjustment(Gtk.Adjustment(
        value=value,
        lower=low,
        upper=max,
        step_incr=1,
        page_incr=10,
    ))

    spin_button.set_numeric(True)

    return spin_button


style_provider = Gtk.CssProvider()
style_provider.load_from_path(CURRENT_PATH+'/css/style.css')

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(), style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

main()
Gtk.main()
