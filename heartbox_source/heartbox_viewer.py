import settings
from heartbox_dsp import heartbox_dsp
import heartbox_comm
from ppg_highlevel import ppg_highlevel
import Tkinter as tk 
from PIL import Image, ImageTk
import tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib
import webbrowser

import numpy as np
from scipy import signal

import multiprocessing
import socket
import time
from struct import *
import subprocess
import pdb
#displays waveform/metric monitor to be viewed by users

class heartbox_wave_viewer:
	def __init__(self):
		self.root = tk.Tk()
		self.dsp = heartbox_dsp()
		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()
		self.min_screen_width = 1200
		self.min_screen_height = 700		
		self.root.attributes("-toolwindow", 1) 
		self.frame_num = 0

		self.root.configure(bg = settings.back_color)
		self.root.title('HeartBox Wavetool')

		self.root.minsize(width = self.min_screen_width, height = self.min_screen_height)
		#self.root.attributes("-zoomed", True)
		self.root.resizable(False, False)
		self.fullscreen_state = False

		self.heartbox_connect_state = False
		self.ecg_disconnect_state =True
		self.ppg_disconnect_state = True
		self.ppg_R_disconnect_state = True
		self.ppg_IR_disconnect_state = True
		self.android_connect_state= False

		self.vitals_title_font_size = 14 #default values for 1200x700 font
		self.vitals_subtitle_font_size = 14
		self.vitals_menubar_font_size = 10 
		self.vitals_text_font_size = 50
		self.vitals_subtext_font_size = 12

		plt.rcParams["font.family"] = "Consolas"
		self.vitals_title_font = tkFont.Font(family = 'Consolas', size = self.vitals_title_font_size)
		self.vitals_subtitle_font = tkFont.Font(family = 'Consolas', size = self.vitals_subtitle_font_size)
		self.vitals_menubar_font = tkFont.Font(family = 'Consolas', size = self.vitals_menubar_font_size)
		self.vitals_text_font = tkFont.Font(family = 'Consolas', size = self.vitals_text_font_size)
		self.vitals_subtext_font = tkFont.Font(family = 'Consolas', size = self.vitals_subtext_font_size)

		self.setup_plots()
		self.bind_shortcuts()
		self.menu_layout()
		self.graph_layout()
		self.vitals_layout()

	def startup(self):
		if (settings.isComm):
			self.simulate=multiprocessing.Process(None,heartbox_comm.heartbox_udp_receive,args=(settings.q,))
			self.simulate.start()
			self.read_live_samples()
		else:
			self.read_recorded_samples()

	#setup elements needed for plots
	def setup_plots(self):
		if (settings.isComm):
			self.ecg_data = np.array([])
			self.ppg_data = np.array([])
			self.ppg_R_data = np.array([])
			self.ppg_IR_data = np.array([])

		else:
			self.ecg_data = np.genfromtxt('ecg.csv', delimiter = ',')
			self.ppg_data = np.genfromtxt('ppg.csv', delimiter = ',')
		
		#setup figure
		self.ecg_fig = plt.figure()
		self.ppg_fig = plt.figure()
		self.ppg_R_fig = plt.figure()
		self.ppg_IR_fig = plt.figure()
		self.ecg_fig.set_size_inches(7,2.5)
		self.ppg_fig.set_size_inches(7,2.5)
		self.ppg_R_fig.set_size_inches(4,2.5)
		self.ppg_IR_fig.set_size_inches(4,2.5)

		self.ecg_ax = self.ecg_fig.add_subplot(1,1,1)
		self.ppg_ax = self.ppg_fig.add_subplot(1,1,1)
		self.ppg_R_ax = self.ppg_R_fig.add_subplot(1,1,1)
		self.ppg_IR_ax = self.ppg_IR_fig.add_subplot(1,1,1)
		plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

		self.ecg_ax.locator_params(axis='y', nbins =2)
		self.ecg_ax.locator_params(axis='x', nbins =2)
		self.ppg_ax.locator_params(axis='y', nbins =2)
		self.ppg_ax.locator_params(axis='x', nbins =2)
		self.ppg_R_ax.locator_params(axis='y', nbins =2)
		self.ppg_R_ax.locator_params(axis='x', nbins =2)
		self.ppg_IR_ax.locator_params(axis='y', nbins =2)
		self.ppg_IR_ax.locator_params(axis='x', nbins =2)

		self.ecg_fig.set_facecolor(settings.back_color) #colors the area surround figs
		self.ppg_fig.set_facecolor(settings.back_color)
		self.ppg_R_fig.set_facecolor(settings.back_color)
		self.ppg_IR_fig.set_facecolor(settings.back_color)

		self.ecg_ax.set_facecolor(settings.back_color) #colors the internal figure area/axes
		self.ppg_ax.set_facecolor(settings.back_color)
		self.ppg_R_ax.set_facecolor(settings.back_color)
		self.ppg_IR_ax.set_facecolor(settings.back_color)

		self.ecg_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)
		self.ppg_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)
		self.ppg_R_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)
		self.ppg_IR_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)

		self.ecg_ax.xaxis.label.set_color(settings.grid_color)
		self.ecg_ax.tick_params(axis='x', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ecg_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ecg_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)

		self.ppg_ax.xaxis.label.set_color(settings.grid_color)
		self.ppg_ax.tick_params(axis='x', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ppg_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)

		self.ppg_R_ax.xaxis.label.set_color(settings.grid_color)
		self.ppg_R_ax.tick_params(axis='x', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ppg_R_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)

		self.ppg_IR_ax.xaxis.label.set_color(settings.grid_color)
		self.ppg_IR_ax.tick_params(axis='x', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ppg_IR_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		
		#set up viewing window (in this case the 25 most recent values)
		self.repeat_length = 500
		self.repeat_length_split = self.repeat_length

		self.ecg_ax.set_xlim([0,self.repeat_length])
		self.ppg_ax.set_xlim([0,self.repeat_length])
		self.ppg_R_ax.set_xlim([0,self.repeat_length_split])
		self.ppg_IR_ax.set_xlim([0,self.repeat_length_split])

		self.ecg_ax.set_ylim([-1,1])
		self.ppg_ax.set_ylim([-1,1])
		self.ppg_R_ax.set_ylim([-1,1])
		self.ppg_IR_ax.set_ylim([-1,1])

		self.ecg_im, = self.ecg_ax.plot([], [], color=(0,0,1))
		self.ppg_im, = self.ppg_ax.plot([], [], color=(1,0,1))
		self.ppg_R_im, = self.ppg_R_ax.plot([], [], color=(1,1,0))
		self.ppg_IR_im, = self.ppg_IR_ax.plot([], [], color=(1,1,1))

		self.n = 0

		self.ecg_max = 1 #initializes max/min for y-axes to scale with data
		self.ecg_min = -1
		self.ppg_max = 1
		self.ppg_min = -1	
		self.ppg_R_max = 1
		self.ppg_R_min = -1	
		self.ppg_IR_max = 1
		self.ppg_IR_min = -1	

		self.ecg_start_graph_index = 0
		self.ppg_start_graph_index = 0
		self.ppg_R_start_graph_index = 0
		self.ppg_IR_start_graph_index = 0	

		self.ecg_background = self.ecg_fig.canvas.copy_from_bbox(self.ecg_ax.bbox)
		self.ppg_background = self.ppg_fig.canvas.copy_from_bbox(self.ppg_ax.bbox)
		self.ppg_R_background = self.ppg_R_fig.canvas.copy_from_bbox(self.ppg_R_ax.bbox)
		self.ppg_IR_background = self.ppg_IR_fig.canvas.copy_from_bbox(self.ppg_IR_ax.bbox)

		self.ecg_disconnect = self.ecg_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ecg_ax.transAxes, color=settings.graph_color)

		self.ppg_disconnect = self.ppg_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ppg_ax.transAxes, color=settings.graph_color)
		
		self.ppg_R_disconnect = self.ppg_R_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ppg_R_ax.transAxes, color=settings.graph_color)

		self.ppg_IR_disconnect = self.ppg_IR_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ppg_IR_ax.transAxes, color=settings.graph_color)
		#defines internal layout of menubar
	def menu_layout(self):
		self.root.iconbitmap(default=settings.ICON_PATH)

		#holds all widgets in menubar
		self.menu_frame = tk.Frame(self.root, bg = settings.back_color, 
			highlightbackground = settings.grid_color)
		self.menu_frame.grid(row = 0, column = 0, columnspan = 2)
		
		#instantiates buttons for main menubar
		self.file_button = tk.Menubutton(self.menu_frame, text="FILE", 
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color)
		self.view_button = tk.Menubutton(self.menu_frame, text="VIEW",
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color) 
		self.tools_button = tk.Menubutton(self.menu_frame, text="TOOLS", 
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color) 
		self.help_button = tk.Menubutton(self.menu_frame, text="HELP", 
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color) 
		self.spacer_menu = tk.Label(self.menu_frame, text=settings.spacer_text, 
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color) 
				
		self.file_button.grid(row = 0, column = 0)
		self.view_button.grid(row = 0, column = 1)
		self.tools_button.grid(row = 0, column = 2)
		self.help_button.grid(row = 0, column = 3)
		self.spacer_menu.grid(row = 0, column = 4, sticky  = 'W' + 'E' + 'N' + 'S')

		self.menu_frame.columnconfigure(0, weight = 0) 
		self.menu_frame.columnconfigure(1, weight = 0)
		self.menu_frame.columnconfigure(2, weight = 0)
		self.menu_frame.columnconfigure(3, weight = 0)
		self.menu_frame.columnconfigure(4, weight = 1)

		self.file_button.menu= tk.Menu(self.file_button, tearoff = 0,
		 background = settings.back_color, fg= settings.font_color, font = self.vitals_menubar_font)
		self.file_button['menu'] = self.file_button.menu
		self.file_button.menu.add_command(label="Connect HeartBox", command=self.connect_heartbox)
		self.file_button.menu.add_command(label="Disconnect HeartBox", command= self.disconnect_heartbox)
		self.file_button.menu.add_separator()
		self.file_button.menu.add_command(label="Connect Android Bluetooth", command=self.connect_bt_android)
		self.file_button.menu.add_command(label="Disconnect Android Bluetooth", command=self.disconnect_bt_android)
		self.file_button.menu.add_separator()
		self.file_button.menu.add_command(label="Option 3")
		self.file_button.menu.add_command(label="Option 4")
		self.file_button.menu.add_separator()
		self.file_button.menu.add_command(label="Exit")

		self.view_button.menu= tk.Menu(self.view_button, tearoff = 0, 
			background = settings.back_color, fg= settings.font_color, font =self.vitals_menubar_font)
		self.view_button['menu'] = self.view_button.menu
		self.view_button.menu.add_command(label="Option 1")
		self.view_button.menu.add_command(label="Option 2")
		self.view_button.menu.add_separator()
		self.view_button.menu.add_command(label="Option 3")
		self.view_button.menu.add_separator()
		self.view_button.menu.add_command(label="Option 4")
		self.view_button.menu.add_command(label="Option 5")
		self.view_button.menu.add_command(label="Option 6")
		self.view_button.menu.add_separator()
		self.view_button.menu.add_command(label="Option 7")

		self.tools_button.menu= tk.Menu(self.tools_button, tearoff = 0,
		 background = settings.back_color, fg= settings.font_color, font = self.vitals_menubar_font)
		self.tools_button['menu'] = self.tools_button.menu
		self.tools_button.menu.add_command(label="Set a register", command=self.config_register_window)
		self.tools_button.menu.add_command(label="Open high-level register config", command=self.create_ppg_highlevel)
		self.tools_button.menu.add_separator()
		self.tools_button.menu.add_command(label="Option 3")
		self.tools_button.menu.add_separator()
		self.tools_button.menu.add_command(label="Option 4")
		self.tools_button.menu.add_command(label="Option 5")
		self.tools_button.menu.add_command(label="Option 6")
		self.tools_button.menu.add_separator()
		self.tools_button.menu.add_command(label="Option 7")

		self.help_button.menu= tk.Menu(self.help_button, tearoff = 0, 
			background = settings.back_color, fg= settings.font_color, font = self.vitals_menubar_font)
		self.help_button['menu'] = self.help_button.menu
		self.help_button.menu.add_command(label="Open ADPD Documentation", command=self.open_adpd103_docs)
		self.help_button.menu.add_command(label="Option 2")
		self.help_button.menu.add_separator()
		self.help_button.menu.add_command(label="Option 3")
		self.help_button.menu.add_separator()
		self.help_button.menu.add_command(label="Option 4")
		self.help_button.menu.add_command(label="Option 5")
		self.help_button.menu.add_command(label="Option 6")
		self.help_button.menu.add_separator()
		self.help_button.menu.add_command(label="Option 7")

	#defines internal layout of graph 
	def graph_layout(self):
		self.all_graph_frame = tk.Frame(self.root, bg = settings.back_color)
		self.all_graph_frame.grid(column = 0, row = 1, sticky = 'E' + 'W' + 'N' + 'S')
		self.all_graph_frame.columnconfigure(0, weight = 1)
		self.all_graph_frame.rowconfigure(0, weight = 1)
		self.all_graph_frame.rowconfigure(1, weight = 1)
		self.all_graph_frame.rowconfigure(2, weight = 1)
		self.all_graph_frame.rowconfigure(3, weight = 0)

		self.ecg_graph_frame = tk.LabelFrame(self.all_graph_frame, bd = 1, text = "ECG",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ecg_graph_frame.grid(column = 0, row = 0, sticky = 'E' + 'W' + 'N' + 'S')
		self.ecg_graph_frame.columnconfigure(0, weight = 1)
		self.ecg_graph_frame.rowconfigure(0, weight = 1)

		self.ppg_graph_frame = tk.LabelFrame(self.all_graph_frame, bd = 1, text = "PPG",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ppg_graph_frame.grid(column = 0, row = 1, sticky = 'E' + 'W' + 'N' + 'S')
		self.ppg_graph_frame.columnconfigure(0, weight = 1)
		self.ppg_graph_frame.rowconfigure(0, weight = 1)

		self.ppg_R_IR_graph_frame = tk.Frame(self.all_graph_frame, bg = settings.back_color)
		self.ppg_R_IR_graph_frame.grid(column = 0, row = 2, sticky = 'E' + 'W' + 'N' + 'S')
		self.ppg_R_IR_graph_frame.rowconfigure(0, weight = 1)
		self.ppg_R_IR_graph_frame.columnconfigure(0, weight = 1)		
		self.ppg_R_IR_graph_frame.columnconfigure(1, weight = 1)

		self.ppg_R_graph_frame = tk.LabelFrame(self.ppg_R_IR_graph_frame, bd = 1, text = "PPG_R",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ppg_R_graph_frame.grid(column = 0, row = 0, sticky = 'E' + 'W' + 'N' + 'S')
		self.ppg_R_graph_frame.columnconfigure(0, weight = 1)
		self.ppg_R_graph_frame.rowconfigure(0, weight = 1)

		self.ppg_IR_graph_frame = tk.LabelFrame(self.ppg_R_IR_graph_frame, bd = 1, text = "PPG_IR",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ppg_IR_graph_frame.grid(column = 1, row = 0, sticky = 'E' + 'W' + 'N' + 'S')
		self.ppg_IR_graph_frame.columnconfigure(0, weight = 1)
		self.ppg_IR_graph_frame.rowconfigure(0, weight = 1)
		plt.tight_layout()

		self.ecg_canvas = FigureCanvasTkAgg(self.ecg_fig, master=self.ecg_graph_frame)
		#self.ecg_canvas.show()
		self.ecg_canvas.get_tk_widget().grid(column=0,row=0, sticky = 'E' + 'W' + 'N' + 'S')

		self.ppg_canvas = FigureCanvasTkAgg(self.ppg_fig, master=self.ppg_graph_frame)
		#self.ppg_canvas.show()
		self.ppg_canvas.get_tk_widget().grid(column=0, row=0, sticky = 'E' + 'W' + 'N' + 'S')

		self.ppg_R_canvas = FigureCanvasTkAgg(self.ppg_R_fig, master=self.ppg_R_graph_frame)
		#self.ppg_canvas.show()
		self.ppg_R_canvas.get_tk_widget().grid(column=0, row=0, sticky = 'E' + 'W' + 'N' + 'S')

		self.ppg_IR_canvas = FigureCanvasTkAgg(self.ppg_IR_fig, master=self.ppg_IR_graph_frame)
		#self.ppg_canvas.show()
		self.ppg_IR_canvas.get_tk_widget().grid(column=0, row=0, sticky = 'E' + 'W' + 'N' + 'S')
		
	#defines internal layout of vitals
	def vitals_layout(self):
		self.heartbeat_var = tk.IntVar() # initialize metric variables
		self.SP02_var = tk.StringVar()
		self.temp_var = tk.IntVar()
		self.pulse_transit_var = tk.IntVar()
		self.abnormal_var = tk.StringVar()

		self.SP02_var_min = tk.StringVar()
		self.SP02_var_max = tk.StringVar()

		self.heartbeat_var = np.random.randint(40, 60)
		self.SP02_var = (self.dsp.SP02_value)
		self.temp_var = np.random.randint(98, 102)
		self.pulse_transit_var = np.random.randint(50, 55)
		self.abnormal_var = settings.condition_set[np.random.randint(0, 3)]

		self.heartbeat_var_min = 9999#initialize max/min metric vars
		self.SP02_var_min = 9999
		self.temp_var_min = 9999
		self.ptt_var_min = 9999
		
		self.heartbeat_var_max = self.heartbeat_var
		self.SP02_var_max = self.SP02_var
		self.temp_var_max = self.temp_var
		self.ptt_var_max = self.pulse_transit_var

		self.root.columnconfigure(0, weight = 7) #Used to allow for widgets to scale with window resolution. This is the column with the graph widgets
		self.root.columnconfigure(1, weight = 1)
		self.root.rowconfigure(0, weight = 0)
		self.root.rowconfigure(1, weight = 1) #scales only the graph/vitals widgets, not the menubar

		self.text_monitor_frame = tk.LabelFrame(self.root, bd = 1, font = self.vitals_title_font,
			text = "VITALS", padx = 5, fg= settings.font_color, bg = settings.back_color) #frame that contains all vital metrics
		self.text_monitor_frame.grid(column = 1, row = 1, rowspan = 2, padx = 10, sticky = 'N' + 'W' + 'S' + 'E')
		self.text_monitor_frame.columnconfigure(0, weight = 1)
		self.text_monitor_frame.rowconfigure(0, weight = 1) #equal scaling of all vital metrics with res
		self.text_monitor_frame.rowconfigure(1, weight = 1)
		self.text_monitor_frame.rowconfigure(2, weight = 1)
		self.text_monitor_frame.rowconfigure(3, weight = 1)
		self.text_monitor_frame.rowconfigure(4, weight = 1)

		self.heartbeat_frame = tk.Frame(self.text_monitor_frame, bd = 0.5, 
			relief="groove", bg = settings.back_color)
		self.SP02_frame = tk.Frame(self.text_monitor_frame, bd = 0.5, 
			relief="groove", bg = settings.back_color)
		self.temp_frame = tk.Frame(self.text_monitor_frame, bd = 0.5,
		 relief="groove", bg = settings.back_color)
		self.pulse_transit_frame = tk.Frame(self.text_monitor_frame, bd = 0.5,
		 relief="groove", bg = settings.back_color)
		self.abnormal_frame = tk.Frame(self.text_monitor_frame, bd = 0.5,
		 relief="groove", bg = settings.back_color)

		self.heartbeat_frame.grid(row = 0, column = 0, sticky = 'N' + 'W' + 'S' + 'E')
		self.SP02_frame.grid(row = 1, column = 0, sticky = 'N' + 'W' + 'S' + 'E')
		self.temp_frame.grid(row = 2, column = 0, sticky = 'N' + 'W' + 'S' + 'E')
		self.pulse_transit_frame.grid(row = 3, column = 0, sticky = 'N' + 'W' + 'S' + 'E')
		self.abnormal_frame.grid(row = 4, column = 0, sticky = 'N' + 'W' + 'S' + 'E')

		self.heartbeat_frame.columnconfigure(0, weight = 2)
		self.heartbeat_frame.columnconfigure(2, weight = 2)
		self.heartbeat_frame.rowconfigure(1, weight = 1)

		self.SP02_frame.columnconfigure(0, weight = 2)
		self.SP02_frame.columnconfigure(2, weight = 2)
		self.SP02_frame.rowconfigure(1, weight = 1)

		self.temp_frame.columnconfigure(0, weight = 2)
		self.temp_frame.columnconfigure(2, weight = 2)
		self.temp_frame.rowconfigure(1, weight = 1)

		self.pulse_transit_frame.columnconfigure(0, weight = 2)
		self.pulse_transit_frame.columnconfigure(2, weight = 2)
		self.pulse_transit_frame.rowconfigure(1, weight = 1)

		self.abnormal_frame.columnconfigure(0, weight = 0)
		self.abnormal_frame.columnconfigure(1, weight = 2)
		self.abnormal_frame.rowconfigure(1, weight = 1)

		self.heartbeat_text = tk.Label(self.heartbeat_frame, text = "ECG HR", font = 
			self.vitals_subtitle_font, anchor = "w", fg=settings.font_color, bg = settings.back_color)
		self.SP02_text = tk.Label(self.SP02_frame, text = "SPO2 (%)", font = self.vitals_subtitle_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.temp_text = tk.Label(self.temp_frame, text = "TEMP (" + settings.deg + "F)", 
			font = self.vitals_subtitle_font, anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.pulse_transit_text = tk.Label(self.pulse_transit_frame, text = "PULSE TT (MS)", 
			font = self.vitals_subtitle_font, anchor ="w",  fg=settings.font_color, bg = settings.back_color)
		self.abnormal_text = tk.Label(self.abnormal_frame, text = "ABNORMAL HB", 
			font = self.vitals_subtitle_font, anchor ="w", fg=settings.font_color, bg = settings.back_color)

		self.heartbeat_label = tk.Label(self.heartbeat_frame, text = '--', font = self.vitals_text_font,
			fg=settings.font_color, bg = settings.back_color)
		self.SP02_label = tk.Label(self.SP02_frame, text = '--', font = self.vitals_text_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.temp_label = tk.Label(self.temp_frame, text = '--', font = self.vitals_text_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.pulse_transit_label = tk.Label(self.pulse_transit_frame, text = '--', 
			font = self.vitals_text_font, anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.abnormal_label = tk.Label(self.abnormal_frame, text = '--', font = self.vitals_text_font,
		    anchor ="w", fg=settings.font_color, bg = settings.back_color)

		self.frame_heartbeat_min_max = tk.Frame(self.heartbeat_frame)
		self.frame_SP02_min_max = tk.Frame(self.SP02_frame)
		self.frame_temp_min_max= tk.Frame(self.temp_frame)
		self.frame_ptt_min_max= tk.Frame(self.pulse_transit_frame)

		self.heartbeat_text.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
		self.SP02_text.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
		self.temp_text.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
		self.pulse_transit_text.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
		self.abnormal_text.grid(row = 0, column = 0, columnspan = 3, sticky = "W")

		self.heartbeat_label.grid(row = 1, column = 0, columnspan = 2)
		self.SP02_label.grid(row = 1, column = 0, columnspan = 2)
		self.temp_label.grid(row = 1, column = 0, columnspan = 2)
		self.pulse_transit_label.grid(row = 1, column = 0, columnspan = 2)
		self.abnormal_label.grid(row = 1, column = 0, columnspan = 2)

		self.frame_heartbeat_min_max.grid(row = 1, column = 2)
		self.frame_SP02_min_max.grid(row = 1, column = 2)
		self.frame_temp_min_max.grid(row = 1, column = 2)
		self.frame_ptt_min_max.grid(row = 1, column = 2)

		self.heartbeat_min_label = tk.Label(self.frame_heartbeat_min_max, text = "MIN:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.heartbeat_max_label = tk.Label(self.frame_heartbeat_min_max, text = "MAX:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.SP02_min_label = tk.Label(self.frame_SP02_min_max, text = "MIN:",
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.SP02_max_label = tk.Label(self.frame_SP02_min_max, text = "MAX:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.temp_min_label = tk.Label(self.frame_temp_min_max, text = "MIN:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.temp_max_label = tk.Label(self.frame_temp_min_max, text = "MAX:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.ptt_min_label = tk.Label(self.frame_ptt_min_max, text = "MIN:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.ptt_max_label = tk.Label(self.frame_ptt_min_max, text = "MAX:", 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.heartbeat_min_label.grid(row = 0, column = 0, sticky = "W")
		self.heartbeat_max_label.grid(row = 1, column = 0, sticky = "W")

		self.SP02_min_label.grid(row = 0, column = 0, sticky = "W")
		self.SP02_max_label.grid(row = 1, column = 0, sticky = "W")

		self.temp_min_label.grid(row = 0, column = 0, sticky = "W")
		self.temp_max_label.grid(row = 1, column = 0, sticky = "W")

		self.ptt_min_label.grid(row = 0, column = 0, sticky = "W")
		self.ptt_max_label.grid(row = 1, column = 0, sticky = "W")

		self.heartbeat_min_value = tk.Label(self.frame_heartbeat_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.heartbeat_max_value = tk.Label(self.frame_heartbeat_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.SP02_min_value = tk.Label(self.frame_SP02_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.SP02_max_value= tk.Label(self.frame_SP02_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.temp_min_value= tk.Label(self.frame_temp_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.temp_max_value = tk.Label(self.frame_temp_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.ptt_min_value = tk.Label(self.frame_ptt_min_max, text = '--', font = 
			self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)
		self.ptt_max_value = tk.Label(self.frame_ptt_min_max, text = '--', 
			font = self.vitals_subtext_font, fg=settings.font_color, bg = settings.back_color)

		self.heartbeat_min_value.grid(row = 0, column = 1)
		self.heartbeat_max_value.grid(row = 1, column = 1)

		self.SP02_min_value.grid(row = 0, column = 1)
		self.SP02_max_value.grid(row = 1, column = 1)

		self.temp_min_value.grid(row = 0, column = 1)
		self.temp_max_value.grid(row = 1, column = 1)

		self.ptt_min_value.grid(row = 0, column = 1)
		self.ptt_max_value.grid(row = 1, column = 1)
	#defines absolute layout of all top level widgets
	#def viewer_layout(self):

	#graph renderer for recorded data
	def read_recorded_samples(self):
		self.n = self.n + 1
		self.update_viewer()
		self.root.after(0, self.read_recorded_samples)

	def update_viewer(self):
		#uses stored data for waveforms
		#pdb.set_trace()
		self.ecg_im.set_xdata(np.arange(self.ecg_start_graph_index, self.n))
		self.ecg_im.set_ydata(self.ecg_data[self.ecg_start_graph_index: self.n])
		self.ppg_im.set_xdata(np.arange(self.ecg_start_graph_index, self.n))
		self.ppg_im.set_ydata(self.ppg_data[self.ppg_start_graph_index: self.n])
		self.ppg_R_im.set_xdata(np.arange(self.ppg_R_start_graph_index, self.n))
		self.ppg_R_im.set_ydata(self.ppg_R_data[self.ppg_R_start_graph_index: self.n])
		self.ppg_IR_im.set_xdata(np.arange(self.ppg_IR_start_graph_index, self.n))
		self.ppg_IR_im.set_ydata(self.ppg_IR_data[self.ppg_IR_start_graph_index: self.n])

		#self.heartbeat_var = np.random.randint(40, 60)
		# self.temp_var = np.random.randint(98, 102)
		# self.pulse_transit_var = np.random.randint(50, 55)
		# self.abnormal_var = condition_set[np.random.randint(0, 3)]

		#self.heartbeat_label.configure(text = self.heartbeat_var)

		if(self.dsp.SP02_valid):
			self.SP02_var = self.dsp.SP02_value
			self.SP02_label.configure(text = self.SP02_var)
			if(self.SP02_var < self.SP02_var_min):
				self.SP02_var_min = self.SP02_var
				self.SP02_min_value.configure(text = self.SP02_var_min)
			if(self.SP02_var > self.SP02_var_max):
				self.SP02_var_max = self.SP02_var
				self.SP02_max_value.configure(text = self.SP02_var_max)
		else:
			self.SP02_label.configure(text = '--')
		# self.temp_label.configure(text = self.temp_var)
		# self.pulse_transit_label.configure(text = self.pulse_transit_var)
		# self.abnormal_label.configure(text = self.abnormal_var)

		#in the case where we need to refresh the x axis
		if ((self.n / self.repeat_length ) > self.frame_num):
			self.frame_num = self.n / self.repeat_length
			self.ecg_start_graph_index = self.n
			self.ppg_start_graph_index = self.n 
			self.ppg_R_start_graph_index = self.n
			self.ppg_IR_start_graph_index = self.n

			limX1 = self.ecg_ax.set_xlim(self.n, self.n + self.repeat_length)
			limX2 = self.ppg_ax.set_xlim(self.n, self.n + self.repeat_length)
			limX3 = self.ppg_R_ax.set_xlim(self.n, self.n + self.repeat_length)
			limX4 = self.ppg_IR_ax.set_xlim(self.n, self.n + self.repeat_length)

			self.ecg_max = settings.large_value_neg
			self.ecg_min = settings.large_value
			self.ppg_max = settings.large_value_neg
			self.ppg_min = settings.large_value
			self.ppg_R_max = settings.large_value_neg
			self.ppg_R_min = settings.large_value
			self.ppg_IR_max = settings.large_value_neg
			self.ppg_IR_min = settings.large_value

			if(self.ecg_data[self.n] > self.ecg_max):
				self.ecg_max = self.ecg_data[self.n] + 500
			elif(self.ecg_data[self.n] < self.ecg_min):
				self.ecg_min = self.ecg_data[self.n] - 500
			if(self.ppg_data[self.n] > self.ppg_max):
				self.ppg_max = self.ppg_data[self.n] + 500
			elif(self.ppg_data[self.n] < self.ppg_min):
				self.ppg_min = self.ppg_data[self.n] - 500
			if(self.ppg_R_data[self.n] > self.ppg_R_max):
				self.ppg_R_max = self.ppg_R_data[self.n] + 500
			elif(self.ppg_R_data[self.n] < self.ppg_R_min):
				self.ppg_R_min = self.ppg_R_data[self.n] - 500
			if(self.ppg_IR_data[self.n] > self.ppg_IR_max):
				self.ppg_IR_max = self.ppg_IR_data[self.n] + 500
			elif(self.ppg_IR_data[self.n] < self.ppg_IR_min):
				self.ppg_IR_min = self.ppg_IR_data[self.n] - 500
			limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
			limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])
			limY3 = self.ppg_R_ax.set_ylim([self.ppg_R_min, self.ppg_R_max])
			limY4 = self.ppg_IR_ax.set_ylim([self.ppg_IR_min, self.ppg_IR_max])

			self.ecg_fig.canvas.draw()
			self.ppg_fig.canvas.draw()
			self.ppg_R_fig.canvas.draw()
			self.ppg_IR_fig.canvas.draw()

		#otherwise, we can plot efficiently since we don't need to change the viewing window
		else:
			if(self.ecg_max - self.ecg_min < 10000):
				if(self.ecg_data[self.n] > self.ecg_max):
					self.ecg_max = self.ecg_data[self.n] + 500
					limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
					self.ecg_fig.canvas.draw()

				elif(self.ecg_data[self.n] < self.ecg_min):
					self.ecg_min = self.ecg_data[self.n] - 500
					limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
					self.ecg_fig.canvas.draw()
				else:
					self.ecg_fig.canvas.restore_region(self.ecg_background)
					self.ecg_ax.draw_artist(self.ecg_im)
					self.ecg_fig.canvas.blit(self.ecg_ax.bbox)
			else:
				self.ecg_fig.canvas.restore_region(self.ecg_background)
				self.ecg_ax.draw_artist(self.ecg_im)
				self.ecg_fig.canvas.blit(self.ecg_ax.bbox)

			if(self.ppg_max - self.ppg_min < 10000):
				if(self.ppg_data[self.n] > self.ppg_max):
					self.ppg_max = self.ppg_data[self.n] + 500
					limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])
					self.ppg_fig.canvas.draw()

				elif(self.ppg_data[self.n] < self.ppg_min):
					self.ppg_min = self.ppg_data[self.n] - 500
					limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])
					self.ppg_fig.canvas.draw()
				else:
					self.ppg_fig.canvas.restore_region(self.ppg_background)
					self.ppg_ax.draw_artist(self.ppg_im)
					self.ppg_fig.canvas.blit(self.ppg_ax.bbox)
			else:
					self.ppg_fig.canvas.restore_region(self.ppg_background)
					self.ppg_ax.draw_artist(self.ppg_im)
					self.ppg_fig.canvas.blit(self.ppg_ax.bbox)

			if(self.ppg_R_max - self.ppg_R_min < 10000):
				if(self.ppg_R_data[self.n] > self.ppg_R_max):
					self.ppg_R_max = self.ppg_R_data[self.n] + 500
					limY2 = self.ppg_R_ax.set_ylim([self.ppg_R_min, self.ppg_R_max])
					self.ppg_R_fig.canvas.draw()

				elif(self.ppg_R_data[self.n] < self.ppg_R_min):
					self.ppg_R_min = self.ppg_R_data[self.n] - 500
					limY2 = self.ppg_R_ax.set_ylim([self.ppg_R_min, self.ppg_R_max])
					self.ppg_R_fig.canvas.draw()
				else:
					self.ppg_R_fig.canvas.restore_region(self.ppg_R_background)
					self.ppg_R_ax.draw_artist(self.ppg_R_im)
					self.ppg_R_fig.canvas.blit(self.ppg_R_ax.bbox)
			else:
					self.ppg_R_fig.canvas.restore_region(self.ppg_R_background)
					self.ppg_R_ax.draw_artist(self.ppg_R_im)
					self.ppg_R_fig.canvas.blit(self.ppg_R_ax.bbox)
			
			if(self.ppg_IR_max - self.ppg_IR_min < 10000):
				if(self.ppg_IR_data[self.n] > self.ppg_IR_max):
					self.ppg_IR_max = self.ppg_IR_data[self.n] + 500
					limY2 = self.ppg_IR_ax.set_ylim([self.ppg_IR_min, self.ppg_IR_max])
					self.ppg_IR_fig.canvas.draw()

				elif(self.ppg_IR_data[self.n] < self.ppg_IR_min):
					self.ppg_IR_min = self.ppg_IR_data[self.n] - 500
					limY2 = self.ppg_IR_ax.set_ylim([self.ppg_IR_min, self.ppg_IR_max])
					self.ppg_IR_fig.canvas.draw()
				else:
					self.ppg_IR_fig.canvas.restore_region(self.ppg_IR_background)
					self.ppg_IR_ax.draw_artist(self.ppg_IR_im)
					self.ppg_IR_fig.canvas.blit(self.ppg_IR_ax.bbox)
			else:
					self.ppg_IR_fig.canvas.restore_region(self.ppg_IR_background)
					self.ppg_IR_ax.draw_artist(self.ppg_IR_im)
					self.ppg_IR_fig.canvas.blit(self.ppg_IR_ax.bbox)


	#graph renderer for live data
	def read_live_samples(self):
		#while(~q.empty()):
		if(self.heartbox_connect_state):
			#pdb.set_trace()
			filtered_data = self.dsp.filt_data_gen()
			if(filtered_data != 'Q' and filtered_data != 'B'):
				filtered_ppg = filtered_data[0,:]
				filtered_ecg = filtered_data[1,:]
				filtered_ppg_R = filtered_data[2,:]
				filtered_ppg_IR = filtered_data[3,:]

				if(self.android_connect_state):
					heartbox_comm.heartbox_bt_send(pack('ff', filtered_ecg, filtered_ppg))

				self.heartbox_var = self.dsp.calc_heartrate()

				self.ppg_data = np.append(self.ppg_data, filtered_ppg)
				self.ecg_data = np.append(self.ecg_data, filtered_ecg)
				self.ppg_R_data = np.append(self.ppg_R_data, filtered_ppg_R)
				self.ppg_IR_data = np.append(self.ppg_IR_data, filtered_ppg_IR)
				#print self.ppg_data[self.n]
				self.n = self.n + filtered_ecg.size - 1
				self.update_viewer()
				self.root.after(0, self.read_live_samples)
				self.n = self.n + 1
			elif (filtered_data == 'Q' or filtered_data == 'B'):
				#print 'R'
				self.root.after(0, self.read_live_samples)
		else:
			self.ppg_disconnect.set_text('---- DISCONNECTED ----')
			time.sleep(1)
			self.ppg_disconnect.set_text('')

	def bind_shortcuts(self):
		self.root.bind("<F11>", self.toggle_fullscreen)
		self.root.bind("<Escape>", self.end_fullscreen)

	def toggle_fullscreen(self, event=None):
		self.fullscreen_state = not self.fullscreen_state  # Just toggling the boolean
		self.root.attributes("-fullscreen", self.fullscreen_state)

		if(not self.fullscreen_state):
			ecg_width = self.ecg_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width) 
			ecg_height = self.ecg_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)
			ppg_width = self.ppg_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width)
			ppg_height = self.ppg_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)
			ppg_R_width = self.ppg_R_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width)
			ppg_R_height = self.ppg_R_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)
			ppg_IR_width = self.ppg_IR_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width)
			ppg_IR_height = self.ppg_IR_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)

			self.vitals_title_font.configure(size = self.vitals_title_font_size)
			self.vitals_subtitle_font.configure(size = self.vitals_subtitle_font_size)
			self.vitals_menubar_font.configure(size = self.vitals_menubar_font_size)
			self.vitals_text_font.configure(size = self.vitals_text_font_size)
			self.vitals_subtext_font.configure(size = self.vitals_subtext_font_size)

			self.ecg_disconnect.set_size(20)
			self.ppg_disconnect.set_size(20)
			self.ppg_R_disconnect.set_size(20)
			self.ppg_IR_disconnect.set_size(20)

		else:
			ecg_width = float(self.ecg_fig.get_size_inches()[0]) * float(self.screen_width) / float(self.min_screen_width)
			ecg_height = float(self.ecg_fig.get_size_inches()[1]) * float(self.screen_height) /  float(self.min_screen_height)
			ppg_width = float(self.ppg_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_height = float(self.ppg_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			ppg_R_width = float(self.ppg_R_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_R_height = float(self.ppg_R_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			ppg_IR_width = float(self.ppg_R_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_IR_height = float(self.ppg_R_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)

			new_to_old_ratio = float(self.screen_width) / float(self.min_screen_width)

			self.ecg_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_R_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_IR_disconnect.set_size(20*new_to_old_ratio)

			self.vitals_title_font.configure(size = int(self.vitals_title_font_size * new_to_old_ratio))
			self.vitals_subtitle_font.configure(size = int(self.vitals_subtitle_font_size * new_to_old_ratio))
			self.vitals_menubar_font.configure(size = int(self.vitals_menubar_font_size * new_to_old_ratio))
			self.vitals_text_font.configure(size = int(self.vitals_text_font_size * new_to_old_ratio))
			self.vitals_subtext_font.configure(size = int(self.vitals_subtext_font_size * new_to_old_ratio))

		self.ecg_fig.set_size_inches(ecg_width, ecg_height)
		self.ppg_fig.set_size_inches(ppg_width, ppg_height)
		self.ppg_R_fig.set_size_inches(ppg_R_width, ppg_R_height)
		self.ppg_IR_fig.set_size_inches(ppg_IR_width, ppg_IR_height)

		self.ecg_fig.canvas.draw()
		self.ppg_fig.canvas.draw()
		self.ppg_R_fig.canvas.draw()
		self.ppg_IR_fig.canvas.draw()

		return "break"

	def end_fullscreen(self, event=None):
		if(self.fullscreen_state == True):
			self.fullscreen_state = False
			self.root.attributes("-fullscreen", False)

			ecg_width = float(self.ecg_fig.get_size_inches()[0]) * float(self.screen_width) / float(self.min_screen_width)
			ecg_height = float(self.ecg_fig.get_size_inches()[1]) * float(self.screen_height) /  float(self.min_screen_height)
			ppg_width = float(self.ppg_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_height = float(self.ppg_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			ppg_R_width = float(self.ppg_R_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_R_height = float(self.ppg_R_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			ppg_IR_width = float(self.ppg_R_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_IR_height = float(self.ppg_R_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			new_to_old_ratio = float(self.screen_width) / float(self.min_screen_width)

			self.ecg_fig.set_size_inches(ecg_width, ecg_height)
			self.ppg_fig.set_size_inches(ppg_width, ppg_height)
			self.ppg_R_fig.set_size_inches(ppg_R_width, ppg_R_height)
			self.ppg_IR_fig.set_size_inches(ppg_IR_width, ppg_IR_height)

			self.vitals_title_font.configure(size = int(self.vitals_title_font_size * new_to_old_ratio))
			self.vitals_subtitle_font.configure(size = int(self.vitals_subtitle_font_size * new_to_old_ratio))
			self.vitals_menubar_font.configure(size = int(self.vitals_menubar_font_size * new_to_old_ratio))
			self.vitals_text_font.configure(size = int(self.vitals_text_font_size * new_to_old_ratio))
			self.vitals_subtext_font.configure(size = int(self.vitals_subtext_font_size * new_to_old_ratio))

			self.ecg_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_R_disconnect.set_size(20*new_to_old_ratio)
			self.ppg_IR_disconnect.set_size(20*new_to_old_ratio)

			self.ecg_fig.canvas.draw()
			self.ppg_fig.canvas.draw()
			self.ppg_R_fig.canvas.draw()
			self.ppg_IR_fig.canvas.draw()

		return "break"

	def connect_heartbox(self):
		self.heartbox_connect_state = True
		if(self.ecg_disconnect_state):
			self.toggle_ecg_disconnect()
			self.toggle_ppg_disconnect()
			self.toggle_ppg_R_disconnect()
			self.toggle_ppg_IR_disconnect()
		self.startup()

	def disconnect_heartbox(self):
		self.heartbox_connect_state = False
		if(not self.ecg_disconnect_state):
			self.toggle_ecg_disconnect()
			self.toggle_ppg_disconnect()
			self.toggle_ppg_R_disconnect()
			self.toggle_ppg_IR_disconnect()
		if(not self.android_connect_state):
			self.disconnect_bt_android()

	def toggle_ecg_disconnect(self):
		if(not self.ecg_disconnect_state):
			self.ecg_disconnect.set_text('---- DISCONNECTED ----')
			self.ecg_disconnect_state = True

		else:
			self.ecg_disconnect.set_text('')
			self.ecg_disconnect_state = False

		self.ecg_fig.canvas.draw()

	def toggle_ppg_disconnect(self):
		if(not self.ppg_disconnect_state):
			self.ppg_disconnect.set_text('---- DISCONNECTED ----')
			self.ppg_disconnect_state = True
		else:
			self.ppg_disconnect.set_text('')
			self.ppg_disconnect_state = False

		self.ppg_fig.canvas.draw()

	def toggle_ppg_R_disconnect(self):
		if(not self.ppg_R_disconnect_state):
			self.ppg_R_disconnect.set_text('---- DISCONNECTED ----')
			self.ppg_R_disconnect_state = True
		else:
			self.ppg_R_disconnect.set_text('')
			self.ppg_R_disconnect_state = False

		self.ppg_R_fig.canvas.draw()

	def toggle_ppg_IR_disconnect(self):
		if(not self.ppg_IR_disconnect_state):
			self.ppg_IR_disconnect.set_text('---- DISCONNECTED ----')
			self.ppg_IR_disconnect_state = True
		else:
			self.ppg_IR_disconnect.set_text('')
			self.ppg_IR_disconnect_state = False

		self.ppg_IR_fig.canvas.draw()

	def connect_bt_android(self):
		self.android_connect_state = True
		if(self.android_connect_state):
			heartbox_comm.heartbox_bt_connect()

	def disconnect_bt_android(self):
		self.android_connect_state= False
		if(not self.android_connect_state):
			heartbox_comm.heartbox_bt_disconnect()

	def config_register_window(self):
		popup_register = tk.Toplevel()
		self.result = tk.StringVar()
		popup_register.configure(bg = settings.back_color)
		popup_register.attributes("-toolwindow", 1) 

		register_field_label = tk.Label(popup_register, text="Enter a Register Setting",
		  font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color)
		self.register_field = tk.Entry(popup_register, textvariable = self.result, 
			font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color)
		register_field_button = tk.Button(popup_register, text = "Enter", font = self.vitals_menubar_font,
		 command = self.send_register_changes, fg= settings.font_color, bg = settings.back_color)

		register_field_label.grid(row = 0, column = 0)
		self.register_field.grid(row = 0, column = 1)
		register_field_button.grid(row = 0, column = 2)

	def send_register_changes(self):
		self.register_field.get()

		if(self.heartbox_connect_state):
			heartbox_comm.heartbox_uart_conf_reg(self.result)
		else:
			popup_error = tk.Toplevel()
			popup_error.configure(bg = settings.back_color)
			popup_error.attributes("-toolwindow", 1) 
			error_label = tk.Label(popup_error, text="ERROR: Connect to HeartBox",
				font = self.vitals_menubar_font, fg= settings.font_color, bg = settings.back_color)
			error_label.grid(row = 0, column = 0)

	def open_adpd103_docs(self):
		subprocess.Popen(['ADPD105-106-107.pdf'],shell=True)

	def create_ppg_highlevel(self):
		ppg_highlevel()

if __name__ == "__main__":
	graph_viewer = heartbox_wave_viewer()
