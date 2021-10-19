#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import configparser
import getpass
import os
import pwd
import shutil
import subprocess

USER_NAME = getpass.getuser()
if USER_NAME == 'root':
    USER_NAME = subprocess.getoutput('last -wn1 | head -n 1 | cut -f 1 -d " "')

HOMEDIR = os.path.expanduser('~{}'.format(USER_NAME))

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CONF = os.path.join(CURRENT_PATH, 'slimbookintelcontroller.conf')
CONFIG_FOLDER = os.path.join(HOMEDIR, '.config/slimbookintelcontroller')
CONFIG_FILE = os.path.join(CONFIG_FOLDER, 'slimbookintelcontroller.conf')

uid, gid =  pwd.getpwnam(USER_NAME).pw_uid, pwd.getpwnam(USER_NAME).pw_gid

def main():    


    if not (os.path.isdir(CONFIG_FOLDER) == True):
        print('Creating config folder ...')
        os.umask(0)
        os.makedirs(CONFIG_FOLDER, mode=0o766) # creates with perms 
        os.chown(CONFIG_FOLDER, uid, gid) # set user:group 
        print(subprocess.getoutput('ls -la '+CONFIG_FOLDER))
    else:
        print('Configuration folder ('+CONFIG_FOLDER+') found!')

    check_config_file()

    


def check_config_file():
    print('Checking Slimbook Intel Controller Configuration')
    if os.path.isfile(CONFIG_FILE):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        default_config = configparser.ConfigParser()
        default_config.read(DEFAULT_CONF)
        incidences = False

        for section in default_config.sections():
            print('Checking section: ' + section + '...')
            if not config.has_section(section):
                incidences = True
                config.add_section(section)
                print('Section added')

            for var in default_config.options(section):
                if not config.has_option(section, var):
                    incidences = True
                    print('Not found: ' + var)
                    config.set(section, var, default_config.get(section, var))

        if incidences:
            try:
                configfile = open(CONFIG_FILE, 'w')
                config.write(configfile)
                configfile.close()
                print('Incidences corrected.')
            except Exception:
                print('Incidences could not be corrected.')
        else:
            print('Incidences not found.')
    else:
        print('Creating config file ...')
        shutil.copy(DEFAULT_CONF, CONFIG_FOLDER)



if __name__ == '__main__':
    print('Config check executed as ' + USER_NAME)
    main()
