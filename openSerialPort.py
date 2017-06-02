import serial
import scriptcontext

SCS = scriptcontext.sticky
K = 'serialport'

if K in SCS:
    myPort=SCS[K]
else:
    myPort=serial.Serial()
    
if open == True:
    try:
        myPort.baudrate = baudrate
        myPort.port = port
        myPort.open()
        SCS[K] = myPort
    except:
        print "Something went wrong. Cannot open port."
    if myPort.isOpen() == True:
        print myPort.name + " is open"
        
if open != True:
    try:
        myPort.close()
    except:
        print "Something went wrong. Cannot close port."
    if myPort.isOpen != True:
        print "Port is closed"