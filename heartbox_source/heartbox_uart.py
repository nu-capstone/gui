import serial
 
ser = serial.Serial()
ser.baudrate = 460800
ser.port = 'COM3'
 
ser.open()
 
s = ser.read()
 
print(s)
while(True):
    s = ser.read(22)
    ser.write(b'r a')
    print(s)

def simulation(q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((UDP_IP, UDP_PORT))
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