import serial
import settings
import socket
from bluetooth import *
import pdb
import time
import pprint
def heartbox_uart_receive(q):
	ser = serial.Serial()
	ser.baudrate = 460800
	ser.open()
	s = ser.read()

	while True:
			#time.sleep(1)
		data, addr = ser.read(22)
		#ser.write(b'r a')
		#print(s)

		settings.q.put(data)
	ser.close()
	settings.q.put('Q')

def heartbox_uart_send():
	return 0

def heartbox_udp_receive(q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((settings.UDP_IP, settings.UDP_PORT))
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
		#print settings.q.get()
	sock.close()
	q.put('Q')

def heartbox_bt_connect():
	target_name = "PC36100"
	target_address = None

	nearby_devices = discover_devices()
	#pdb.set_trace()

	for bdaddr in nearby_devices:
		if target_name == lookup_name( bdaddr ):
			target_address = bdaddr
			break

	if target_address is not None:
		print "found target bluetooth device with address ", target_address
		return 0
	else:
		print "could not find target bluetooth device nearby"
		return 0


def heartbox_bt_send(packet):
	target_address =  'AC:CF:85:28:E9:40'
	service = find_service(address = target_address)
	pp =  pprint.PrettyPrinter(indent=4)
	pp.pprint(service)

	client_socket = BluetoothSocket( RFCOMM )
	client_socket.connect((target_address, 3))
	while(1):
		data = client_socket.send("hello")
		print data
	return 0

def heartbox_bt_receive():
	return 0
