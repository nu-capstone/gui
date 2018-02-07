import Tkinter as tk
import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style


class graph_viewer:
	def __init__(self, master):
		x = 7
	def create_graph(master):
		master.withdraw()
		graph_window = tk.Toplevel(master)


