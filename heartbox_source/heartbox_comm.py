import serial
import settings
import socket
from bluetooth import *
import sys
import pprint
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

    return target_address


def heartbox_bt_send():
	addr = '30:19:66:8E:01:3F'

	service_matches = find_service(address = addr)
	#pp =  pprint.PrettyPrinter(indent=4)
	#pp.pprint(service_matches)




	# if len(service_matches) == 0:
	#     print("couldn't find the SampleServer service =(")
	#     sys.exit(0)


	for service in service_matches:
  		try:
	   		if "HeartBox" in service["name"]:
	   			port = service["port"]
	   			name = service["name"]
	   			host = service["host"]
	   	except:
			print("fail")


	# first_match = service_matches[0]
	# port = first_match["port"]
	# name = first_match["name"]
	# host = first_match["host"]

	print("connecting to \"%s\" on %s" % (name, host))

	# Create the client socket
	sock=BluetoothSocket( RFCOMM )
	sock.connect((host, port))

	print("connected.  type stuff")
	while True:
		#data = input()
		data = "1";
		sock.send(data)

	sock.close()

def heartbox_bt_receive():
	return 0
