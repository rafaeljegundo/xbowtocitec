# -*- coding: utf-8 -*-

"""
Code for testing crc, destuffing and data conversion to engineering units

"""

from string import split
from fcs import calc_crc, conector, destuffed, crc_test

"""
data is the captured message. Example: {7E}{42}{7D}{5E}{00}{0B}{7D}{5D}{25}{00}{00}{A4}{13}{00}{00}{33}{85}{86}
{00}{00}{98}{01}{84}{06}{4C}{18}{AF}{C7}{98}{07}{9F}{AE}{C8}{C3}{51}{71}{FD}{44}
{E2}{FF}{00}{00}{C1}{01}{C3}{01}{2B}{F8}{7E}
"""

data = "{7E}{42}{7D}{5E}{00}{0B}{7D}{5D}{25}{00}{00}{9A}{13}{00}{00}{33}{85}{86}{00}{00}{94}{01}\
{47}{06}{3E}{1A}{B0}{B5}{98}{D1}{61}{AF}{3B}{BA}{54}{6D}{18}{47}{DE}{FF}{B8}{FF}{C1}{01}{C2}{01}{5D}{81}{7E}"
# Converting the string to a more treatable format

data = split(data[1:len(data)-1],'}{')

data = map (lambda x: '0x' + x, data)

data = map (eval, data)

## Verifing initial and final 0x7E

if data[0] == 0x7E:
	pass
else:
	print "Falta o Start Bit"
  
if data[-1] == 0x7E:
	pass
else:
	print "Falta o Stop Bit"
	
for a in data[1:-1]:
	if a == 0x7E:
		print "To many 0x7E in the message"

## Validating CRC

print crc_test(data)

# Removing Start and Stop Bit

data = data[1:-1]


## Destuffing

data = destuffed(data)

length = data[5]

print 'Length is', length

## Filtering content by removing the tinyOS Header

xmesh_msg = data[6:-2]

## Printing out the payload -> Convert to dictionary

print 'Multihop Header'
print 'sourceAddr', hex(xmesh_msg[0]), hex(xmesh_msg[1])
print 'originAddr', hex(xmesh_msg[2]), hex(xmesh_msg[3])
print 'seqno', hex(xmesh_msg[4]), hex(xmesh_msg[5])
print 'socket', hex(xmesh_msg[6])
print 'Sensor Header'
print 'Sensor Board ID', xmesh_msg[7] 
print 'Sensor Packet ID', xmesh_msg[8]
print 'Parent', conector(xmesh_msg[9:11])
print 'Data Payload'
print 'Voltage', conector(xmesh_msg[11:13]) 
print 'humidade', conector(xmesh_msg[13:15])
print 'humtemp', conector(xmesh_msg[15:17])
print 'Cal_word1', conector(xmesh_msg[17:19])
print 'Cal_word2', conector(xmesh_msg[19:21])
print 'Cal_word3', conector(xmesh_msg[21:23])
print 'Cal_word4', conector(xmesh_msg[23:25])
print 'prtemp', conector(xmesh_msg[25:27])
print 'press', conector(xmesh_msg[27:29])
print 'taosch0', conector(xmesh_msg[29:31])
print 'taosch1', conector(xmesh_msg[31:33])
print 'ax', conector(xmesh_msg[33:35])
print 'ay', conector(xmesh_msg[35:37])



## Converting payload data to real-world units

print
print 'Converting payload data to real-world units'
print

## Voltage

valortensaomedido=conector(xmesh_msg[11:13]) 
BV_calc=0
BV_calc= 1252.352 / valortensaomedido
print 'O valor da bateria e',BV_calc, 'Volts'

##CALCULO DA HUMIDADE E TEMPERATURA
humid_medida= conector(xmesh_msg[13:15])
humtemp_medida = conector(xmesh_msg[15:17])
humtemp_calc = -38.4 + (0.0098*humtemp_medida)
print 'O valor da temperatura e', humtemp_calc,'C'
humid_calc=(0.0098 * humtemp_medida - 63.4)*(0.01+0.00008*humid_medida)-4 + (0.0405*humid_medida) - (0.0000028*humid_medida*humid_medida)
print 'O valor da humidade e', humid_calc,'%'

## CALCULO DOS VALORES DA ACELERACAO ( X e Y)
valormedido_x=conector(xmesh_msg[33:35])
valormedido_y=conector(xmesh_msg[35:37])
aceleracao_x= 1- ((500-valormedido_x)/float(50))
print 'O valor da aceleracao segundo o eixo do x e', aceleracao_x,'g'
aceleracao_y= 1-((500 - valormedido_y)/float(50))
print 'O valor da aceleracao segundo o eixo do x e', aceleracao_y,'g'

## CALCULO DA PRESSAO E DO PRTEMP
C1= (conector(xmesh_msg[17:19]) >> 1)
C2= (((conector(xmesh_msg[21:23]) & 0x3F )<< 6)) + (conector(xmesh_msg[23:25]) & 0x3F)
C3= (conector(xmesh_msg[23:25]) >> 6)
C4= (conector(xmesh_msg[21:23]) >> 6)
C5= ((conector(xmesh_msg[17:19]) & 1) << 10) + (conector(xmesh_msg[19:21]) >> 6)
C6= (conector(xmesh_msg[19:21]) & 0x3F)
prtemp_medido=conector(xmesh_msg[25:27])
pressao_medido=conector(xmesh_msg[27:29])
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


## Luminosity

taosch0_bin=(conector(xmesh_msg[29:31]))& 0b11111111
taosch1_bin=(conector(xmesh_msg[31:33]))& 0b11111111
taosch0_bin_0=taosch0_bin & 0xFF
taosch1_bin_1=taosch1_bin & 0xFF
v0 = (taosch0_bin_0 & 0b10000000) >>7
c0 = (taosch0_bin_0 & 0b01110000) >>4
s0 = (taosch0_bin_0 & 0b00001111)
v1 = (taosch1_bin_1 & 0b10000000) >>7
c1 = (taosch1_bin_1 & 0b01110000) >>4
s1 = (taosch1_bin_1 & 0b00001111)
adccount0 = 16.5*((pow(2,c0)-1))+(s0*(pow(2,c0)))
adccount1 = 16.5*((pow(2,c1)-1))+(s1*(pow(2,c1)))
exponencial=exp(-3.13*(adccount1/adccount0))
lightlevel = (adccount0*0.46*exponencial)
print lightlevel, "Lumens"
