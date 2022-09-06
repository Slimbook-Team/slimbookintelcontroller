#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This file will be executed as sudo by pkexec
import os
import sys
import subprocess
import shutil
from time import sleep
from configparser import ConfigParser
import utils

print(
    "SlimbookIntelController-Applyconfig, executed as: "
    + str(subprocess.getoutput("whoami"))
)

USER_NAME = utils.get_user()
HOMEDIR = subprocess.getoutput("echo ~" + USER_NAME)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAUNCHER_DESKTOP = os.path.join(BASE_DIR, "slimbookintelcontroller-autostart.desktop")

AUTOSTART_DESKTOP = os.path.expanduser(
    "{}/.config/autostart/slimbookintelcontroller-autostart.desktop".format(HOMEDIR)
)

model_cpu = utils.get_cpu_info("name")[1]

config_file = HOMEDIR + "/.config/slimbookintelcontroller/slimbookintelcontroller.conf"
config = ConfigParser()
config.read(config_file)

# Commands:
# sudo intel-undervolt read
# sudo intel-undervolt apply
# sudo


def main(args):  # Args will be like --> command_name value
    # Argument 0 is the current route
    if len(args) > 1:
        print("Using " + args[1] + " ...")

        if args[1] == "plug":
            print(args[1])
            sleep(1)
            apply_all()

        elif args[1] == "post":
            print(args[1])

            call = subprocess.getstatusoutput("sudo intel-undervolt apply")
            print("Exit: " + str(call[0]))  # To do after suspension

        elif args[1] == "autostart":
            if not os.path.exists("/home/" + USER_NAME + "/.config/autostart/"):
                os.system("mkdir /home/" + USER_NAME + "/.config/autostart/")
                print("Dir autostart created.")

            if args[2] == "enable":
                if not os.path.isfile(AUTOSTART_DESKTOP):
                    shutil.copy(LAUNCHER_DESKTOP, AUTOSTART_DESKTOP)
                    os.system("sudo chmod 755 " + AUTOSTART_DESKTOP)
                    print("File -autostart has been copied!.")

            elif args[2] == "disable":
                if os.path.isfile(AUTOSTART_DESKTOP):
                    os.remove(AUTOSTART_DESKTOP)
                    print("File -autostart has been deleted.")

    else:  # --> Apply all
        apply_all()


def apply_all():
    mode = config.get("CONFIGURATION", "mode")
    params = (
        config.get("PROCESSORS", model_cpu).split("/")
        if not config.has_option("CONFIGURATION", "cpu-parameters")
        else config.get("CONFIGURATION", "cpu-parameters")
    )
    params = params.split(" ")[0].split("/")

    if mode == "low":
        apply_params = params[0].split("@")

    elif mode == "medium":
        apply_params = params[1].split("@")

    elif mode == "high":
        apply_params = params[2].split("@")

    # Turbo value goes first
    command = "power package " + apply_params[1] + "/3 " + apply_params[0] + "/30"

    line_number = subprocess.getstatusoutput(
        "cat /etc/intel-undervolt.conf | grep 'Power Limits Alteration' -n | cut -d: -f1"
    )

    if line_number[1] != "":
        with open("/etc/intel-undervolt.conf", "r") as file:
            # read a list of lines into data
            data = file.readlines()
        # now change the line, note that you have to add a newline
        data[int(line_number[1]) - 2] = command + "\n"
        # and write everything back
        with open("/etc/intel-undervolt.conf", "w") as file:
            file.writelines(data)
    else:
        print("Data not found")

    call = subprocess.getstatusoutput("sudo intel-undervolt apply")
    print("sudo intel-undervolt apply --> Exit:" + str(call[0]))


if __name__ == "__main__":
    # Se obtiene las variables que se le pasa desde el archivo /usr/share/slimbookface/slimbookface
    main(sys.argv)
