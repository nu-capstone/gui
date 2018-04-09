import serial
import settings
import socket
#from bluetooth import *
import sys
import pdb
import time
import string

addr = ''
port = ''
host = ''
#sock = BluetoothSocket( RFCOMM )

def heartbox_uart_conf_reg(text):
	ser = serial.Serial('COM3', baudrate = 460800, timeout = 3)

	if(ser.isOpen() == False):
		ser.open()

	ser.write(text + '\n')
	ser.close()

def heartbox_uart_receive(q):
	ser = serial.Serial('COM3', baudrate = 460800, timeout = 3)
	
	#import pdb; pdb.set_trace()
	if(ser.isOpen() == False):
		ser.open()

	ser.write('s0\r\n')
	ser.readline()

	ser.write('s0\n')
	ser.readline()

	print ser
	# asdfasdf

	filename = "RI_DEFAULT.dcfg"
	filename =  "R01_142RI.dcfg"


	with open(filename) as inputfile:
		for line in inputfile:
			s = line[0:2]
			if(all(c in string.hexdigits for c in s)):
				addr = line[0:2]
				data = line[3:7]

				print(addr, data)

				ser.write('w ' + addr + ' ' + data + '\n')
				ser.readline()
				ser.readline()
				print ser.readline()

	#ser.write('w 12 3D\n') # sample rate 130
	#ser.readline()
	#ser.readline()
	#ser.readline()

	# ser.write('w 36 0290\n') # 1 pulse timeslot B
	# ser.readline()
	# ser.readline()
	# ser.readline()

	#ser.write('w 44 1C26\n') # reduce gain to 25k
	#ser.readline()
	#ser.readline()
	#ser.readline()

	print("got here")

	time.sleep(1)

	ser.write('t a a\n')
	ser.readline()

	time.sleep(1)

	ser.write('s1\r\n')
	ser.readline()
	
	ser.write('s1\n')

	while True:
			#time.sleep(1)
		data = ser.readline()
		#ser.write(b'r a')
		
		try:
			if(data[1] == "#"):
				q.put(data)

		except:
			print data
			print("HI")
			#print(data)

	ser.close()
	q.put('Q')

def heartbox_uart_send():
	return 0

def heartbox_udp_receive(q):
	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
	udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	udp_sock.bind((settings.UDP_IP, settings.UDP_PORT))
	while True:
			#time.sleep(1)
		data, addr = udp_sock.recvfrom(100)
		#sample = int(data[26:34],16);
		#print data + '\n'
		#time.sleep()
		#sample = 0.00025
		#print sample
				#here send any data you want to send to the other process, can be any pickable object
		q.put(data)
		#print settings.q.get()
	udp_sock.close()
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
