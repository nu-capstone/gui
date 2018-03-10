import serial
 
def heartbox_uart(q):
	ser = serial.Serial()
	ser.baudrate = 460800
	ser.open()
	s = ser.read()

	while True:
			#time.sleep(1)
		data, addr = ser.read(22)
    	#ser.write(b'r a')
    	#print(s)

		q.put(data)
	sock.close()
	q.put('Q')