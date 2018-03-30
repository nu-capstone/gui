from scipy import signal
import numpy as np
import pdb
import settings

filterCoeffB_ppg_H, filterCoeffA_ppg_H = signal.butter(5,.0025,'highpass')
filterCoeffB_ppg_L, filterCoeffA_ppg_L = signal.butter(5,.2,'lowpass')
filterCoeffB_ecg_H, filterCoeffA_ecg_H = signal.butter(5,.005,'highpass')
filterCoeffB_ecg_L, filterCoeffA_ecg_L = signal.butter(5,.3,'lowpass')

filter_length = 20 #cannot be hardcoded
sample_rate = 50.0

class heartbox_dsp:
	def __init__(self):
		self.numSamples = 0
		self.fifo_ppg_length = 1024
		self.fifo_ecg_length = 1024
		self.fifo_ecg = np.zeros(self.fifo_ppg_length)
		self.fifo_ppg = np.zeros(self.fifo_ppg_length)

	def filt_data_gen1(self):
		# check if new sample ready
		#pdb.set_trace()
		if not(settings.q.empty()):
			#print 'R'
			sample = settings.q.get_nowait()
			print sample
		else:
			#print 'Q'
			return 'Q', 'Q'

		A = int(sample[42:50], 16)
		B = int(sample[50:58], 16)

		print A, B
		#pdb.set_trace()
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


	def filt_data_gen(self):
		# check if new sample ready
		#pdb.set_trace()
		sample_buffer = []
		i = 0

		while not settings.q.empty():
			sample_buffer.append(settings.q.get_nowait())
			i = i + 1

		#print i
		filtered_data = np.zeros((2,i))

		if(i > 0):
			for x in range(i):
	 			sample = sample_buffer[x]
				A = int(sample[42:50], 16)
				B = int(sample[50:58], 16)

				#print A, B
				#pdb.set_trace()
				self.fifo_ppg = np.append(self.fifo_ppg[1:],int(sample[26:34],16))
				self.fifo_ecg = np.append(self.fifo_ecg[1:], A-B)
				self.numSamples = self.numSamples + 1

				if(self.numSamples < filter_length):
					continue
				else:
					#pdb.set_trace()
					filtered_ppg = signal.filtfilt(filterCoeffB_ppg_L,filterCoeffA_ppg_L,\
						self.fifo_ppg[self.fifo_ppg.size - filter_length:])

					filtered_ppg = signal.filtfilt(filterCoeffB_ppg_H,filterCoeffA_ppg_H,filtered_ppg)

					moving_ppg_avg = np.sum(filtered_ppg)

					filtered_ecg = signal.filtfilt(filterCoeffB_ecg_L,filterCoeffA_ecg_L,\
						self.fifo_ecg[self.fifo_ecg.size - filter_length:])
					#filtered_ecg = signal.filtfilt(filterCoeffB_ecg_H,filterCoeffA_ecg_H,filtered_ecg)
					#moving_ecg_avg = np.sum(filtered_ecg)

					filtered_data[:,x] = [moving_ppg_avg, filtered_ecg[filter_length-1]]

			if(self.numSamples < filter_length):
				return 'B'
			return filtered_data

		else:
			return 'Q'

			#else:
				#print 'Q'

	def filt_data_gen1(self):
		# check if new sample ready
		#pdb.set_trace()
		if(~q.empty()):
			sample = q.get()
			#print sample
		else:
			return 'Q'			

			A = int(sample[42:50], 16)
			B = int(sample[50:58], 16)

			print A, B
			#pdb.set_trace()
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
			return int((heartbeat_index+low_bound) * sample_rate / self.fifo_ppg_length * 60)
			#plt.show()
			#print self.heartbeat_var
