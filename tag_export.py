from fcs import conector, destuffed
import time
from random import random

try:
	import OpenOPC
	opc = OpenOPC.client()
	opc.connect('Citect.OPC.1')
except:
	print "Can't connect to OPC Server"

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

class Message:
	
	def __init__(self,msg):

		print map(hex,msg)


		msg = msg[1:-1]#Removing 7E

		print map(hex,msg)

                msg = destuffed(msg)#Destuffing
		msg = msg[6:-2]

		print map(hex,msg)

		
                # Humidade

                humid_medida = conector(msg[13:15])
                humtemp_medida = conector(msg[15:17])
                humtemp_calc = -38.4 + (0.0098*humtemp_medida)
                self.humidade =(0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + (0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)

##                humid_medida = conector(msg[13:15])
##                humtemp_medida = conector(msg[15:17])
##                humtemp_calc = -38.4 + (0.0098*humtemp_medida)
##                self.humidade = (0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + (0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)
##		
                # Temperatura
                self.temperatura = -38.4 + (0.0098*humtemp_medida)
		
		self.data = {"Humidade": self.humidade, "Temperatura": self.temperatura}
		
		return
		
		
def updateTags(msg):

	msg = Message(msg)

	print msg.data	
	for tag in msg.data:
		opc.write((tag,int(msg.data[tag])))
                print tag, "written"
                
 	#print "Tags hypothetically updated"
        #print map(hex,msg)
        #msg = msg[1:-1] #Removing 7E
        #msg = destuffed(msg) #Destuffing
        #msg = msg[6:-2]
        #tagsValue = tagsMapping
        #print msg[13:15]
        #humid_medida= conector(msg[13:15])
        #humtemp_medida = conector(msg[15:17])
        #humtemp_calc = -38.4 + (0.0098*humtemp_medida)
        #hum = (0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + (0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)
        #print opc.write(('Humidade',int(hum)))


        return

def main():
	print "testing"
	tagname = 'Humidade' # Alterar para tag do sistema
	tagrange = 100 # Alterar para maximo da tag no sistema
	while True:
		try:
			time.sleep(1)
			hum = random()*tagrange
			print opc.write((tagname,int(hum)))
		except KeyboardInterrupt: 
			print "Bye" 
			break
	pass
	
if __name__ == "__main__": 
	main()
