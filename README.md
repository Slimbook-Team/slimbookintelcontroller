# Slimbook Intel Controller

Slimbook Intel Controller works by setting your CPU TDP value. That is, the amount of power measured in watts that you CPU is allowed to draw to save battery or to improve the overall performance under heavy workloads like rendering jobs or serious number crunching on large spreadsheets. Increasing the TDP allows the CPU to use its boost frequency more often or even permanently on some scenarios.

Use this software with caution as the heat output will increase dramatically on the higher performance settings, we can't guarantee that all INTEL CPU's will behave the same way, so your mileage may vary.

Slimbook Intel Controller is designed with mobile intel pocessors in mind. 
If you want to try the software in any other CPU, you can add it to the configuration file  /home/*(username)*/.config/slimboookintelcontroller/slimbookintelcontroller.conf

NOTE: Secureboot enabled does not allow kernel to manage CPU parameters.


![image](https://user-images.githubusercontent.com/18195266/124899040-02f1c700-dfe0-11eb-9c46-9e33484d44d8.png)


# Install
```bat
   sudo add-apt-repository ppa:slimbook/slimbook
   sudo apt install slimbookintelcontroller
```


![image](https://user-images.githubusercontent.com/18195266/124899253-39c7dd00-dfe0-11eb-9ea1-afc14d5ac9a7.png)




Here you have link to the app tutorial! --> [App tutorial](https://slimbook.es/en/tutoriales/aplicaciones-slimbook/514-en-slimbook-intel-controller)
--

# Colaborate
Help us coding, suggest ideas, everyone is welcome! --> <span style="font-size:larger;">[To do list](https://github.com/slimbook/slimbookintelcontroller/projects/2)</span>



This software is protected with the GPLv3 license, which allows you to modify it with the same license and authorship. 

Thank you.

