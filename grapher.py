time_interval=float(input('Enter temperature measurement time interval: '))

import matplotlib.pyplot as plt
import numpy as np

f=open('/home/pi/thz_temp/robogaia_temperature_controller_filtered/temps.txt','r')

text=f.read()

temps_graph=np.array(text.split())
times_graph=np.arange(0,time_interval*len(temps_graph),time_interval)

fig=plt.figure(1)
plt.clf()
ax1=fig.add_subplot(111)
ax1.grid(which='major')
##ax1.minorticks_on()
ax1.grid(which='minor')

ax1.set_ylabel(r'Temperature ($^{o}C$)')
ax1.set_xlabel(r'Time (s)')

##        print(times_graph)
##        print(temps_graph)

ax1.plot(times_graph,temps_graph)

        

plt.show()
