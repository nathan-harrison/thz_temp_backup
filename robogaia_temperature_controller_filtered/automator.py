props=[24]

ints=[0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.020,0.021,0.022,0.023,0.024,0.025,0.026,0.027,0.028,0.029,0.030,0.031,0.032,0.033,0.034,0.035]

sets=[]
p_gain=20
i_gain=0.04
time_interval=2.5
duty_cycle=0

################

on_secs=1500
off_secs=300

################

for prop in props:
    for int_ in ints:
        sets.append([prop,int_])

########################################

import smbus
import time
import datetime
from subprocess import call
import sys
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Tkinter as tk
import webbrowser
import csv
period=2
set_temp=60
bus = smbus.SMBus(1)
address = 0x4d
filterArray = [0 , 0, 0 , 0 , 0, 0, 0, 0] #holds the filter values
errors_I=[]
filename='data_dump.csv'

def filter(input_value):
    global filterArray
    filterArray.append(input_value);
    filterArray.pop(0);
    result = (filterArray[0] + filterArray[1]+ filterArray[2]+ filterArray[3]+ filterArray[4]+ filterArray[5]+ filterArray[6]+ filterArray[7])/8 ;
    stringFilterArray = [str(a) for a in filterArray];
    return result;

def get_celsius_val():
        global bus,data
	data = bus.read_i2c_block_data(address, 1,2)
	val = (data[0] << 8) + data[1]
	return val/5.00
   
def initialise():
	print( "initialising...")
	call(["temperature_controller_init"])

initialise()	
   
def cool():
	call(["temp_relay_off", "hot"])
	Heater=False
	
def heat():
	call(["temp_relay_on", "hot"])
	Heater=True

def background():
    global duty_cycle
    while True: # This loop turns the heater on and off at a rate set by the PID value
        heat()
        if duty_cycle>=0:
            time.sleep((duty_cycle/100)*period)
        cool()
        if duty_cycle>=0:
            time.sleep(period-((duty_cycle/100)*period))
        else:
            time.sleep(period)

def foreground():
    global duty_cycle,filename,time_interval,bus,data,set_temp,errors_I

    while True:
        temp=(filter(get_celsius_val()))
        if temp>100:
            sys.exit()
        # print'Temp: ',temp
        with open(filename,'a') as myfile:
                writer=csv.writer(myfile, delimiter=',')
                writer.writerow([temp,duty_cycle])
        
        error=set_temp-temp
        if float(error)<=5:
                errors_I.append(error)
        else:
                pass
        P=p_gain*error
        # print'P-gain: ',p_gain
        integral=sum(errors_I)*time_interval
        I=i_gain*(integral+(error*time_interval))
        # print'I-gain: ',i_gain

        if (P+I)>100:
            duty_cycle=100
        elif (P+I)<=0 or on==False:
            duty_cycle=0
        else:
            duty_cycle=P+I
        print 'Duty cycle:',duty_cycle
        time.sleep(time_interval)  
        
######################################

b=threading.Thread(name='background',target=background)
f=threading.Thread(name='foreground',target=foreground)

b.start()
f.start()          

for parameters in sets:

    # print(parameters)

    p_gain=parameters[0]

    i_gain=parameters[1]

    filename=str(p_gain).replace('.','-')+'_'+str(i_gain).replace('.','-')+'_automated_TRY3.csv'

    with open(filename,'w') as myfile: # Opens file that stores temperature data
            myfile.write('\n NEWNEWNEWNEWNEWNEWNEWNEWNEWNEWNEW \n') #Makes file blank

    errors_I=[]

    # print('on')

    on=True

    time.sleep(on_secs)

    # print('off')

    on=False

    filename='data_dump.csv'

    duty_cycle=0

    time.sleep(off_secs)

sys.exit()    
