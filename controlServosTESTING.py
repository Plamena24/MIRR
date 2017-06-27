import serial
import scriptcontext
import base64

myPort = scriptcontext.sticky['serialport']
myPort.flushInput()
myPort.flushOutput()

ghSpeedsList = []
board0speeds = []
board1speeds = []
board2speeds = []
board3speeds = []
board4speeds = []

ghTargetsList = []
board0targets = []
board1targets = []
board2targets = []
board3targets = []
board4targets = []

print speed_val
print angle_us1

class Controller:
    
    def __init__(self, device_number = 0x00):
        # Define the object as the already open port
        self.usb = myPort
        # Command lead-in and device number are sent for each Pololu serial commands.
        self.PololuCmd = [0xaa, device_number]
     
    def setTargets(self, num_targets, start_chan = 0x00, *targets):

        pairList = list(targets)
        valueList = []
        cmdSplitList = []

        for pair in pairList:
            valueList.append(pair[1])
        #print valueList

        qValueList = [us*4 for us in valueList]
        #print qValueList

        for value in qValueList:
            lsb = value & 0x7f #7 bits for least significant byte
            msb = (value >> 7) & 0x7f #shift 7 and take next 7 bits for msb
            cmdSplitList.append(lsb)
            cmdSplitList.append(msb)
        #print cmdSplitList

        # Send Pololu intro, device number, multiple targets command, number of targets, start channel, and targets lsb/msb
        multi_target_cmd = [0x1F, num_targets, start_chan]
        cmd_intro = self.PololuCmd + multi_target_cmd
        cmd = cmd_intro + cmdSplitList
        #print cmd
        return cmd
        # self.usb.write(bytes(bytearray(cmd)))
        # myPort.write(bytes(bytearray(cmd)))
        # # Record Target value
        # self.Targets[chan] = target
        
    # Set speeds for all used channels on each board
    # Speed is measured as 0.25microseconds/10milliseconds
    # For the standard 1ms pulse width change to move a servo between extremes, a speed
    # of 1 will take 1 minute, and a speed of 60 would take 1 second.
    # Speed of 0 is unrestricted.
    def setSpeeds(self, *speeds):
        
        pairList = list(speeds)
        valueList = []
        cmdSplitList = []
        speed_cmd = []

        for pair in pairList:
            valueList.append(pair[1])
        #print valueList

        qValueList = [us*4 for us in valueList]

        # Send Pololu intro, device number, command, channel, and target lsb/msb
        for chan, value in enumerate(qValueList):
            lsb = value & 0x7f #7 bits for least significant byte
            msb = (value >> 7) & 0x7f #shift 7 and take next 7 bits for msb
            set_speed_cmd = [0x07, chan, lsb, msb]
            cmd = self.PololuCmd + set_speed_cmd
            speed_cmd = speed_cmd + cmd
        # print speed_cmd
        return speed_cmd
            # print cmd

            # self.usb.write(bytes(bytearray(cmd)))
            # myPort.write(bytes(bytearray(cmd)))
        

    # Set acceleration of channel
    # This provide soft starts and finishes when servo moves to target position.
    # Valid values are from 0 to 255. 0=unrestricted, 1 is slowest start.
    # A value of 1 will take the servo about 3s to move between 1ms to 2ms range.
    def setAccel(self, chan, accel):
        pass
        # lsb = accel & 0x7f #7 bits for least significant byte
        # msb = (accel >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        # # Send Pololu intro, device number, command, channel, accel lsb, accel msb
        # cmd = self.PololuCmd + chr(0x09) + chr(chan) + chr(lsb) + chr(msb)
        # self.usb.write(bytes(bytearray(cmd)))
    

    def getMovingState(self):
        intro_cmd = self.PololuCmd
        moving = [0x13]
        cmd = intro_cmd + moving
        # print cmd
        self.usb.write(bytes(bytearray(cmd)))
        # myPort.write(bytes(bytearray(cmd)))
        # workaround to make the speed and target assignment to run since the reads are not returning anything
        # return False
        response = self.usb.read()
        # response = myPort.read()
        print (base64.b16encode(response) + "\n")
        if response == chr(0):
            return False
        else:
            return True

# the parsing functions create the arrays of speeds and targets used for each board
# both functions take a list of 98 values which is the number of servos used in the project
# in the full version of the program the lists are generated dynamically - target values for the 98 servos will generally be all different, speeds may or may not be different
def parseSpeeds(*ghSpeeds):
    global ghSpeedsList, board0speeds, board1speeds, board2speeds, board3speeds, board4speeds
    parsedSpeeds = [0]*2

    ghSpeedsList = list(ghSpeeds)
    #print ghSpeedsList
    board0speeds = []
    board1speeds = []
    board2speeds = []
    board3speeds = []
    board4speeds = []
    
    for index, speed in enumerate(ghSpeedsList):
        if index < 20:
            parsedSpeeds[0] = 0x00
            parsedSpeeds[1] = speed
            board0speeds.append(parsedSpeeds)
            #print board0speeds
        elif index > 19 and index < 39:
            parsedSpeeds[0] = 0x01
            parsedSpeeds[1] = speed
            board1speeds.append(parsedSpeeds)
        elif index > 38 and index < 59:
            parsedSpeeds[0] = 0x02
            parsedSpeeds[1] = speed
            board2speeds.append(parsedSpeeds)
        elif index > 58 and index < 78:
            parsedSpeeds[0] = 0x03
            parsedSpeeds[1] = speed
            board3speeds.append(parsedSpeeds)
        elif index > 77 and index < 98:
            parsedSpeeds[0] = 0x04
            parsedSpeeds[1] = speed
            board4speeds.append(parsedSpeeds)
        else:
            print "Invalid speed index."

def parseTargets(*ghTargets):
    global ghTargetsList, board0targets, board1targets, board2targets, board3targets, board4targets
    parsedTargets = [0]*2

    ghTargetsList = list(ghTargets)
    print ghTargetsList
    board0targets = []
    board1targets = []
    board2targets = []
    board3targets = []
    board4targets = []
    print board0targets
    print board1targets
    print board2targets
    print board3targets
    print board4targets
    
    for index, target in enumerate(ghTargetsList):
        if index < 20:
            print index, target
#            parsedTargets[0] = 0x00
#            parsedTargets[1] = target
#            print parsedTargets
            board0targets.append(target)
            print board0targets
        elif index > 19 and index < 39:
            print index, target
            parsedTargets[0] = 0x01
            parsedTargets[1] = target
            print parsedTargets
            board1targets.append(parsedTargets)
            print board1targets
        elif index > 38 and index < 59:
            print index, target
            parsedTargets[0] = 0x02
            parsedTargets[1] = target
            print parsedTargets
            board2targets.append(parsedTargets)
            print board2targets
        elif index > 58 and index < 78:
            print index, target
            parsedTargets[0] = 0x03
            parsedTargets[1] = target
            print parsedTargets
            board3targets.append(parsedTargets)
            print board3targets
        elif index > 77 and index < 98:
            print index, target
            parsedTargets[0] = 0x04
            parsedTargets[1] = target
            print parsedTargets
            board4targets.append(parsedTargets)
            print board4targets
        else:
            print "Invalid target index."
    print board0targets
    print board1targets
    print board2targets
    print board3targets
    print board4targets

def movingState():
    moving_state0 = board0.getMovingState()
    moving_state1 = board1.getMovingState()
    moving_state2 = board2.getMovingState()
    moving_state3 = board3.getMovingState()
    moving_state4 = board4.getMovingState()

    if moving_state0 is False and \
       moving_state1 is False and \
       moving_state2 is False and \
       moving_state3 is False and \
       moving_state4 is False:
        return False
    else:
        return True


def setBoards():
    parseSpeeds(*speed_val)
    parseTargets(*angle_us1)
    
    speeds0 = board0.setSpeeds(*board0speeds)
    speeds1 = board1.setSpeeds(*board1speeds)
    speeds2 = board2.setSpeeds(*board2speeds)
    speeds3 = board3.setSpeeds(*board3speeds)
    speeds4 = board4.setSpeeds(*board4speeds)
          
    targets0 = board0.setTargets(0x14, 0x00,*board0targets)
    targets1 = board1.setTargets(0x13, 0x00,*board1targets)
    targets2 = board2.setTargets(0x14, 0x00,*board2targets) 
    targets3 = board3.setTargets(0x13, 0x00,*board3targets)
    targets4 = board4.setTargets(0x14, 0x00,*board4targets)

    # if movingState() == False:
    #     full_cmd = speeds0 + speeds1 + speeds2 + speeds3 + speeds4 + \
    #                targets0 + targets1 + targets2 + targets3 + targets4
    #     # print full_cmd
    #     myPort.write(bytes(bytearray(full_cmd)))
    #     print "Moving servos"
    # else:
    #     print "There are servos still moving."
    full_cmd = speeds0 + speeds1 + speeds2 + speeds3 + speeds4 + \
               targets0 + targets1 + targets2 + targets3 + targets4
    myPort.write(bytes(bytearray(full_cmd)))
    print full_cmd
    print "Moving servos"
        
def goHome():
    speed_val = []
    angle_us1 = []

    speed_val = [6]*98
    angle_us1= [1500]*98
    
    parseSpeeds(*speed_val)
    parseTargets(*angle_us1)

    speeds0 = board0.setSpeeds(*board0speeds)
    speeds1 = board1.setSpeeds(*board1speeds)
    speeds2 = board2.setSpeeds(*board2speeds)
    speeds3 = board3.setSpeeds(*board3speeds)
    speeds4 = board4.setSpeeds(*board4speeds)
          
    targets0 = board0.setTargets(0x14, 0x00,*board0targets)
    targets1 = board1.setTargets(0x13, 0x00,*board1targets)
    targets2 = board2.setTargets(0x14, 0x00,*board2targets) 
    targets3 = board3.setTargets(0x13, 0x00,*board3targets)
    targets4 = board4.setTargets(0x14, 0x00,*board4targets)

    full_cmd = speeds0 + speeds1 + speeds2 + speeds3 + speeds4 + \
               targets0 + targets1 + targets2 + targets3 + targets4
    # print full_cmd
    myPort.write(bytes(bytearray(full_cmd)))
    print "Homing"

def power_off(off_value):
    while movingState() == True:
        print "Waiting to go home."
    else:   
        print "Shutting servos off"
        trigger = off_value * 4
        lsb = trigger & 0x7f #7 bits for least significant byte
        msb = (trigger >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        switch1 = [0xAA, 0x01, 0x04, 0x17, lsb, msb]
        switch2 = [0xAA, 0x03, 0x04, 0x17, lsb, msb]
        off_cmd = switch1 + switch2
        print off_cmd
        myPort.write(bytes(bytearray(off_cmd)))

def power_on(on_value):
    print "Power on"
    trigger = on_value * 4
    lsb = trigger & 0x7f #7 bits for least significant byte
    msb = (trigger >> 7) & 0x7f #shift 7 and take next 7 bits for msb
    switch1 = [0xAA, 0x01, 0x04, 0x17, lsb, msb]
    switch2 = [0xAA, 0x03, 0x04, 0x17, lsb, msb]
    on_cmd = switch1 + switch2
    print on_cmd
    myPort.write(bytes(bytearray(on_cmd)))


board0 = Controller(0x00)
board1 = Controller(0x01)
board2 = Controller(0x02)
board3 = Controller(0x03)
board4 = Controller(0x04)

if boards_off == 1:
    goHome()
    power_off(2000)
else:
    power_on(1000)
    #goHome()
    setBoards()
    
    
    