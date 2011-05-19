# -*- coding: cp1252 -*-

import time
import signal
import sys

import serial
ser = serial.Serial()
ser.port = 3 # muda entre PCs
ser.baudrate = 57600
if ser.isOpen():
    ser.close()
    ser.open()
else:
    ser.open()

def decode(code):
    deco = []
    for a in code:
        deco.append(ord(a))
    return deco
    
def listen(b):
    msg = b
    while 1:
        a = ser.read(1)
        if a == '\x7E':
            msg += a
            return msg
        else:
            msg += a
    return msg

def main():
	d = open('messages.txt','w')
	
	while True:
	    try:
	        b = ser.read(1)
	        if b == '\x7E':
	            print "7E found"
	            msg_array = decode(listen(b))
	            print map(hex,msg_array)
	            stringtofile = ""
	            for a in msg_array:
	                stringtofile += str(hex(a)) + " "
	            d.write(stringtofile + "\n")
	    except KeyboardInterrupt:
	        print "Bye"
	        print map(hex,msg_array)
	        ser.close()
	        d.close()
	        sys.exit()
	
if __name__ == '__main__':
	main()
