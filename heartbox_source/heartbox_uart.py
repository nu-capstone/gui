import serial
 
def heartbox_uart():
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


def heartbox_udp():
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
	sock.close()
	q.put('Q')

