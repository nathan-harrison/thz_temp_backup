import smbus
import time
import datetime
from subprocess import call
import sys
import numpy as np
import matplotlib.pyplot as plt
import threading
import matplotlib.animation as animation
##    from matplotlib import style

plt.ioff()
bus = smbus.SMBus(1)

#I2C addres
address = 0x4d

#this will tell how low will go until the heater starts again below the set point
temperature_hysteresis = 2
safe_level = 80 #deg C
isHeating = True
plot = True
temps = np.array([0])
errors=[]
time_interval = 2

fig = plt.figure(1)

def animate(i):
    global temps
    times = np.arange(len(temps))*time_interval
    print(times)
    print(temps)
    plt.clf()
    ax = fig.add_subplot(111)
    ax.plot(times, np.asarray(temps))

  
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
        time.sleep((duty_cycle/100)*period)
        cool()
        time.sleep(period-((duty_cycle/100)*period))
	
Kp=0.2
Ki=0.5
time_interval=float(raw_input('Enter temperature measurement time interval: '))

duty_cycle = float(raw_input('Enter heating duty cycle (percent): '))

def foreground():
    global duty_cycle

    ani=animation.FuncAnimation(fig,animate,interval=100000)
    plt.show()
    
    while True:
        print('Duty cycle foreground: ',duty_cycle)
        temperature = get_celsius_val()
        print temperature
        np.append(temps,[temperature])
        error=set_temp-temperature
        errors.append(error)
        P=Kp*error
        integral=sum(errors)*time_interval
        I=Ki*(integral+(error*time_interval))

        if (P+I)>100:
            duty_cycle=100
        else:
            duty_cycle=P+I
        print P+I
        time.sleep(time_interval)


initialise()
isHeating = True
set_temp = float(raw_input('Enter set temperature: '))
period = float(raw_input('Enter period: '))

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

        

            
            
    
