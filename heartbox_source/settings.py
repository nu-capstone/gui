import settings

deg =  u"\u00b0"

condition_set = ('Normal', 'Warning', 'Critical')

isComm = 1
UDP_IP = "192.168.56.1"
UDP_PORT = 50007

filterCoeffB_ppg_H, filterCoeffA_ppg_H = signal.butter(5,.0025,'highpass')
filterCoeffB_ppg_L, filterCoeffA_ppg_L = signal.butter(5,.2,'lowpass')
filterCoeffB_ecg_H, filterCoeffA_ecg_H = signal.butter(5,.005,'highpass')
filterCoeffB_ecg_L, filterCoeffA_ecg_L = signal.butter(5,.3,'lowpass')
filter_length = 20
sample_rate = 50.0

q = multiprocessing.Queue()


