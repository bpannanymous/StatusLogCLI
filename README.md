# StatusLogCLI
Background TUI based tool to log temperature, fan, and power performance at a selected recording frequency and for a selected amount of datapoints



INSTALLATIONS
=================================================================================
No additional installations are necessary other than the libraries at the top of each of the .py files




USE
=================================================================================
'''
python StatusLog.py
'''



Compatibility Note
=================================================================================
This code is specifically aimed to be used for the ThinkPad T14 Gen 5 AMD but can EASILY be modified to be applicable to almost any other laptop running linux (not sure about other OS). All that needs to be changed is the 4 variables in StatusLog.py as follows:

'''
cpu_temp_path=Path("/sys/class/hwmon/hwmon5/temp1_input") #cpu temperature file
gpu_temp_path=Path("/sys/class/hwmon/hwmon6/temp1_input") #gpu temperature file
fan_speed_path=Path("/sys/class/hwmon/hwmon5/fan1_input") #fan speed file
power_path=Path("/sys/class/hwmon/hwmon3/power1_input") #power consumption file
'''

These variables correspond to the paths to the modules of the properties in the hwmon path. To make these fit your setup, you must first understand which of the hwmon paths corresponds to what sensor. This can be done using the following commands:

'''
cd /sys/class/hwmon/ && ls
'''

This will change the directory to the hwmon directory and list all hwmon modules available. You will then iteratively, for however many there are, run the following:

'''
cat hwmon0/name
'''

'''
cat hwmon1/name
'''

You will continue to do this so you can see the name of all of these modules. You will then open another terminal window beside it and run the following command:

'''
sensors
'''

You will see your sensor information, but also the names of the hwmon modules they are coming from. You will need to link these names to the name of one of the hwmon names that you filed through in the first terminal window. You will then, for example with cpu temperature, look into that module, say hwmon4, then list all of the files in there using:

'''
ls
'''

There should be a temp1_input. This does not mean that it is the cpu temperature, that will be up to your own discretion on how to determine that, but it is most likely that in the sensors window, the order that they are listed in under a respective hwmon feature is the same order they are numbered in under the module files. This is the path you need to put into the section I stated you much change above. To see the full path, run the following then add the actual sensor name (temp1_input) at the end:

'''
pwd
'''

Changing this accordingly will allow seamless integration of this script into your workflow. Note that in some cases this will not be able to relay the gpu temperature because it may not be linked through the hwmon modules. I don't know how to rectify that at this time, and instead opted to change that temperature reading to something else, for instance the nvme or other interface temperatures. Technically if you change only the path it will still work correctly,but if you want to change the chart axes and the TUI relaying statement so it doesn't say GPU Temperature anymore, you can do so in Functions.py. Anything you change in GeneralFunctions.py will most likely break the program in some way because those only address base level interaction that are virtually independent of the nature of this file.

You can also technically change one of the readings, for example gpu temperature, to be another reading, for example fan input. This will need an additional change in Functions.py because it uses a scale factor of 1000 that would need to be changed. I trust that if this idea came to you then you know how to do it, but otherwise you're free to reach out to me via email or discord (bpanan).
