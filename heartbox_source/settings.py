import multiprocessing
from scipy import signal
import tempfile

deg =  u"\u00b0" #degree unicode
graph_color = '#32cd32' #neon green, colors the data
font_color = '#32cd32'  #neon green, colors the text
grid_color = '#32cd32'  #neon green, colors the graph's grid/axes
back_color = '#000000' #neon green, colors the background

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

condition_set = ('NORMAL', 'WARNING', 'CRITICAL')

isComm = 1 #currently hard-coded settings for live reading (1) or from file (0)

UDP_IP = "192.168.56.1" #only for UDP communication with old PCB
UDP_PORT = 50007  #only for UDP communication with old PCB


filterCoeffB_ppg_H, filterCoeffA_ppg_H = signal.butter(5,.0025,'highpass')
filterCoeffB_ppg_L, filterCoeffA_ppg_L = signal.butter(5,.2,'lowpass')
filterCoeffB_ecg_H, filterCoeffA_ecg_H = signal.butter(5,.005,'highpass')
filterCoeffB_ecg_L, filterCoeffA_ecg_L = signal.butter(5,.3,'lowpass')

filter_length = 20
sample_rate = 50.0

q = multiprocessing.Queue()

