import usb_import
import tag_export
from sys import exit
from fcs import crc_test

f = open('msg_log.txt','w')
        
def writeToLog(msg):
	
    f.write(str(map(hex,msg)) + '\n')
    
	return

def stop():
        f.close()
        usb_import.ser.close()
        return

def getMessage():
        while True:
                b = usb_import.ser.read(1)
                if b == '\x7E':
                        msg = usb_import.decode(usb_import.listen(b))
                        return msg
                else:
                        continue
                                
def main():
        while True:
            try:
				rawmsg = msg[:]
                msg = getMessage()
                if crc_test(msg):
                        msg = tag_export.Message(msg)
                        if msg.tipe == "normal":
                            tag_export.updateTags(msg)
							writeToLog(rawmsg)
            except KeyboardInterrupt:
                print "Bye"
                stop()
                exit()
        
if __name__ == '__main__':
        main()
    
