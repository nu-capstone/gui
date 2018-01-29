#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports

class ppg_graph(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        label = tk.Label(master,text="SHM Simulation").grid(column=0, row=0)

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(ppg_highlevel))
        button2.grid(row = 0, column = 0)

        fig = plt.Figure()
        x = np.arange(0, 2*np.pi, 0.01)        # x-array
        master = tk.Tk()
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.get_tk_widget().grid(column=0,row=1)

        ax = fig.add_subplot(111)
        line, = ax.plot(x, np.sin(x))
        ani = animation.FuncAnimation(fig, self.animate, np.arange(1, 200), interval=25, blit=False)

    def animate(i):
        line.set_ydata(np.sin(x+i/10.0))  # update the data
        return line,
