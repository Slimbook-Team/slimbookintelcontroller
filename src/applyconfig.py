#!/usr/bin/python3
# -*- coding: utf-8 -*-

#This file will be executed as sudo by pkexec
import os
import sys
import subprocess
import shutil
from time import sleep
from configparser import ConfigParser
import utils

print('SlimbookIntelController-Applyconfig, executed as: '+str(subprocess.getoutput('whoami')))

print(subprocess.getoutput("echo $USERNAME"))

USER_NAME = utils.get_user()
HOMEDIR = subprocess.getoutput("echo ~"+USER_NAME)

print("Homedir: "+HOMEDIR+"\n")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAUNCHER_DESKTOP = os.path.join(BASE_DIR, "slimbookintelcontroller-autostart.desktop")
print(LAUNCHER_DESKTOP)

AUTOSTART_DESKTOP = os.path.expanduser("{}/.config/autostart/slimbookintelcontroller-autostart.desktop".format(HOMEDIR))
print(AUTOSTART_DESKTOP)

config_file = HOMEDIR+'/.config/slimbookintelcontroller/slimbookintelcontroller.conf'


config = ConfigParser()
config.read(config_file)



#Commands:
# sudo intel-undervolt read
# sudo intel-undervolt apply
# sudo 

def main(args): # Args will be like --> command_name value

    print("Total Args --> "+ str(len(args)))
    # Argument 0 is the current route

    if len(args) > 1:
        print("Using "+args[1]+" ...")

        if args[1] == "plug":
            print(args[1])
            sleep(1)
            apply_all()
        
        elif args[1] == "post":
            print(args[1])
                   	
            call = subprocess.getstatusoutput("sudo intel-undervolt apply")
            print("Exit: "+str(call[0])) #To do after suspension
            
        elif args[1] == "autostart":
            if not os.path.exists ('/home/'+USER_NAME+'/.config/autostart/'):
                os.system('mkdir /home/'+USER_NAME+'/.config/autostart/')    
                print('Dir autostart created.')

            if args[2] == "enable":
                if not os.path.isfile(AUTOSTART_DESKTOP):
                    shutil.copy(LAUNCHER_DESKTOP, AUTOSTART_DESKTOP)
                    os.system('sudo chmod 755 '+AUTOSTART_DESKTOP)
                    print("File -autostart has been copied!.")

            elif args[2] == "disable":
                if os.path.isfile(AUTOSTART_DESKTOP):
                    os.remove(AUTOSTART_DESKTOP)                
                    print("File -autostart has been deleted.")
           

    else: #--> Apply all
        apply_all()

def apply_all():  
    os.system("cat "+config_file)

    cpu = config.get('CONFIGURATION', 'cpu')

    apply_params =''

    mode = config.get('CONFIGURATION', 'mode')

    if mode == 'low':
        params = config.get('PROCESSORS', cpu).split('/')
        apply_params = params[0].split("@")

    elif mode == 'medium':
        params = config.get('PROCESSORS', cpu).split('/')
        apply_params = params[1].split("@")

    elif mode == 'high':
        params = config.get('PROCESSORS', cpu).split('/')
        apply_params = params[2].split("@")

    #Turbo value goes first
    command ='power package '+apply_params[1]+'/3 '+apply_params[0]+'/30'

    line_number = subprocess.getstatusoutput("cat /etc/intel-undervolt.conf | grep 'Power Limits Alteration' -n | cut -d: -f1")
    
    if line_number[1] != '':

        print("Linea de titulo: "+str(int(line_number[1])-1)+" | Linea de comando: "+str(int(line_number[1])-2))

        # with is like your try .. finally block in this case
        with open('/etc/intel-undervolt.conf', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        # now change the line, note that you have to add a newline
        data[int(line_number[1])-2] = command+'\n'
        print(data[int(line_number[1])-2])

        # and write everything back
        with open('/etc/intel-undervolt.conf', 'w') as file:
            file.writelines( data )
    else: 

        print("Data not found")
    

    #Necesitamos sudo para modificar el config de intel-undervolt       
    call = subprocess.getstatusoutput("sudo intel-undervolt apply")

    print("sudo intel-undervolt apply --> Exit:"+str(call[0]))
        


if __name__ == "__main__":
    #Se obtiene las variables que se le pasa desde el archivo /usr/share/slimbookface/slimbookface
    main(sys.argv)