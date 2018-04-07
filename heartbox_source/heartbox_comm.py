import serial
import settings
import socket
from bluetooth import *
import sys
import pprint
import pdb
import time
import pprint

addr = ''
port = ''
host = ''
sock = BluetoothSocket( RFCOMM )


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
	upd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	upd_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	upd_sock.bind((settings.UDP_IP, settings.UDP_PORT))
	while True:
			#time.sleep(1)
		data, addr = upd_sock.recvfrom(100)
		#sample = int(data[26:34],16);
		#print data + '\n'
		#time.sleep()
		#sample = 0.00025
		#print sample
				#here send any data you want to send to the other process, can be any pickable object
		q.put(data)
		#print settings.q.get()
	upd_sock.close()
	q.put('Q')

def heartbox_bt_connect():
    target_name = "SCH-I545"
    target_address = None
    nearby_devices = discover_devices()
    for bdaddr in nearby_devices:
        if target_name == lookup_name( bdaddr ):
            target_address = bdaddr
            break
    if target_address is not None:
        print("found target bluetooth device with address ", target_address)
    else:
        print("could not find target bluetooth device nearby")

   	addr = target_address
	service_matches = find_service(address = addr)

	for service in service_matches:
  		try:
	   		if "HeartBox" in service["name"]:
	   			port = service["port"]
	   			name = service["name"]
	   			host = service["host"]
	   			sock.connect((host, port))
	   	except:
			print("fail")
			heartbox_bt_disconnect()

def heartbox_bt_send(packet):
	# Create the client socket
	sock.send(packet)

def heartbox_bt_disconnect():
	sock.close()

def heartbox_bt_receive():
	return 0
