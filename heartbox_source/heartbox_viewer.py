import Tkinter as tk 
from PIL import Image, ImageTk
import tkFont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib

import numpy as np
from scipy import signal
import pdb

import multiprocessing
import socket
import time

import settings
from heartbox_dsp import heartbox_dsp
import heartbox_comm
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

		self.vitals_title_font = tkFont.Font(family = 'Consolas', size = 15)
		self.vitals_subtitle_font = tkFont.Font(family = 'Consolas', size = 15)
		self.vitals_menubar_font = tkFont.Font(family = 'Consolas', size = 10)
		self.vitals_text_font = tkFont.Font(family = 'Consolas', size = 55)
		self.vitals_subtext_font = tkFont.Font(family = 'Consolas', size = 10)

		self.setup_plots()
		self.bind_shortcuts()
		self.menu_layout()
		self.graph_layout()
		self.vitals_layout()

		#heartbox_comm.heartbox_bt_send('HELLO')

	def startup(self):
		#for offline viewing, reads data from csv
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
		else:
			self.ecg_data = np.genfromtxt('ecg.csv', delimiter = ',')
			self.ppg_data = np.genfromtxt('ppg.csv', delimiter = ',')
		
		#setup figure
		self.ecg_fig = plt.figure()
		self.ppg_fig = plt.figure()
		self.ecg_fig.set_size_inches(8,3.5)
		self.ppg_fig.set_size_inches(8,3.5)
		self.ecg_ax = self.ecg_fig.add_subplot(1,1,1)
		self.ppg_ax = self.ppg_fig.add_subplot(1,1,1)
		self.ecg_ax.locator_params(axis='y', nbins =2)
		self.ecg_ax.locator_params(axis='x', nbins =2)
		self.ppg_ax.locator_params(axis='y', nbins =2)
		self.ppg_ax.locator_params(axis='x', nbins =2)

		self.ecg_fig.set_facecolor(settings.back_color)
		self.ppg_fig.set_facecolor(settings.back_color)
		#self.ecg_ax.set_frame_on(False)
		#self.ppg_ax.set_frame_on(False)

		self.ecg_ax.set_facecolor(settings.back_color)
		self.ppg_ax.set_facecolor(settings.back_color)

		self.ecg_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)
		self.ppg_ax.grid(color = settings.grid_color, linestyle='--', linewidth = 0.25)


		self.ecg_ax.xaxis.label.set_color(settings.grid_color)
		self.ecg_ax.tick_params(axis='x', colors=settings.grid_color, width  = 0.5, labelsize = 8)
		self.ecg_ax.tick_params(axis='y', colors=settings.grid_color, width  = 0.5, labelsize = 8)


		self.ppg_ax.xaxis.label.set_color(settings.grid_color)
		self.ppg_ax.tick_params(axis='x', colors=settings.grid_color)
		self.ppg_ax.tick_params(axis='y', colors=settings.grid_color)

		#set up viewing window (in this case the 25 most recent values)
		#self.repeat_length = (np.shape(self.ecg_data)[0]+1)/10
		self.repeat_length = 500
		self.ecg_ax.set_xlim([0,self.repeat_length])
		self.ppg_ax.set_xlim([0,self.repeat_length])

		self.ecg_ax.set_ylim([-1,1])
		self.ppg_ax.set_ylim([-1,1])

		self.ecg_im, = self.ecg_ax.plot([], [], color=(0,0,1))
		self.ppg_im, = self.ppg_ax.plot([], [], color=(1,0,1))

		self.n = 0
		self.ppg_max = 1
		self.ppg_min = -1
		self.ecg_max = 1
		self.ecg_min = -1
		self.ppg_start_graph_index = 0
		self.ecg_start_graph_index = 0

		self.ecg_background = self.ecg_fig.canvas.copy_from_bbox(self.ecg_ax.bbox)
		self.ppg_background = self.ppg_fig.canvas.copy_from_bbox(self.ppg_ax.bbox)
		
		self.ecg_disconnect = self.ecg_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ecg_ax.transAxes, color=settings.graph_color)

		self.ppg_disconnect = self.ppg_ax.text(0.5, 0.5,'---- DISCONNECTED ----', size=20, 
			ha = 'center', va = 'center', transform=self.ecg_ax.transAxes, color=settings.graph_color)
		

		#defines internal layout of menubar
	def menu_layout(self):
		self.root.iconbitmap(default=settings.ICON_PATH)

		#holds all widgets in menubar
		self.menu_frame = tk.Frame(self.root, bg = settings.back_color, highlightbackground = settings.grid_color)
		self.menu_frame.grid(row = 0, column = 0, columnspan = 2)
		
		#instantiates buttons for main menubar
		self.file_button = tk.Menubutton(self.menu_frame, text="FILE", font = self.vitals_menubar_font,
			fg= settings.font_color, bg = settings.back_color)
		self.view_button = tk.Menubutton(self.menu_frame, text="VIEW", font = self.vitals_menubar_font,
			fg= settings.font_color, bg = settings.back_color) 
		self.tools_button = tk.Menubutton(self.menu_frame, text="TOOLS", font = self.vitals_menubar_font,
			fg= settings.font_color, bg = settings.back_color) 
		self.help_button = tk.Menubutton(self.menu_frame, text="HELP", font = self.vitals_menubar_font,
			fg= settings.font_color, bg = settings.back_color) 
		self.spacer_menu = tk.Label(self.menu_frame, text=settings.spacer_text, font = self.vitals_menubar_font,
			fg= settings.font_color, bg = settings.back_color) 
				
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
		self.file_button.menu.add_command(label="Option 1")
		self.file_button.menu.add_separator()
		self.file_button.menu.add_command(label="Option 2")
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
		self.tools_button.menu.add_command(label="Option 1")
		self.tools_button.menu.add_command(label="Option 2")
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
		self.help_button.menu.add_command(label="Option 1")
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
		self.all_graph_frame.rowconfigure(2, weight = 0)

		self.ecg_graph_frame = tk.LabelFrame(self.all_graph_frame, bd = 1, text = "ECG",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ecg_graph_frame.grid(column = 0, row = 0, sticky = 'E' + 'W' + 'N' + 'S')
		self.ecg_graph_frame.columnconfigure(0, weight = 1)
		self.all_graph_frame.rowconfigure(0, weight = 1)

		self.ecg_canvas = FigureCanvasTkAgg(self.ecg_fig, master=self.ecg_graph_frame)
		#self.ecg_canvas.show()
		self.ecg_canvas.get_tk_widget().grid(column=0,row=0, sticky = 'E' + 'W' + 'N' + 'S')

		self.ppg_graph_frame = tk.LabelFrame(self.all_graph_frame, bd = 1, text = "PPG",
			fg=settings.font_color, bg = settings.back_color, font = self.vitals_title_font)
		self.ppg_graph_frame.grid(column = 0, row = 1, sticky = 'E' + 'W' + 'N' + 'S')
		self.ppg_graph_frame.columnconfigure(0, weight = 1)
		self.ppg_graph_frame.rowconfigure(0, weight = 1)

		self.ppg_canvas = FigureCanvasTkAgg(self.ppg_fig, master=self.ppg_graph_frame)
		#self.ppg_canvas.show()
		self.ppg_canvas.get_tk_widget().grid(column=0,row=0,sticky = 'E' + 'W' + 'N' + 'S')
		
	#defines internal layout of vitals
	def vitals_layout(self):
		self.heartbeat_var = tk.StringVar()
		self.SP02_var = tk.StringVar()
		self.temp_var = tk.StringVar()
		self.pulse_transit_var = tk.StringVar()
		self.abnormal_var = tk.StringVar()

		self.heartbeat_var = str(np.random.randint(40, 60))
		self.SP02_var = str(np.random.randint(20, 30))
		self.temp_var = str(np.random.randint(98, 102))
		self.pulse_transit_var = str(np.random.randint(50, 55))
		self.abnormal_var = settings.condition_set[np.random.randint(0, 3)]

		self.heartbeat_var_min = self.heartbeat_var
		self.SP02_var_min = self.SP02_var
		self.temp_var_min = self.temp_var
		self.ptt_var_min = self.pulse_transit_var
		
		self.heartbeat_var_max = self.heartbeat_var
		self.SP02_var_max = self.SP02_var
		self.temp_var_max = self.temp_var
		self.ptt_var_max = self.pulse_transit_var

		self.root.columnconfigure(0, weight = 7)
		self.root.columnconfigure(1, weight = 3)
		self.root.rowconfigure(0, weight = 0)
		self.root.rowconfigure(1, weight = 1)

		self.text_monitor_frame = tk.LabelFrame(self.root, bd = 1, font = self.vitals_title_font,
			text = "VITALS", padx = 5, fg= settings.font_color, bg = settings.back_color)
		self.text_monitor_frame.grid(column = 1, row = 1, rowspan = 2, padx = 10, sticky = 'N' + 'W' + 'S' + 'E')
		self.text_monitor_frame.columnconfigure(0, weight = 1)
		self.text_monitor_frame.columnconfigure(1, weight = 0)
		self.text_monitor_frame.rowconfigure(0, weight = 1)
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

		self.SP02_frame.columnconfigure(0, weight = 2)
		self.SP02_frame.columnconfigure(2, weight = 2)

		self.temp_frame.columnconfigure(0, weight = 2)
		self.temp_frame.columnconfigure(2, weight = 2)

		self.pulse_transit_frame.columnconfigure(0, weight = 2)
		self.pulse_transit_frame.columnconfigure(2, weight = 2)

		self.abnormal_frame.columnconfigure(0, weight = 0)
		self.abnormal_frame.columnconfigure(1, weight = 2)

		self.heartbeat_text = tk.Label(self.heartbeat_frame, text = "ECG HR", font = self.vitals_subtitle_font,
			anchor = "w", fg=settings.font_color, bg = settings.back_color)
		self.SP02_text = tk.Label(self.SP02_frame, text = "SpO2 %", font = self.vitals_subtitle_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.temp_text = tk.Label(self.temp_frame, text = "TEMP (" + settings.deg + "F)", font = self.vitals_subtitle_font,
		 anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.pulse_transit_text = tk.Label(self.pulse_transit_frame, text = "Pulse TT (MS)", font = self.vitals_subtitle_font,
			anchor ="w",  fg=settings.font_color, bg = settings.back_color)
		self.abnormal_text = tk.Label(self.abnormal_frame, text = "ABNORMAL HB", font = self.vitals_subtitle_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)

		self.heartbeat_label = tk.Label(self.heartbeat_frame, text = self.heartbeat_var, font = self.vitals_text_font,
			fg=settings.font_color, bg = settings.back_color)
		self.SP02_label = tk.Label(self.SP02_frame, text = self.SP02_var, font = self.vitals_text_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.temp_label = tk.Label(self.temp_frame, text = self.temp_var, font = self.vitals_text_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.pulse_transit_label = tk.Label(self.pulse_transit_frame, text = self.pulse_transit_var, font = self.vitals_text_font,
			anchor ="w", fg=settings.font_color, bg = settings.back_color)
		self.abnormal_label = tk.Label(self.abnormal_frame, text = self.abnormal_var, font = self.vitals_text_font,
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

		self.frame_heartbeat_min_max.grid(row = 1, column = 2, sticky = "W")
		self.frame_SP02_min_max.grid(row = 1, column = 2,  sticky = "W")
		self.frame_temp_min_max.grid(row = 1, column = 2,  sticky = "W")
		self.frame_ptt_min_max.grid(row = 1, column = 2, sticky = "W")

		self.heartbeat_min_label = tk.Label(self.frame_heartbeat_min_max, text = "MIN:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.heartbeat_max_label = tk.Label(self.frame_heartbeat_min_max, text = "MAX:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)


		self.SP02_min_label = tk.Label(self.frame_SP02_min_max, text = "MIN:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.SP02_max_label = tk.Label(self.frame_SP02_min_max, text = "MAX:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)


		self.temp_min_label = tk.Label(self.frame_temp_min_max, text = "MIN:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.temp_max_label = tk.Label(self.frame_temp_min_max, text = "MAX:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

		self.ptt_min_label = tk.Label(self.frame_ptt_min_max, text = "MIN:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.ptt_max_label = tk.Label(self.frame_ptt_min_max, text = "MAX:", font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

		self.heartbeat_min_label.grid(row = 0, column = 0, sticky = "W")
		self.heartbeat_max_label.grid(row = 1, column = 0, sticky = "W")

		self.SP02_min_label.grid(row = 0, column = 0, sticky = "W")
		self.SP02_max_label.grid(row = 1, column = 0, sticky = "W")

		self.temp_min_label.grid(row = 0, column = 0, sticky = "W")
		self.temp_max_label.grid(row = 1, column = 0, sticky = "W")

		self.ptt_min_label.grid(row = 0, column = 0, sticky = "W")
		self.ptt_max_label.grid(row = 1, column = 0, sticky = "W")

		self.heartbeat_min_value = tk.Label(self.frame_heartbeat_min_max, text = self.heartbeat_var_min, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.heartbeat_max_value = tk.Label(self.frame_heartbeat_min_max, text = self.heartbeat_var_max, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

		self.SP02_min_value = tk.Label(self.frame_SP02_min_max, text = self.SP02_var_min, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.SP02_max_value= tk.Label(self.frame_SP02_min_max, text = self.SP02_var_max, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

		self.temp_min_value= tk.Label(self.frame_temp_min_max, text = self.temp_var_min, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.temp_max_value = tk.Label(self.frame_temp_min_max, text = self.temp_var_max, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

		self.ptt_min_value = tk.Label(self.frame_ptt_min_max, text = self.ptt_var_min, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)
		self.ptt_max_value = tk.Label(self.frame_ptt_min_max, text = self.ptt_var_max, font = self.vitals_subtext_font, 
			fg=settings.font_color, bg = settings.back_color)

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
		self.ecg_im.set_xdata(np.arange(self.ecg_start_graph_index, self.n))
		self.ecg_im.set_ydata(self.ecg_data[self.ecg_start_graph_index: self.n])
		self.ppg_im.set_xdata(np.arange(self.ecg_start_graph_index, self.n))
		self.ppg_im.set_ydata(self.ppg_data[self.ppg_start_graph_index: self.n])

		#self.heartbeat_var = np.random.randint(40, 60)
		# self.SP02_var = np.random.randint(20, 30)
		# self.temp_var = np.random.randint(98, 102)
		# self.pulse_transit_var = np.random.randint(50, 55)
		# self.abnormal_var = condition_set[np.random.randint(0, 3)]

		self.heartbeat_label.configure(text = self.heartbeat_var)
		# self.SP02_label.configure(text = self.SP02_var)
		# self.temp_label.configure(text = self.temp_var)
		# self.pulse_transit_label.configure(text = self.pulse_transit_var)
		# self.abnormal_label.configure(text = self.abnormal_var)

		#in the case where we need to refresh the x axis
		if ((self.n / self.repeat_length ) > self.frame_num):
			

			self.frame_num = self.n / self.repeat_length
			self.ppg_start_graph_index = self.n 
			self.ecg_start_graph_index = self.n

			limX1 = self.ecg_ax.set_xlim(self.n, self.n + self.repeat_length)
			limX2 = self.ppg_ax.set_xlim(self.n, self.n + self.repeat_length)
			#lim3 = self.ecg_ax.set_ylim([np.amin(self.ecg_data[self.n: self.n + self.repeat_length]), np.amax(self.ecg_data[self.n: self.n + self.repeat_length])])
			#lim4 = self.ppg_ax.set_ylim([np.amin(self.ppg_data[self.n: self.n + self.repeat_length]), np.amax(self.ppg_data[self.n: self.n + self.repeat_length])])
			
			self.ecg_max = 3
			self.ecg_min = -3
			self.ppg_max = 3
			self.ppg_min = -3

			if(self.ecg_data[self.n] > self.ecg_max):
				self.ecg_max = 2*self.ecg_data[self.n]
			elif(self.ecg_data[self.n] < self.ecg_min):
				self.ecg_min = 2*self.ecg_data[self.n]

			if(self.ppg_data[self.n] > self.ppg_max):
				self.ppg_max = 2*self.ppg_data[self.n]
			elif(self.ppg_data[self.n] < self.ppg_min):
				self.ppg_min = 2*self.ppg_data[self.n]

			limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
			limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])

			self.ecg_fig.canvas.draw()
			self.ppg_fig.canvas.draw()

		#otherwise, we can plot efficiently since we don't need to change the viewing window
		else:
			if(self.ecg_data[self.n] > self.ecg_max):
				self.ecg_max = 2*self.ecg_data[self.n]
				limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
				self.ecg_fig.canvas.draw()

			elif(self.ecg_data[self.n] < self.ecg_min):
				self.ecg_min = 2*self.ecg_data[self.n]
				limY1 = self.ecg_ax.set_ylim([self.ecg_min, self.ecg_max])
				self.ecg_fig.canvas.draw()

			else:
				self.ecg_fig.canvas.restore_region(self.ecg_background)
				self.ecg_ax.draw_artist(self.ecg_im)
				self.ecg_fig.canvas.blit(self.ecg_ax.bbox)

			if(self.ppg_data[self.n] > self.ppg_max):
				self.ppg_max = 2*self.ppg_data[self.n]
				limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])
				self.ppg_fig.canvas.draw()

			elif(self.ppg_data[self.n] < self.ppg_min):
				self.ppg_min = 2*self.ppg_data[self.n]
				limY2 = self.ppg_ax.set_ylim([self.ppg_min, self.ppg_max])
				self.ppg_fig.canvas.draw()

			else:
				self.ppg_fig.canvas.restore_region(self.ppg_background)
				self.ppg_ax.draw_artist(self.ppg_im)
				self.ppg_fig.canvas.blit(self.ppg_ax.bbox)

	#graph renderer for live data
	def read_live_samples(self):
		#while(~q.empty()):
		if(self.heartbox_connect_state):
			filtered_data = self.dsp.filt_data_gen()
			if(filtered_data != 'Q' and filtered_data != 'B'):
				#print 'X'
				filtered_ppg = filtered_data[0,:]
				filtered_ecg = filtered_data[1,:]
				self.heartbox_var = self.dsp.calc_heartrate()
				self.ppg_data = np.append(self.ppg_data, filtered_ppg)
				self.ecg_data = np.append(self.ecg_data, filtered_ecg)

				#print self.ppg_data[self.n]
				self.n = self.n + filtered_ecg.size - 1
				self.update_viewer()
				self.root.after(0, self.read_live_samples)
				self.n = self.n + 1
			elif (filtered_data == 'Q'):
				#print 'R'
				self.root.after(0, self.read_live_samples)
			elif (filtered_data == 'B'):
				#print 'B'
				self.root.after(0, self.read_live_samples)

	def read_live_samples_old(self):
		#while(~q.empty()):
		filtered_data = self.dsp.filt_data_gen()

		filtered_ppg = filtered_data[0,:]
		filtered_ecg = filtered_data[1,:]
		if(filtered_ecg != 'Q' and filtered_ppg != 'Q' ):
			self.heartbox_var = self.dsp.calc_heartrate()
			self.ppg_data = np.append(self.ppg_data, filtered_ppg)
			self.ecg_data = np.append(self.ecg_data, filtered_ecg)

			#print self.ppg_data[self.n]
			self.update_viewer()
			self.root.after(0, self.read_live_samples)
			self.n = self.n + 1
		else:
			self.root.after(0, self.read_live_samples)

	def bind_shortcuts(self):
		self.root.bind("<F11>", self.toggle_fullscreen)
		self.root.bind("<Escape>", self.end_fullscreen)

	def connect_heartbox(self):
		self.heartbox_connect_state = True
		if(self.ecg_disconnect_state):
			self.toggle_ecg_disconnect()
			self.toggle_ppg_disconnect()
		self.startup()

	def disconnect_heartbox(self):
		self.heartbox_connect_state = False
		if(not self.ecg_disconnect_state):
			self.toggle_ecg_disconnect()
			self.toggle_ppg_disconnect()

	def toggle_fullscreen(self, event=None):
		self.fullscreen_state = not self.fullscreen_state  # Just toggling the boolean
		self.root.attributes("-fullscreen", self.fullscreen_state)

		if(not self.fullscreen_state):
			ecg_width = self.ecg_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width) 
			ecg_height = self.ecg_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)
			ppg_width = self.ppg_fig.get_size_inches()[0] * float(self.min_screen_width) / float(self.screen_width)
			ppg_height = self.ppg_fig.get_size_inches()[1] * float(self.min_screen_height) / float(self.screen_height)
			self.spacer_menu.config(text = settings.spacer_text)	
			#self.ecg_fig.set_size_inches(ecg_width, ecg_height)
			#self.ppg_fig.set_size_inches(ppg_width, ppg_height)
			#self.ecg_fig.canvas.draw()
			#self.ppg_fig.canvas.draw()

		else:
			ecg_width = float(self.ecg_fig.get_size_inches()[0]) * float(self.screen_width) / float(self.min_screen_width)
			ecg_height = float(self.ecg_fig.get_size_inches()[1]) * float(self.screen_height) /  float(self.min_screen_height)
			ppg_width = float(self.ppg_fig.get_size_inches()[0])* float(self.screen_width) /float(self.min_screen_width)
			ppg_height = float(self.ppg_fig.get_size_inches()[1])* float(self.screen_height) / float(self.min_screen_height)
			self.spacer_menu.config(text = settings.spacer_text + ' ' * int(len(settings.spacer_text)*float(self.min_screen_width) / float(self.screen_width)))
			#self.ecg_fig.set_size_inches(ecg_width, ecg_height, forward=True)
			#self.ppg_fig.set_size_inches(ppg_width, ppg_height, forward=True)
			#self.ecg_fig.canvas.draw()
			#self.ppg_fig.canvas.draw()

		return "break"

	def toggle_ecg_disconnect(self):
		if(not self.ecg_disconnect_state):
			self.ecg_disconnect.set_text('---- DISCONNECTED ----')
			self.ecg_disconnect_state = True

		else:
			self.ecg_disconnect.set_text('')
			self.ecg_disconnect_state = False

		self.ecg_fig.canvas.draw()
		self.ppg_fig.canvas.draw()

	def toggle_ppg_disconnect(self):
		if(not self.ppg_disconnect_state):
			self.ppg_disconnect.set_text('---- DISCONNECTED ----')
			self.ppg_disconnect_state = True
		else:
			self.ppg_disconnect.set_text('')
			self.ppg_disconnect_state = False

		self.ecg_fig.canvas.draw()
		self.ppg_fig.canvas.draw()

	def end_fullscreen(self, event=None):
		self.fullscreen_state = False

		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()

		self.curr_screen_width = 1200
		self.curr_screen_height = 700

		self.root.attributes("-fullscreen", False)
		return "break"

if __name__ == "__main__":
	graph_viewer = heartbox_wave_viewer()
