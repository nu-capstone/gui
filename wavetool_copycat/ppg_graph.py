
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib
import numpy as np
from numpy import arange, sin, pi
import Tkinter as tk 
from PIL import Image, ImageTk
import tkFont
import pdb
from scipy import signal

#create image with format (time,x,y)
data = np.random.rand(1000,10,10)
ecg_data = np.genfromtxt('ecg.csv', delimiter = ',')
ppg_data = np.genfromtxt('ppg.csv', delimiter = ',')
#print(_data.size)
#pdb.set_trace()
condition_set = ('Normal', 'Warning', 'Critical')
deg =  u"\u00b0"
#setup figure
ecg_fig = plt.figure()
ppg_fig = plt.figure()
ecg_fig.set_size_inches(6,3.5)
ppg_fig.set_size_inches(6,3.5)
ecg_ax = ecg_fig.add_subplot(1,1,1)
ppg_ax = ppg_fig.add_subplot(1,1,1)

ecg_ax.set_frame_on(False)
ppg_ax.set_frame_on(False)

ecg_ax.grid(color = '#add8e6', linestyle='--')
ppg_ax.grid(color = '#add8e6', linestyle='--', )

ecg_ax.set_facecolor('black')
ppg_ax.set_facecolor('black')

#set up viewing window (in this case the 25 most recent values)
repeat_length = (np.shape(ecg_data)[0]+1)/10
ecg_ax.set_xlim([0,repeat_length])
ppg_ax.set_xlim([0,repeat_length])

ecg_ax.set_ylim([np.amin(ecg_data),np.amax(ecg_data)])
ppg_ax.set_ylim([np.amin(ppg_data),np.amax(ppg_data)])

#set up list of images for animation

ecg_im, = ecg_ax.plot([], [], color=(0,0,1))
ppg_im, = ppg_ax.plot([], [], color=(1,0,1))

def func(n):
    #pdb.set_trace()



    ecg_im.set_xdata(np.arange(n))
    ecg_im.set_ydata(ecg_data[0:n])
    ppg_im.set_xdata(np.arange(n))
    ppg_im.set_ydata(ppg_data[0:n])
    #pdb.set_trace()

    heartbeat_var = np.random.randint(40, 60)
    SP02_var = np.random.randint(20, 30)
    temp_var = np.random.randint(98, 102)
    pulse_transit_var = np.random.randint(50, 55)
    abnormal_var = condition_set[np.random.randint(0, 3)]

    #pdb.set_trace()
    heartbeat_label.configure(text = heartbeat_var)
    SP02_label.configure(text = SP02_var)
    temp_label.configure(text = temp_var)
    pulse_transit_label.configure(text = pulse_transit_var)
    abnormal_label.configure(text = abnormal_var)

    if n>repeat_length:
        lim1 = ecg_ax.set_xlim(n-repeat_length, n)
        lim2 = ppg_ax.set_xlim(n-repeat_length, n)
        #lim3 = ecg_ax.set_ylim(0,n)
        #ecg_ax.relim()
        #ecg_ax.autoscale() #autoscale
        lim3 = ecg_ax.set_ylim([np.amin(ecg_data[n-repeat_length:n]),np.amax(ecg_data[n-repeat_length:n])])
        lim4 = ppg_ax.set_ylim([np.amin(ppg_data[n-repeat_length:n]),np.amax(ppg_data[n-repeat_length:n])])
    else:
        # makes it look ok when the animation loops
        #pdb.set_trace()
        lim1 = ecg_ax.set_xlim(0, repeat_length)
        lim2 = ppg_ax.set_xlim(0, repeat_length)
        lim3 = ecg_ax.set_ylim([np.amin(ecg_data[0:repeat_length]), np.amax(ecg_data[0:repeat_length])])
        lim4 = ppg_ax.set_ylim([np.amin(ppg_data[0:repeat_length]), np.amax(ppg_data[0:repeat_length])])



        #ecg_ax.relim()
        #ecg_ax.autoscale()      
        #lim3 = ecg_ax.set_ylim([np.amin(ecg_data[0,repeat_length]), np.amax(ecg_data[0, repeat_length])])
        #lim4 = ppg_ax.set_ylim([0, np.amax(ppg_data[0, repeat_length])])
        #pdb.set_trace()

    return ecg_im, ppg_im

root = tk.Tk()
root.title('HeartBox Wavetool')
root.minsize(width=900, height = 700)

heartbeat_var = tk.IntVar()
SP02_var = tk.IntVar()
temp_var = tk.IntVar()
pulse_transit_var = tk.IntVar()
abnormal_var = tk.StringVar()

heartbeat_var = np.random.randint(40, 60)
SP02_var = np.random.randint(20, 30)
temp_var = np.random.randint(98, 102)
pulse_transit_var = np.random.randint(50, 55)
abnormal_var = condition_set[np.random.randint(0, 3)]


text_monitor_frame = tk.LabelFrame(root, bd = 3, text = "Vitals", font = 8, padx = 5)
text_monitor_frame.grid(column = 1, row = 1, rowspan = 2, padx = 10)
text_monitor_frame.rowconfigure(1, weight = 1)
text_monitor_frame.rowconfigure(2, weight = 1)

heartbeat_frame = tk.Frame(text_monitor_frame, bd = 1, relief="raised", width = 500)
SP02_frame = tk.Frame(text_monitor_frame, bd = 1, relief="raised", width = 500)
temp_frame = tk.Frame(text_monitor_frame, bd = 1, relief="raised", width = 500)
pulse_transit_frame = tk.Frame(text_monitor_frame, bd = 1, relief="raised", width = 500)
abnormal_frame = tk.Frame(text_monitor_frame, bd = 1, relief="raised", width = 500)

heartbeat_frame.columnconfigure(0, weight = 1)
heartbeat_frame.columnconfigure(1, weight = 1)

SP02_frame.columnconfigure(0, weight = 1)
SP02_frame.columnconfigure(1, weight = 1)

temp_frame.columnconfigure(0, weight = 1)
temp_frame.columnconfigure(1, weight = 1)

pulse_transit_frame.columnconfigure(0, weight = 1)
pulse_transit_frame.columnconfigure(1, weight = 1)

abnormal_frame.columnconfigure(0, weight = 1)
abnormal_frame.columnconfigure(1, weight = 1)

heartbeat_frame.grid(row = 0, column = 0)
SP02_frame.grid(row = 1, column = 0)
temp_frame.grid(row = 2, column = 0)
pulse_transit_frame.grid(row = 3, column = 0)
abnormal_frame.grid(row = 4, column = 0)

heartbeat_text = tk.Label(heartbeat_frame, text = "ECG  HR", anchor ="w", width = 40)
SP02_text = tk.Label(SP02_frame, text = "SpO2  %", anchor ="w", width = 40)
temp_text = tk.Label(temp_frame, text = "TEMP  " + deg + "F", anchor ="w", width = 40)
pulse_transit_text = tk.Label(pulse_transit_frame, text = "PULSE TRANSIT TIME  MS", anchor ="w", width = 40)
abnormal_text = tk.Label(abnormal_frame, text = "ABNORMAL HB", anchor ="w", width = 40)

heartbeat_text.config(font=(None, 9))
SP02_text.config(font=(None,9))
temp_text.config(font=(None, 9))
pulse_transit_text.config(font=(None, 9))
abnormal_text.config(font=(None, 9))

heartbeat_label = tk.Label(heartbeat_frame, text = heartbeat_var, width = 6, pady = 10)
SP02_label = tk.Label(SP02_frame, text = SP02_var, width = 6, pady = 10)
temp_label = tk.Label(temp_frame, text = temp_var, width = 6, pady = 10)
pulse_transit_label = tk.Label(pulse_transit_frame, text = pulse_transit_var, width = 6, pady = 10)
abnormal_label = tk.Label(abnormal_frame, text = abnormal_var, width = 6, pady = 10)

heartbeat_label.config(font=(None, 60))
SP02_label.config(font=(None, 60))
temp_label.config(font=(None, 60))
pulse_transit_label.config( font=(None, 60))
abnormal_label.config(font=(None, 40))

heartbeat_text.grid(row = 0, column = 0, columnspan = 2)
SP02_text.grid(row = 0, column = 0, columnspan = 2)
temp_text.grid(row = 0, column = 0, columnspan = 2)
pulse_transit_text.grid(row = 0, column = 0, columnspan = 2)
abnormal_text.grid(row = 0, column = 0, columnspan = 2)

heartbeat_label.grid(row = 1, column = 0, columnspan = 2)
SP02_label.grid(row = 1, column = 0, columnspan = 2)
temp_label.grid(row = 1, column = 0, columnspan = 2)
pulse_transit_label.grid(row = 1, column = 0, columnspan = 2)
abnormal_label.grid(row = 1, column = 0, columnspan = 2)



ecg_graph_frame = tk.LabelFrame(root, bd = 3, text = "ECG Raw Data")
ecg_graph_frame.grid(column = 0, row = 1)
ecg_canvas = FigureCanvasTkAgg(ecg_fig, master=ecg_graph_frame)
ecg_canvas.get_tk_widget().grid(column=0,row=0)

ppg_graph_frame = tk.LabelFrame(root, bd = 3, text = "PPG Raw Data")
ppg_graph_frame.grid(column = 0, row = 2)
ppg_canvas = FigureCanvasTkAgg(ppg_fig, master=ppg_graph_frame)
ppg_canvas.get_tk_widget().grid(column=0,row=0)

curr_anim = []
ecg_figcomp = ecg_fig, ecg_ax
ppg_figcomp = ppg_fig, ppg_ax

for figcomps in [ecg_figcomp, ppg_figcomp]:
    fig,ax = figcomps
    curr_anim.append(animation.FuncAnimation(fig, func, frames=ecg_data.shape[0], interval=10, blit=False))

plt.show

tk.mainloop()