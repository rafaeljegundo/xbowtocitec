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

nodeList = []

class Message:
	
	def __init__(self,msg):

		# Removing 7E: Start and Stop bit
		msg = msg[1:-1]

		# Destuffing message -> Replacing encrypted 7E
        msg = destuffed(msg)
		
		# Removing xmesh Header 
		msg = msg[6:-2]
		
		# Converting data
		
		self.node = conector(msg[2:4])
		print "Confirm node mapping", self.node
		
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
			
		# Pressure
		C1= (conector(msg[17:19]) >> 1)
		C2= (((conector(msg[21:23]) & 0x3F )<< 6)) + (conector(msg[23:25]) & 0x3F)
		C3= (conector(msg[23:25]) >> 6)
		C4= (conector(msg[21:23]) >> 6)
		C5= ((conector(msg[17:19]) & 1) << 10) + (conector(msg[19:21]) >> 6)
		C6= (conector(msg[19:21]) & 0x3F)
		prtemp_medido=conector(msg[25:27])
		pressao_medido=conector(msg[27:29])
		UTI= (8 * C5) + 20224
		dT= prtemp_medido - UTI
		prtemp_calc= (200 + (dT * (C6+50)/float(1024)))/float(10)
		print 'O valor do prtemp e', prtemp_calc,'C'
		OFF= ((C2*4) +(((C4-512)*dT))/float(4096))
		SENS= (C1 + (C3*dT)/float(1024))+ 24576
		X=SENS*((pressao_medido-7168)/float(16384)) - OFF
		print X
		pressao_calc= (X*(100/float(32))+ (250*100))/100
		print 'O valor da pressao e', pressao_calc,'milibar'
		self.pressure = pressao_calc
		
		
		if self.node is not in nodeList:		
			nodeList.append(node)
		else:
			nodeNumber = nodeList.index(self.node)
		
		node = "Node" + str(nodeNumber)
		humidade = "Humidade" + str(nodeNumber)
		temperatura = "Temperatura" + str(nodeNumber)
		luminosidade = "Luminosidade" + str(nodeNumber)
		pressao = "Pressao" + str(nodeNumber)
		
		# To improve: it writes de node in each iteration, without necessity
		
		self.data = {node: self.node, humidade: self.humidade, temperatura: self.temperatura, luminosidade: self.light, pressao: self.pressure}
			
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


"""
To Be Done:

Ler mensagem.
Se nodo é novo -> Mapear, as in Node 1 = xpto432
Se nodo é conhecido -> fazer update a tags respectivas, as in for Node 1, Temp1 = x, Hum1 = y, Lum = z


Also:
permitir usar tags com valores decimais

"""