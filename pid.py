################################################
with open('temps.txt','w') as myfile:
        myfile.write('')

import Tkinter as tk
import webbrowser

window=tk.Tk()

temperature=28

temp1=tk.DoubleVar()

temp1.set(temperature)

set_temp=60

Heater=False

set_temp1=tk.DoubleVar()

set_temp1.set(set_temp)

def create_graph(event):
        global time_interval

        import matplotlib.pyplot as plt
        import numpy as np

        f=open('temps.txt','r')

        text=f.read()

##        print(text)

        temps_graph=np.array(text.split())
        times_graph=np.arange(0,time_interval*len(temps_graph),time_interval)

        fig=plt.figure(1)
        plt.clf()
        ax1=fig.add_subplot(111)
        ax1.grid(which='major')
        ax1.minorticks_on()
        ax1.grid(which='minor')

        ax1.set_ylabel(r'Temperature ($^{o}C$)')
        ax1.set_xlabel(r'Time (s)')

##        print(times_graph)
##        print(temps_graph)

        ax1.plot(times_graph,temps_graph)

        

        plt.show()

        plt.savefig('testfig.png')

##        webbrowser.open('/home/pi/robogaia_temperature_controller/testfig.png')

        ##sys.exit()
        

def update_set_point(event):
    global set_point_entry, set_temp1,errors_I
    set_temp1.set(set_point_entry.get())
    errors_I[:]=[]

def close_program(event):
## STOP HEATER HERE
        with open('temps.txt','w') as myfile:
                myfile.write('')
        sys.exit()

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

temp_current=tk.Label(window,textvariable=temp1).grid(row=3,column=1)

graph_button=tk.Button(window, text='Open graph')
graph_button.grid(row=6)
graph_button.bind('<Button-1>',create_graph)

close_button=tk.Button(window, text='Exit program')
close_button.grid(row=7)
close_button.bind('<Button-1>',close_program)

if Heater==True:
    heater_on=tk.Label(window, text='HEATER ON', background='green')
    heater_on.grid(row=4)
    window.update()
if Heater==False:
    heater_off=tk.Label(window, text='HEATER OFF', background='red',fg='white')
    heater_off.grid(row=4)
    window.update()



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

errors_I=[]
errors_D=[]
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
	Heater=False
	
def heat():
	print "heating"
	call(["temp_relay_on", "hot"])
	#call(["temp_relay_off", "cold"])
	Heater=True
	

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
	
Kp=30
Ki=0
Kd=0

##time_interval=float(raw_input('Enter temperature measurement time interval: '))

time_interval=2

##duty_cycle = float(raw_input('Enter heating duty cycle (percent): '))

duty_cycle=55

i=0

def foreground():
    global duty_cycle,temps,times,i

    while True:
        
##        print'Duty cycle foreground: ',duty_cycle
        temp1.set(get_celsius_val())
        temps=np.append(temps,[temp1.get()])
        times=np.append(times,[i])

##        print(temps)
##        print 'temperature: ', temp1.get()
        with open('temps.txt','a') as myfile:
                myfile.write(str(temp1.get())+' ')
        
        error=set_temp1.get()-temp1.get()
        errors_I.append(error)
        errors_D.append(error)
        P=Kp*error
        integral=sum(errors_I)*time_interval
        I=Ki*(integral+(error*time_interval))

        if len(errors_D)>=6:
            derivative_term=(errors_D[i]-errors_D[i-2])/(2*time_interval)
        elif len(errors_D)>=2:
                derivative_term=(errors_D[i]-errors_D[i-1])/(time_interval)
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
##set_temp = float(raw_input('Enter set temperature: '))
set_temp=60
##period = float(raw_input('Enter period: '))
period=6

# if len (sys.argv) < 2 :
#   print "Usage: temperature_hold  [temperature] "
# 	sys.exit (1)
# set_point=sys.argv[1]
try:
	set_point=float(set_temp)
except ValueError:
	print "the argument is not a number"
	sys.exit (1)
##print "set point = " , set_point
##print "temperature hysteresis =" , temperature_hysteresis
	
#main loop
loop = True

b=threading.Thread(name='background',target=background)
f=threading.Thread(name='foreground',target=foreground)


b.start()
f.start()          

window.mainloop()
