import matplotlib.pyplot as plt
import numpy as np

f=open('temps.txt','r')

text=f.read()

temps_graph=np.array(text.split())
times_graph=np.arange(len(temps_graph))

fig=plt.figure(1)
plt.clf()
ax1=fig.add_subplot(111)
ax1.grid(which='major')
ax1.minorticks_on()
ax1.grid(which='minor')

ax1.plot(times_graph,temps_graph)

##plt.show()

plt.savefig('testfig.png')

##sys.exit()
