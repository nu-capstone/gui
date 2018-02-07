#!/usr/bin/env python
import Tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.use("TkAgg")
from numpy import arange, sin, pi
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

class ppg_graph:
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		fig = plt.Figure()
		x = np.arange(0, 2*np.pi, 0.01)        # x-array
		canvas = FigureCanvasTkAgg(fig, master=master)
		canvas.get_tk_widget().grid(column=0,row=1)

		ax = fig.add_subplot(111)
		line, = ax.plot(x, np.sin(x))
		ani = animation.FuncAnimation(fig, self.animate, np.arange(1, 200), interval=25, blit=False)

	def animate(i):
		line.set_ydata(np.sin(x+i/10.0))  # update the data
		return line,

	def show(self):
		self.lift()
