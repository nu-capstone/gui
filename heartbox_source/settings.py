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

condition_set = ('NORMAL', 'NORMAL', 'NORMAL')

isComm = 1 #currently hard-coded settings for live reading (1) or from file (0)

UDP_IP = "192.168.56.1" #only for UDP communication with old PCB
UDP_PORT = 50007  #only for UDP communication with old PCB



global q 
q = multiprocessing.Queue()

