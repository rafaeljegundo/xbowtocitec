from fcs import conector, destuffed
import time
from random import random

try:
	import OpenOPC
	opc = OpenOPC.client()
	opc.connect('Citect.OPC.1')
except:
	print "Can't connect to OPC Server"

"""
tagsMapping = {	'Voltage':"11:13", \
	'Humidade':"13:15", \
	'humtemp':"15:17", \
	'Cal_word1':"17:19", \
	'Cal_word2':"19:21", \
	'Cal_word3':"21:23", \
	'Cal_word4':"23:25", \
	'prtemp':"25:27", \
	'press':"27:29", \
	'taosch0':"29:31", \
	'taosch1':"31:33", \
	'ax':"33:35", \
	'ay':"35:37" \
	} # tag -> index on the msg like 1:2
"""

class Message:
	
	def __init__(self,msg):

		# Removing 7E: Start and Stop bit
		msg = msg[1:-1]

		# Destuffing message -> Replacing encrypted 7E
        msg = destuffed(msg)

		# Removing xmesh Header
		msg = msg[6:-2]

		# Converting data
		
        # Humidade
		humid_medida = conector(msg[13:15])
		humtemp_medida = conector(msg[15:17])
		humtemp_calc = -38.4 + (0.0098*humtemp_medida)
		self.humidade =(0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + \
		(0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)

		# Temperatura
		self.temperatura = -38.4 + (0.0098*humtemp_medida)

		# Luminosidade
		taosch0_bin=(conector(msg[29:31]))& 0b11111111
		taosch1_bin=(conector(msg[31:33]))& 0b11111111
		v=taosch0_bin & 0b10000000 >>7
		c=taosch0_bin & 0b01110000 >>4
		s=taosch0_bin & 0b00001111
		v1= taosch1_bin & 0b10000000 >>7
		c1= taosch1_bin & 0b01110000 >>4
		s1= taosch1_bin & 0b00001111
		adccount0=(16.5*((2^c)-1))+(s*(2^c))
		adccount1=(16.5*((2^c1)-1))+(s1*(2^c1))
		self.light = (adccount0*0.46*exp(-3.13*(adccount1/adccount0)))
			
		self.data = {"Humidade": self.humidade, "Temperatura": self.temperatura, "Humidade": self.light}
			
		return
		
		
def updateTags(message):

	# Creating message object
	msg = Message(message)

	for tag in msg.data:
		opc.write((tag,int(msg.data[tag])))
                print tag, "written"

	return

def testing():

	print "Testing conversion from raw message to clean data"
	
	testMessage = "0x7e 0x42 0x7d 0x5e 0x0 0xb 0x7d 0x5d 0x25 0x0 0x0 0xbd 0x13 0x0 \
	0x0 0x33 0x85 0x86 0x0 0x0 0xa6 0x1 0x21 0x6 0x2c 0x1a 0xd8 0xb5 0x18 0xf0 0x5e \
	0xa4 0x73 0xba 0x11 0x71 0x9 0x46 0xdb 0xff 0xb2 0xff 0xc1 0x1 0xc1 0x1 0xd6 0xdc 0x7e"
	
	testMessage = testMessage.split(" ")
	
	updateTags(testMessage)
	
	print "Testing writing trough OPC with random values"
	
	tagrange = 60 # Maximum value for testing ALL tags. As integer.
	
	while True:
		try:
			time.sleep(3)
			for a in msg.data:
				testNumber = int(random()*tagrange)
				opc.write((tag,testNumber))
		except KeyboardInterrupt: 
			print "Bye" 
			break
	pass
	
if __name__ == "__main__":
	testing()
