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
