################################################

import Tkinter as tk

window=tk.Tk()

temperature=28

temp1=tk.DoubleVar()

temp1.set(temperature)

set_temp=60

Heater=False

set_temp1=tk.DoubleVar()

set_temp1.set(set_temp)

def update_set_point(event):
    global set_point_entry, set_temp1
    set_temp1.set(set_point_entry.get())

def close_program(event):
## STOP HEATER HERE
    exit()

set_point_label=tk.Label(window,text='Enter set-point temperature (degrees celsius): ').grid(row=0)

window.title('Temperature Controller')

frame=tk.Frame(window).grid()

set_point_entry=tk.Entry(window)

set_point_entry.grid(row=0,column=1)

update_set_point_button=tk.Button(window, text='Update set-point')

update_set_point_button.grid(row=0, column=2)

update_set_point_button.bind('<Button-1>',update_set_point)

set_point_current_intro=tk.Label(window,text='''Temperature set-point
(degrees celsius): ''').grid(row=2,column=0)

set_point_current=tk.Label(window,textvariable=set_temp1).grid(row=2,column=1)

temp_current_intro=tk.Label(window,text='''Current temperature
(degrees celsius):''').grid(row=3,column=0)

set_point_current=tk.Label(window,textvariable=temp1).grid(row=3,column=1)

close_button=tk.Button(window, text='Exit program')
close_button.grid(row=6)
close_button.bind('<Button-1>',close_program)

if Heater==True:
    heater_on=tk.Label(window, text='HEATER ON', background='green')
    heater_on.grid(row=4)
else:
    heater_off=tk.Label(window, text='HEATER OFF', background='red',fg='white')
    heater_off.grid(row=4) 

window.mainloop()

################################################


import smbus
import time
import datetime
from subprocess import call
import sys
import numpy as np
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
##    from matplotlib import style

####graph=plt.figure()
####ax1=graph.add_subplot(1,1,1)

times=np.array([0])
temps=np.array([0])

##def animate(j):
##        ax1.plot(times, temps)

##ani=animation.FuncAnimation(graph,animate,interval=1000)
##plt.show()

bus = smbus.SMBus(1)

#I2C addres
address = 0x4d

#this will tell how low will go until the heater starts again below the set point
temperature_hysteresis = 2
safe_level = 80 #deg C
isHeating = True
plot = True

errors=[]
time_interval = 2
 
def get_fahrenheit_val(): 
	data = bus.read_i2c_block_data(address, 1,2)
	val = (data[0] << 8) + data[1]
	return val/5.00*9.00/5.00+32.00
def get_celsius_val(): 
	data = bus.read_i2c_block_data(address, 1,2)
	val = (data[0] << 8) + data[1]
	return val/5.00
   
def initialise():
	print "initialising..."
	call(["temperature_controller_init"])
   
def cool():
	print "cooling"
	#call(["temp_relay_on", "cold"])
	call(["temp_relay_off", "hot"])
	
def heat():
	print "heating"
	call(["temp_relay_on", "hot"])
	#call(["temp_relay_off", "cold"])	
	

def close():
	print "close"
	#call(["temp_relay_off", "cold"])
	call(["temp_relay_off", "hot"])

def background():
    
    while True:
        heat()
        if duty_cycle>=0:
            time.sleep((duty_cycle/100)*period)
        cool()
        if duty_cycle>=0:
            time.sleep(period-((duty_cycle/100)*period))
        else:
            time.sleep(period)
	
Kp=20.5
Ki=0.06
Kd=16

##time_interval=float(raw_input('Enter temperature measurement time interval: '))

time_interval=4

##duty_cycle = float(raw_input('Enter heating duty cycle (percent): '))

duty_cycle=55

i=0

def foreground():
    global duty_cycle,temps,times,i

    while True:
        
##        print'Duty cycle foreground: ',duty_cycle
        temperature = get_celsius_val()
        temps=np.append(temps,[temperature])
        times=np.append(times,[i])

        print(temps)
        print 'temperature: ', temperature
        with open('temps.txt','a') as myfile:
                myfile.write(str(temperature)+' ')
        
        error=set_temp-temperature
        errors.append(error)
        P=Kp*error
        integral=sum(errors)*time_interval
        I=Ki*(integral+(error*time_interval))

        if len(errors)>=6:
            derivative_term=(errors[i]-errors[i-5])/(5*time_interval)
        elif len(errors)>=2:
                derivative_term=(errors[i]-errors[i-1])/(time_interval)
        else:
                derivative_term=0

        i+=1
        
        D=Kd*derivative_term
        print'Actual PID: ',P+I+D

        if (P+I+D)>100:
            duty_cycle=100
        elif (P+I+D)==0:
            duty_cycle=0
        else:
            duty_cycle=P+I+D
        time.sleep(time_interval)


initialise()
isHeating = True
set_temp = float(raw_input('Enter set temperature: '))
##period = float(raw_input('Enter period: '))
period=3

# if len (sys.argv) < 2 :
#   print "Usage: temperature_hold  [temperature] "
# 	sys.exit (1)
# set_point=sys.argv[1]
try:
	set_point=float(set_temp)
except ValueError:
	print "the argument is not a number"
	sys.exit (1)
print "set point = " , set_point
print "temperature hysteresis =" , temperature_hysteresis
	
#main loop
loop = True

b=threading.Thread(name='background',target=background)
f=threading.Thread(name='foreground',target=foreground)


b.start()
f.start()          

window.mainloop()
