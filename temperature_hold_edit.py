#!/usr/bin/python

#robogaia.com
# the temperatures are in fahrenheit
# temperature_hysteresis sets how low the temperature
#goes until the heater starts

import smbus
import time
import datetime
from subprocess import call
import sys
import numpy
import matplotlib.pyplot as pyplot

bus = smbus.SMBus(1)

#I2C addres
address = 0x4d

#this will tell how low will go until the heater starts again below the set point
temperature_hysteresis = 5
safe_level = 80 #deg C
isHeating = True
plot = True
temps = []
time_interval = 5
  
def get_fahrenheit_val(): 
	data = bus.read_i2c_block_data(address, 1,2)
	val = (data[0] << 8) + data[1]
	return val/5.00*9.00/5.00+32.00
def get_celsius_val(): 
	data = bus.read_i2c_block_data(address, 1,2)
	val = (data[0] << 8) + data[1]
	return val/5.00
   
   
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
	


def main(argv):
	set_temp = raw_input('Enter set temperature')
	# if len (sys.argv) < 2 :
	# 	print "Usage: temperature_hold  [temperature] "
	# 	sys.exit (1)	
	# set_point=sys.argv[1]
	try:
		set_point=float(set_temp)
	except ValueError:
		print "the argument is not a number"
		sys.exit (1)
	print "set point =" , set_point
	print "temperature hysteresis =" , temperature_hysteresis
	
	#main loop
	while 1 == 1:
        	try:
            	#get the temperature from sensor
            		temperature = get_celsius_val()
            		print temperature
            
            		#safety cut-off!
            		if temperature > safe_level:
                		close()
                print 'Temperature exceeded safe level, exiting...'
                return
            #verify if we need to cool or to heat
            elif temperature > set_point:
                cool()
                isHeating = False
            elif temperature  <= (set_point- temperature_hysteresis):
                heat()
                isHeating = True
            elif isHeating == True and temperature  <= set_point:
                heat()
            else:
                print "something went wrong!"

            if plot:
                temps.append(temperature)
            time.sleep(time_interval)

        except KeyboardInterrupt:
			print '\n Caught KB interrupt signal\n'
            cont = raw_input("Continue? (y/n)")
            if cont == 'y':
                new_lvl = raw_input("Enter new set level:")
                set_point = int(float(new_lvl))    
            elif cont == 'n':     
                if plot:
                    times = numpy.arange(len(temps))*time_interval
                    pyplot.figure()
                    pyplot.plot(times, temps)
                    pyplot.show()
                print "Exiting loop"
                close()
                return

if __name__ == "__main__":
	main()
