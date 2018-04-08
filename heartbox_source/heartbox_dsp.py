from scipy import signal
import numpy as np
import pdb
import settings

filterCoeffB_ppg_H, filterCoeffA_ppg_H = signal.butter(5,.0025,'highpass')
filterCoeffB_ppg_L, filterCoeffA_ppg_L = signal.butter(5,.1,'lowpass')
filterCoeffB_ecg_H, filterCoeffA_ecg_H = signal.butter(5,.005,'highpass')
filterCoeffB_ecg_L, filterCoeffA_ecg_L = signal.butter(5,.3,'lowpass')

filterCoeffB_sp02_H, filterCoeffA_sp02_H = signal.butter(5,.0025,'highpass')
filterCoeffB_sp02_L, filterCoeffA_sp02_L = signal.butter(5,.1,'lowpass')


filter_length = 20 #cannot be hardcoded
sample_rate = 50.0
num_seconds = 20

class heartbox_dsp:
	def __init__(self):
		self.numSamples = 0
		self.fifo_ppg_length = 1024
		self.fifo_ecg_length = 1024
		self.fifo_ecg = np.zeros(self.fifo_ppg_length)
		self.fifo_ppg = np.zeros(self.fifo_ppg_length)
		self.fifo_R = np.zeros(int(sample_rate*num_seconds))
		self.fifo_IR = np.zeros(int(sample_rate*num_seconds))
		self.SP02_counter = 0
		self.SP02_valid = False
		self.SP02_value = 0
		#self.f = open("sp02.txt","w")

	def parse_sample(self, sample):
		if(len(sample) < 30):
			return 0, 0, 0, int(sample[-16:-8], 16), int(sample[-8:], 16)
		else:
			return int(sample[42:50], 16), int(sample[50:58], 16), int(sample[26:34],16), 0, 0


	def filt_data_gen(self):
		# check if new sample ready
		#pdb.set_trace()
		sample_buffer = []
		i = 0

		while not settings.q.empty():

			sample_buffer.append(settings.q.get_nowait())
			i = i + 1

		#print i
		filtered_data = np.zeros((4,i))

		if(i > 0):
			for x in range(i):
	 			sample = sample_buffer[x]
	 			#print sample
	 			E1, E2, G, R, IR = self.parse_sample(sample)
				#print R, IR 
				#E1 = E2 = G = R = IR = 0

				#print A, B
				#pdb.set_trace()
				self.fifo_ppg = np.append(self.fifo_ppg[1:], G) # FIX LATER
				self.fifo_ecg = np.append(self.fifo_ecg[1:], E1-E2)
				self.fifo_IR = np.append(self.fifo_IR[1:], IR)
				self.fifo_R = np.append(self.fifo_R[1:], R)

				self.numSamples = self.numSamples + 1

				self.calc_SP02()

				if(self.numSamples < filter_length):
					continue
				else:
					filtered_ppg = signal.filtfilt(filterCoeffB_ppg_L,filterCoeffA_ppg_L,\
						self.fifo_ppg[self.fifo_ppg.size - filter_length:])

					filtered_ppg = signal.filtfilt(filterCoeffB_ppg_H,filterCoeffA_ppg_H,filtered_ppg)

					moving_ppg_avg = np.sum(filtered_ppg)

					filtered_ecg = signal.filtfilt(filterCoeffB_ecg_L,filterCoeffA_ecg_L,\
						self.fifo_ecg[self.fifo_ecg.size - filter_length:])
					#filtered_ecg = signal.filtfilt(filterCoeffB_ecg_H,filterCoeffA_ecg_H,filtered_ecg)
					#moving_ecg_avg = np.sum(filtered_ecg)

					filtered_ppg_R = signal.filtfilt(filterCoeffB_sp02_L,filterCoeffA_sp02_L,\
						self.fifo_R[self.fifo_R.size - filter_length:])


					filtered_ppg_R = signal.filtfilt(filterCoeffB_sp02_H,filterCoeffA_sp02_H,filtered_ppg_R)


					filtered_ppg_IR = signal.filtfilt(filterCoeffB_sp02_L,filterCoeffA_sp02_L,\
						self.fifo_IR[self.fifo_IR.size - filter_length:])


					filtered_ppg_IR = signal.filtfilt(filterCoeffB_sp02_H,filterCoeffA_sp02_H,filtered_ppg_IR)

					filtered_data[:,x] = [moving_ppg_avg, filtered_ecg[filter_length-1], filtered_ppg_R[filter_length-1], filtered_ppg_IR[filter_length-1]]

			if(self.numSamples < filter_length):
				return 'B'
			return filtered_data

		else:
			return 'Q'

			#else:
				#print 'Q'
	def calc_SP02(self):
		if(self.fifo_R[-1] < 4000):
			self.SP02_valid = False
			self.SP02_counter = 0
			return 0
		elif(self.SP02_counter == sample_rate * num_seconds):
			self.SP02_valid = True
			filteredR = signal.filtfilt(filterCoeffB_ppg_L,filterCoeffA_ppg_L,self.fifo_R)
			filteredIR = signal.filtfilt(filterCoeffB_ppg_L,filterCoeffA_ppg_L,self.fifo_IR)

			AC_R = np.average(np.absolute(np.gradient(filteredR)))
			DC_R = np.average(filteredR)
			AC_IR = np.average(np.absolute(np.gradient(filteredIR)))
			DC_IR = np.average(filteredIR)
			self.SP02_value = (AC_R/DC_R)/(AC_IR/DC_IR)
			self.SP02_value = int(np.floor(106 - 20*(self.SP02_value)))
			return self.SP02_value
			#print self.SP02_value
			#self.f.write("%f \n"% self.SP02_value)

		else:
			self.SP02_valid = False
			self.SP02_counter = self.SP02_counter + 1
			return 0


	def calc_heartrate(self):
		if(self.numSamples%(5*sample_rate) == 0 and self.numSamples > 1000):
			hb_fft = np.fft.fft(self.fifo_ppg)
			#pdb.set_trace()
			#plt.figure()
			#plt.plot(abs(hb_fft))
			low_bound = int (np.floor(.5/(sample_rate/self.fifo_ppg_length)))
			high_bound = int (np.floor(3/(sample_rate/self.fifo_ppg_length)))
			#pdb.set_trace()
			heartbeat_index = np.argmax(abs(hb_fft[low_bound: high_bound]))
			#print heartbeat_index
			return int((heartbeat_index+low_bound) * sample_rate / self.fifo_ppg_length * 60)
			#plt.show()
			#print self.heartbeat_var
