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
import multiprocessing
import socket
import time

condition_set = ('Normal', 'Warning', 'Critical')
deg =  u"\u00b0"
isComm = 1
UDP_IP = "192.168.56.1"
UDP_PORT = 50007

q = multiprocessing.Queue()

filterCoeffB_ppg_H, filterCoeffA_ppg_H = signal.butter(5,.0025,'highpass')
filterCoeffB_ppg_L, filterCoeffA_ppg_L = signal.butter(5,.2,'lowpass')
filterCoeffB_ecg_H, filterCoeffA_ecg_H = signal.butter(5,.005,'highpass')
filterCoeffB_ecg_L, filterCoeffA_ecg_L = signal.butter(5,.3,'lowpass')

filter_length = 20
sample_rate = 50.0

def simulation(q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((UDP_IP, UDP_PORT))
	while True:
			#time.sleep(1)
		data, addr = sock.recvfrom(100)
		#sample = int(data[26:34],16);
		#print data + '\n'
		#time.sleep()
		#sample = 0.00025
		#print sample
				#here send any data you want to send to the other process, can be any pickable object
		q.put(data)
	sock.close()
	q.put('Q')


class heartbox_wave_viewer:
	def __init__(self):
		self.root = tk.Tk()
		self.numSamples = 0
		self.fifo_ppg_length = 1024
		self.fifo_ecg_length = 1024
		self.fifo_ecg = np.zeros(self.fifo_ppg_length)
		self.fifo_ppg = np.zeros(self.fifo_ppg_length)

		self.root.title('HeartBox Wavetool')
		self.root.minsize(width=900, height = 700)
		self.setup_plots()
		self.viewer_layout()
		self.startup()

	def startup(self):

		#Create and start the simulation process

		#pdb.set_trace()
		#for offline viewing, reads data from csv
		if (isComm):
			self.simulate=multiprocessing.Process(None,simulation,args=(q,))
			self.simulate.start()
			#pdb.set_trace()
			self.read_live_samples()
		else:
			self.read_recorded_samples()

	#setup elements needed for plots
	def setup_plots(self):
		if (isComm):
			self.ecg_data = np.array([])
			self.ppg_data = np.array([])
		else:
			self.ecg_data = np.genfromtxt('ecg.csv', delimiter = ',')
			self.ppg_data = np.genfromtxt('ppg.csv', delimiter = ',')
		
		#setup figure
		self.ecg_fig = plt.figure()
		self.ppg_fig = plt.figure()
		self.ecg_fig.set_size_inches(6,3.5)
		self.ppg_fig.set_size_inches(6,3.5)
		self.ecg_ax = self.ecg_fig.add_subplot(1,1,1)
		self.ppg_ax = self.ppg_fig.add_subplot(1,1,1)

		self.ecg_ax.set_frame_on(False)
		self.ppg_ax.set_frame_on(False)

		self.ecg_ax.grid(color = '#add8e6', linestyle='--')
		self.ppg_ax.grid(color = '#add8e6', linestyle='--', )

		self.ecg_ax.set_facecolor('black')
		self.ppg_ax.set_facecolor('black')

		#set up viewing window (in this case the 25 most recent values)
		#self.repeat_length = (np.shape(self.ecg_data)[0]+1)/10
		self.repeat_length = 250
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

	#establishes basic layout of GUI elements
	def viewer_layout(self):

		self.heartbeat_var = tk.IntVar()
		self.SP02_var = tk.IntVar()
		self.temp_var = tk.IntVar()
		self.pulse_transit_var = tk.IntVar()
		self.abnormal_var = tk.StringVar()

		self.heartbeat_var = np.random.randint(40, 60)
		self.SP02_var = np.random.randint(20, 30)
		self.temp_var = np.random.randint(98, 102)
		self.pulse_transit_var = np.random.randint(50, 55)
		self.abnormal_var = condition_set[np.random.randint(0, 3)]


		self.text_monitor_frame = tk.LabelFrame(self.root, bd = 3, 
			text = "Vitals", font = 8, padx = 5)
		self.text_monitor_frame.grid(column = 1, row = 1, rowspan = 2, padx = 10)
		self.text_monitor_frame.rowconfigure(1, weight = 1)
		self.text_monitor_frame.rowconfigure(2, weight = 1)

		self.heartbeat_frame = tk.Frame(self.text_monitor_frame, bd = 1, 
			relief="raised", width = 500)
		self.SP02_frame = tk.Frame(self.text_monitor_frame, bd = 1, 
			relief="raised", width = 500)
		self.temp_frame = tk.Frame(self.text_monitor_frame, bd = 1,
		 relief="raised", width = 500)
		self.pulse_transit_frame = tk.Frame(self.text_monitor_frame, bd = 1,
		 relief="raised", width = 500)
		self.abnormal_frame = tk.Frame(self.text_monitor_frame, bd = 1,
		 relief="raised", width = 500)

		self.heartbeat_frame.columnconfigure(0, weight = 1)
		self.heartbeat_frame.columnconfigure(1, weight = 1)

		self.SP02_frame.columnconfigure(0, weight = 1)
		self.SP02_frame.columnconfigure(1, weight = 1)

		self.temp_frame.columnconfigure(0, weight = 1)
		self.temp_frame.columnconfigure(1, weight = 1)

		self.pulse_transit_frame.columnconfigure(0, weight = 1)
		self.pulse_transit_frame.columnconfigure(1, weight = 1)

		self.abnormal_frame.columnconfigure(0, weight = 1)
		self.abnormal_frame.columnconfigure(1, weight = 1)

		self.heartbeat_frame.grid(row = 0, column = 0)
		self.SP02_frame.grid(row = 1, column = 0)
		self.temp_frame.grid(row = 2, column = 0)
		self.pulse_transit_frame.grid(row = 3, column = 0)
		self.abnormal_frame.grid(row = 4, column = 0)

		self.heartbeat_text = tk.Label(self.heartbeat_frame, text = "ECG  HR",
		 anchor ="w", width = 40)
		self.SP02_text = tk.Label(self.SP02_frame, text = "SpO2  %", 
			anchor ="w", width = 40)
		self.temp_text = tk.Label(self.temp_frame, text = "TEMP  " + deg + "F",
		 anchor ="w", width = 40)
		self.pulse_transit_text = tk.Label(self.pulse_transit_frame, text = "PULSE TRANSIT TIME  MS", 
			anchor ="w", width = 40)
		self.abnormal_text = tk.Label(self.abnormal_frame, text = "ABNORMAL HB", 
			anchor ="w", width = 40)

		self.heartbeat_text.config(font=(None, 9))
		self.SP02_text.config(font=(None,9))
		self.temp_text.config(font=(None, 9))
		self.pulse_transit_text.config(font=(None, 9))
		self.abnormal_text.config(font=(None, 9))

		self.heartbeat_label = tk.Label(self.heartbeat_frame, text = self.heartbeat_var, 
			width = 6, pady = 10)
		self.SP02_label = tk.Label(self.SP02_frame, text = self.SP02_var, 
			width = 6, pady = 10)
		self.temp_label = tk.Label(self.temp_frame, text = self.temp_var, 
			width = 6, pady = 10)
		self.pulse_transit_label = tk.Label(self.pulse_transit_frame, text = self.pulse_transit_var, 
			width = 6, pady = 10)
		self.abnormal_label = tk.Label(self.abnormal_frame, text = self.abnormal_var,
		 width = 6, pady = 10)

		self.heartbeat_label.config(font=(None, 60))
		self.SP02_label.config(font=(None, 60))
		self.temp_label.config(font=(None, 60))
		self.pulse_transit_label.config( font=(None, 60))
		self.abnormal_label.config(font=(None, 40))

		self.heartbeat_text.grid(row = 0, column = 0, columnspan = 2)
		self.SP02_text.grid(row = 0, column = 0, columnspan = 2)
		self.temp_text.grid(row = 0, column = 0, columnspan = 2)
		self.pulse_transit_text.grid(row = 0, column = 0, columnspan = 2)
		self.abnormal_text.grid(row = 0, column = 0, columnspan = 2)

		self.heartbeat_label.grid(row = 1, column = 0, columnspan = 2)
		self.SP02_label.grid(row = 1, column = 0, columnspan = 2)
		self.temp_label.grid(row = 1, column = 0, columnspan = 2)
		self.pulse_transit_label.grid(row = 1, column = 0, columnspan = 2)
		self.abnormal_label.grid(row = 1, column = 0, columnspan = 2)

		self.ecg_graph_frame = tk.LabelFrame(self.root, bd = 3, text = "ECG Raw Data")
		self.ecg_graph_frame.grid(column = 0, row = 1)
		self.ecg_canvas = FigureCanvasTkAgg(self.ecg_fig, master=self.ecg_graph_frame)
		self.ecg_canvas.show()
		self.ecg_canvas.get_tk_widget().grid(column=0,row=0)

		self.ppg_graph_frame = tk.LabelFrame(self.root, bd = 3, text = "PPG Raw Data")
		self.ppg_graph_frame.grid(column = 0, row = 2)
		self.ppg_canvas = FigureCanvasTkAgg(self.ppg_fig, master=self.ppg_graph_frame)
		self.ppg_canvas.show()
		self.ppg_canvas.get_tk_widget().grid(column=0,row=0)

	#graph renderer for recorded data
	def read_recorded_samples(self):
		self.n = self.n + 1
		self.update_viewer()
		#pdb.set_trace()
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

		if ((self.n % self.repeat_length) == 0):

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

		# else:
		# 	# makes it look ok when the animation loops
		# 	lim1 = self.ecg_ax.set_xlim(0, self.repeat_length)
		# 	lim2 = self.ppg_ax.set_xlim(0, self.repeat_length)
		# 	lim3 = self.ecg_ax.set_ylim([np.amin(self.ecg_data[0: self.repeat_length]),
		# 	 np.amax(self.ecg_data[0: self.repeat_length])])
		# 	lim4 = self.ppg_ax.set_ylim([np.amin(self.ppg_data[0: self.repeat_length]),
		# 	 np.amax(self.ppg_data[0: self.repeat_length])])

		# 	self.ecg_fig.canvas.restore_region(self.ecg_background)
		# 	self.ppg_fig.canvas.restore_region(self.ppg_background)

		# 	self.ecg_ax.draw_artist(self.ecg_im)
		# 	self.ppg_ax.draw_artist(self.ppg_im)

		# 	self.ecg_fig.canvas.blit(self.ecg_ax.bbox)
		# 	self.ppg_fig.canvas.blit(self.ppg_ax.bbox)

	#graph renderer for live data
	def read_live_samples(self):
		#while(~q.empty()):
		filtered_ppg, filtered_ecg = self.filt_data_gen()
		self.calc_heartrate()

		if(filtered_ecg != 'Q'):
			self.ppg_data = np.append(self.ppg_data, filtered_ppg)
			self.ecg_data = np.append(self.ecg_data, filtered_ecg)

			#print self.ppg_data[self.n]
			self.update_viewer()
			self.root.after(0, self.read_live_samples)
			self.n = self.n + 1
		else:
			self.root.after(0, self.read_live_samples)

	def filt_data_gen(self):
		# check if new sample ready
		if(~q.empty()):
			sample = q.get()
			#print sample
		else:
			return 'Q'

		A = int(sample[42:50], 16)
		B = int(sample[50:58], 16)


		print A, B
		self.fifo_ppg = np.append(self.fifo_ppg[1:],int(sample[26:34],16))
		self.fifo_ecg = np.append(self.fifo_ecg[1:], A-B)

		self.numSamples = self.numSamples + 1

		if(self.numSamples < filter_length):
			return 0, 0
		else:
			#import pdb; pdb.set_trace()
			filtered_ppg = signal.filtfilt(filterCoeffB_ppg_L,filterCoeffA_ppg_L,\
				self.fifo_ppg[self.fifo_ppg.size - filter_length:])

			filtered_ppg = signal.filtfilt(filterCoeffB_ppg_H,filterCoeffA_ppg_H,filtered_ppg)

			moving_ppg_avg = np.sum(filtered_ppg)


			filtered_ecg = signal.filtfilt(filterCoeffB_ecg_L,filterCoeffA_ecg_L,\
				self.fifo_ecg[self.fifo_ecg.size - filter_length:])
			#filtered_ecg = signal.filtfilt(filterCoeffB_ecg_H,filterCoeffA_ecg_H,filtered_ecg)
			#moving_ecg_avg = np.sum(filtered_ecg)

			return moving_ppg_avg, filtered_ecg[filter_length-1]
			#return filteredArray[filter_length - 1]

	def calc_heartrate(self):
		if(self.numSamples%(5*sample_rate)==0 and self.numSamples > 1000):
			hb_fft = np.fft.fft(self.fifo_ppg)
			#pdb.set_trace()
			#plt.figure()
			#plt.plot(abs(hb_fft))
			low_bound = int (np.floor(.5/(sample_rate/self.fifo_ppg_length)))
			high_bound = int (np.floor(3/(sample_rate/self.fifo_ppg_length)))
			#pdb.set_trace()
			heartbeat_index = np.argmax(abs(hb_fft[low_bound: high_bound]))
			#print heartbeat_index
			self.heartbeat_var = int((heartbeat_index+low_bound) * sample_rate / self.fifo_ppg_length * 60)
			#plt.show()
			#print self.heartbeat_var


	#renders a single frame of plotting ECG/PPG data and biometrics	

if __name__ == "__main__":
	graph_viewer = heartbox_wave_viewer()
