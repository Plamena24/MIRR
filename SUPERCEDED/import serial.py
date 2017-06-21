import serial

myPort=serial.Serial()
myPort.baudrate = x
myPort.port = y

'''
if z == True:
    try:
        myPort.open()
    except:
        print "Something went wrong. Cannot open port."
    if myPort.isOpen() == True:
        print myPort.name + " is open"
        
if z != True:
    try:
        myPort.close()
    except:
        print "Something went wrong. Cannot close port."
    if myPort.isOpen != True:
        print myPort.name + " is closed"
        
'''

try:
    myPort.close()
except:
    pass

myPort.open()

#myPort.write(bytearray([0x84, 0x00, 0x70, 0x2E]))
myPort.write(b"\x84\x00\x70\x2E")

myPort.close()