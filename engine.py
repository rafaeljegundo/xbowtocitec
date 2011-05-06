import usb_import
import tag_export
from sys import exit
from fcs import crc_test

#Requires OpenOPC, pywin32, pyserial, citect >7, gateway USB drivers
f = open('msg_log.txt','w')

def getMessage():
    while True:
        b = usb_import.ser.read(1)
        if b == '\x7E':
            msg = usb_import.decode(usb_import.listen(b))
            return msg

def writeToLog(msg):
    f.write(str(map(hex,msg)) + '\n')
    return

def stopLog():
    f.close()
    return

while True:
    print "+1 Loop"
    try:
        msg = getMessage()
        print msg
        if len(msg) > 15 and crc_test(msg):
            writeToLog(msg)
            tag_export.updateTags(msg)
            print msg
            stopLog()
            break
    except KeyboardInterrupt:
        print "Bye"
   #     stopListening()
        stopLog()
        exit()
    
