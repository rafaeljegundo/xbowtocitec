#!/usr/bin/env python
# encoding: utf-8


def calc_crc(crc, b):
	
	crc = crc ^ int(b) << 8;
	
	for i in range(8):
		
		if ((crc & 0x8000) == 0x8000):
			crc = crc << 1 ^ 0x1021
		else:
			crc = crc << 1
	
	return crc & 0xffff
	

def conector(a):
	
	return a[1]*256 + a[0]
	

def destuffed(data):

	a = 0

	while a < len(data)-1:
		if hex(data[a]) == hex(0x7D):
			if hex(data[a+1]) == hex(0x5E):
				data[a] = 0x7E
				data.pop(a+1)
				a += 1
			if hex(data[a+1]) == hex(0x5D):
				data[a] = 0x7D
				data.pop(a+1)
				a += 1
		else:
			a += 1
	return data
	
def crc_test(msg_complete):

	msg =  msg_complete[1:-3] #[0x42, 0x7E, 0x00, 0xFD, 0x7D, 0x02, 0x31, 0x02] # 0xD2C6
		
	msg = destuffed(msg)
	
	crc = 0x0000
	crc_expected = conector(msg_complete[-3:-1])
	
	for b in msg:
		crc = calc_crc(crc,b)

	if hex(crc) == hex(crc_expected):
		print "Valid CRC"
		return True
	else:
		print "UNVALID CRC"
		return False

if __name__ == '__main__':
	
	msg_complete = [0x7E, 0x42, 0x7D, 0x5E, 0x00, 0xFD, 0x7D, 0x5D, 0x02, 0x31, 0x02, 0xC6, 0xD2, 0x7E]
	
	crc_test(msg_complete)
