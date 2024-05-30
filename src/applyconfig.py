#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This file will be executed as root by pkexec
import os
import sys
import subprocess
import shutil
from time import sleep
import utils
import configuration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_cpu = utils.get_cpu_info("name")[1]

def main(args):
    if len(args) > 1:
        if args[1] == "plug" and len(args) > 2:
            apply_all(args[2])

        elif args[1] == "post":
            call = subprocess.getstatusoutput("/usr/bin/intel-undervolt apply")

    sys.exit(0)

def apply_all(user_config):
    
    config = configuration.read_conf(user_config)

    mode = config.get("CONFIGURATION", "mode")
    if (
        not config.has_option("CONFIGURATION", "cpu-parameters")
        or config.get("CONFIGURATION", "cpu-parameters") == ""
    ):
        print("Getting original processor params")
        params = config.get("PROCESSORS", model_cpu)
    else:
        params = config.get("CONFIGURATION", "cpu-parameters")

    params = params.split(" ")[0].split("/")
    print(params)
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
        with open("/etc/intel-undervolt.conf", "w") as file:
            file.writelines(data)
    else:
        print("Data not found")

    call = subprocess.getstatusoutput("/usr/bin/intel-undervolt apply")

if __name__ == "__main__":
    main(sys.argv)
