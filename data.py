# -*- coding: cp1252 -*-

## Tratamento da msg

from string import split

from fcs import calc_crc

# data = "{7E}{42}{7D}{5E}{00}{0B}{7D}{5D}{25}{00}{00}{A0}{13}{00}{00}{33}{85}{86}{00}{00}{A0}{01}{C9}{05}{02}{18}{E3}{BF}{98}{1F}{5D}{A2}{44}{BE}{F7}{73}{36}{45}{E3}{FF}{BB}{FF}{C1}{01}{C3}{01}{EF}{75}{7E}"

data = "{7E}{42}{7D}{5E}{00}{0B}{7D}{5D}{25}{00}{00}{A4}{13}{00}{00}{33}{85}{86}{00}{00}{98}{01}{84}{06}{4C}{18}{AF}{C7}{98}{07}{9F}{AE}{C8}{C3}{51}{71}{FD}{44}{E2}{FF}{00}{00}{C1}{01}{C3}{01}{2B}{F8}{7E}"

data = split(data[1:len(data)-1],'}{')

data = map (lambda x: '0x' + x, data)

data = map (eval, data)

raw_data = data[:]

## Verificação do 7E

if data[0] == 0x7E:
	print 'valid'
else:
	print "Falta o Start Bit"
  
if data[-1] == 0x7E:
	print 'valid'
else:
	print "Falta o Stop Bit"
	
for a in data[1:-1]:
	if a == 0x7E:
		print "To many 0x7E in the message"

## Destuffing
    
## print map(hex,data)

## Impreciso nos ultimos elementos
print len(data)
print map(hex,data)
while a < len(data): ## for a in range(len(data)-4):
	print a
	if hex(data[a]) == hex(0x7D):
		if hex(data[a+1]) == hex(0x5E):
			data[a] = 0x7E
			data.pop(a+1)
		else:
			a += 1
	else:
		a += 1
	if hex(data[a]) == hex(0x7D):
		if hex(data[a+1]) == hex(0x5D):
			data[a] = 0x7D
			data.pop(a+1)
		else:
			a += 1
	else:
		a += 1

## Confimar CRC

data = data[1:-1]

de_stuff = data[:]

"""
print map(hex,raw_data)
print 
print map(hex,data)
"""

crc = 0x0000;
for b in data[:-2]:
    crc = calc_crc(crc, b);
print hex(crc)

crc_esperado = data[-1]*256 + data[-2]

print hex(crc_esperado)

print map(hex,de_stuff)

length = data[5]

print 'Length is ', hex(length), 'aka', length

xmesh_msg = de_stuff[6:-2]

print map(hex,xmesh_msg) 

def conector(a):
        return a[1]*256 + a[0]

## Esmiúçar o payload

print 'sourceAddr', hex(xmesh_msg[0]), hex(xmesh_msg[1])
print 'originAddr', hex(xmesh_msg[2]), hex(xmesh_msg[3])
print 'seqno', hex(xmesh_msg[4]), hex(xmesh_msg[5])
print 'socket', hex(xmesh_msg[6])
print 'Payload'

tempo = xmesh_msg[7:11]
tempo.reverse()

print 'Sensor Board ID', xmesh_msg[7]
print 'Sensor Packet ID', xmesh_msg[8]
print 'Parent', conector(xmesh_msg[9:11])
print 'Voltage', conector(xmesh_msg[11:13])
print 'humidade', conector(xmesh_msg[13:15])
print 'humtemp', conector(xmesh_msg[15:17])
print 'Cal_word1', conector(xmesh_msg[17:19])
print 'Cal_word2', conector(xmesh_msg[19:21])
print 'Cal_word3', conector(xmesh_msg[21:23])
print 'Cal_word4', conector(xmesh_msg[23:25])
print 'prtemp', xmesh_msg[26]
print 'press', xmesh_msg[27]
print 'taosch0', xmesh_msg[28]
print 'taosch1', xmesh_msg[29]
print 'ax', xmesh_msg[30]
print 'ay', xmesh_msg[31]

"""

Voltage no 3º par do payload

"""

"""
ValidaÃ§Ã£o
    ComeÃ§a em 7E
    Acaba em 7E
    Confirmar length
    Confimar CRC
    
"""
