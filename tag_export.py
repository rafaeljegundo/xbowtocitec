import OpenOPC
from fcs import conector, destuffed

opc = OpenOPC.client()
opc.connect('Citect.OPC.1')

tagsMapping = {"Humidade":"13:15"} # tag -> index on the msg like 1:2

def updateTags(msg):
    print "Tags hypothetically updated"
    print map(hex,msg)
    msg = msg[1:-1] #Removing 7E
    msg = destuffed(msg) #Destuffing
    msg = msg[6:-2]
    tagsValue = tagsMapping
    print msg[13:15]
    humid_medida= conector(msg[13:15])
    humtemp_medida = conector(msg[15:17])
    humtemp_calc = -38.4 + (0.0098*humtemp_medida)
    hum =(0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + (0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)
    print hum
    print opc.write(('Humidade',int(hum)))
    return
