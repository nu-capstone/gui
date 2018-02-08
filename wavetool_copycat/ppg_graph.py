from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib
import numpy as np
from numpy import arange, sin, pi
import Tkinter as tk 
from PIL import Image, ImageTk


#create image with format (time,x,y)
data = np.random.rand(1000,10,10)
condition_set = ('Normal', 'Warning', 'Critical')

#setup figure
ecg_fig = plt.figure()
ppg_fig = plt.figure()
ecg_fig.set_size_inches(6,3.5)
ppg_fig.set_size_inches(6,3.5)

ecg_ax = ecg_fig.add_subplot(1,1,1)
ppg_ax = ppg_fig.add_subplot(1,1,1)
#set up viewing window (in this case the 25 most recent values)
repeat_length = (np.shape(data)[0]+1)/4
ecg_ax.set_xlim([0,repeat_length])
ppg_ax.set_xlim([0,repeat_length])

#ax2.autoscale_view()
ecg_ax.set_ylim([np.amin(data[:,5,5]),np.amax(data[:,5,5])])
ppg_ax.set_ylim([np.amin(data[:,5,6]),np.amax(data[:,5,6])])

#set up list of images for animation

ecg_im, = ecg_ax.plot([], [], color=(0,0,1))
ppg_im, = ppg_ax.plot([], [], color=(1,0,1))

def func(n):
    ecg_im.set_xdata(np.arange(n))
    ecg_im.set_ydata(data[0:n, 5, 5])
    ppg_im.set_xdata(np.arange(n))
    ppg_im.set_ydata(data[0:n, 5, 6])


    heartbeat_var = np.random.randint(40, 60)
    SP02_var = np.random.randint(20, 30)
    temp_var = np.random.randint(98, 102)
    pulse_transit_var = np.random.randint(50, 55)
    abnormal_var = condition_set[np.random.randint(0, 3)]

    heartbeat_label.configure(text = heartbeat_var)
    SP02_label.configure(text = SP02_var)
    temp_label.configure(text = temp_var)
    pulse_transit_label.configure(text = pulse_transit_var)
    abnormal_label.configure(text = abnormal_var)

    if n>repeat_length:
        lim1 = ecg_ax.set_xlim(n-repeat_length, n)
        lim2 = ppg_ax.set_xlim(n-repeat_length, n)
    else:
        # makes it look ok when the animation loops
        lim1 = ecg_ax.set_xlim(0, repeat_length)
        lim2 = ppg_ax.set_xlim(0, repeat_length)
    return ecg_im, ppg_im

root = tk.Tk()
root.title('HeartBox Wavetool')
root.minsize(width=900, height = 1000)
root.resizable(width=False, height=False)

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


text_monitor_frame = tk.LabelFrame(root, bd = 3, text = "Vitals", width = 500, padx = 5)
text_monitor_frame.grid(column = 1, row = 1, rowspan = 2, padx = 10)
text_monitor_frame.rowconfigure(1, weight = 1)
text_monitor_frame.rowconfigure(2, weight = 1)

heartbeat_text = tk.Label(text_monitor_frame, text = "Heartbeat")
SP02_text = tk.Label(text_monitor_frame, text = "SpO2")
temp_text = tk.Label(text_monitor_frame, text = "Temperature")
pulse_transit_text = tk.Label(text_monitor_frame, text = "Pulse Transit Time")
abnormal_text = tk.Label(text_monitor_frame, text = "Abnormal Heartbeat")

heartbeat_label = tk.Label(text_monitor_frame, text = heartbeat_var, width = 20)
SP02_label = tk.Label(text_monitor_frame, text = SP02_var, width = 20)
temp_label = tk.Label(text_monitor_frame, text = temp_var, width = 20)
pulse_transit_label = tk.Label(text_monitor_frame, text = pulse_transit_var, width = 20)
abnormal_label = tk.Label(text_monitor_frame, text = abnormal_var, width = 20)

heartbeat_text.grid(row = 0, column = 0)
SP02_text.grid(row = 1, column = 0)
temp_text.grid(row = 2, column = 0)
pulse_transit_text.grid(row = 3, column = 0)
abnormal_text.grid(row = 4, column = 0)

heartbeat_label.grid(row = 0, column = 1)
SP02_label.grid(row = 1, column = 1)
temp_label.grid(row = 2, column = 1)
pulse_transit_label.grid(row = 3, column = 1)
abnormal_label.grid(row = 4, column = 1)

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
    curr_anim.append(animation.FuncAnimation(fig, func, frames=data.shape[0], interval=30, blit=False))

plt.show

tk.mainloop()