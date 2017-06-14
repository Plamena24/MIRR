import serial
import scriptcontext
myPort = scriptcontext.sticky['serialport']
myPort.flushInput()
myPort.flushOutput()

# out_bytes = [0xAA, 0x00, 0x07, 0x00, None, None, 0xAA, 0x00, 0x07, 0x01, None, None, 0xAA, 0x00, 0x1F, 0x02, 0x00, None, None, None, None]
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

def parseSpeeds(*ghSpeeds):
    global ghSpeedsList, board0speeds, board1speeds, board2speeds, board3speeds, board4speeds
    parsedSpeeds = [0]*2

    ghSpeedsList = list(ghSpeeds)
    print ghSpeedssList

    for index, speed in enumerate(ghSpeedsList):
        if index < 20:
            parsedSpeeds[0] = 0x00
            parsedSpeeds[1] = speed
            board0speeds.append(parsedSpeeds)
            print board0speeds
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
            parsedSpeed[0] = 0x04
            parsedSpeed[1] = speed
            board4speeds.append(parsedSpeeds)
        else:
            print "Invalid target index"

def parseTargets(*ghTargets):
    global ghTargetsList, board0targets, board1targets, board2targets, board3targets, board4targets
    parsedTargets = [0]*2

    ghTargetsList = list(ghTargets)
    print ghTargetsList

    for index, target in enumerate(ghTargetsList):
        if index < 20:
            parsedTargets[0] = 0x00
            parsedTargets[1] = target
            board0targets.append(parsedTargets)
            print board0targets
        elif index > 19 and index < 39:
            parsedTargets[0] = 0x01
            parsedTargets[1] = target
            board1targets.append(parsedTargets)
        elif index > 38 and index < 59:
            parsedTargets[0] = 0x02
            parsedTargets[1] = target
            board2targets.append(parsedTargets)
        elif index > 58 and index < 78:
            parsedTargets[0] = 0x03
            parsedTargets[1] = target
            board3targets.append(parsedTargets)
        elif index > 77 and index < 98:
            parsedTargets[0] = 0x04
            parsedTargets[1] = target
            board4targets.append(parsedTargets)
        else:
            print "Invalid target index"



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
        print valueList

        qValueList = [us*4 for us in valueList]
        print qValueList

        for value in qValueList:
            lsb = value & 0x7f #7 bits for least significant byte
            msb = (value >> 7) & 0x7f #shift 7 and take next 7 bits for msb
            cmdSplitList.append(lsb)
            cmdSplitList.append(msb)
        print cmdSplitList

        # Send Pololu intro, device number, command, channel, and target lsb/msb
        multi_target_cmd = [0x1F, num_targets, start_chan]
        cmd_intro = self.PololuCmd + multi_target_cmd
        cmd = cmd_intro + cmdSplitList
        print cmd

        self.usb.write(bytes(bytearray(cmd)))
        # # Record Target value
        # self.Targets[chan] = target
        
    # Set speed of channel
    # Speed is measured as 0.25microseconds/10milliseconds
    # For the standard 1ms pulse width change to move a servo between extremes, a speed
    # of 1 will take 1 minute, and a speed of 60 would take 1 second.
    # Speed of 0 is unrestricted.
    def setSpeed(self, *speeds):
        
        pairList = list(speeds)
        valueList = []
        cmdSplitList = []

        for pair in pairList:
            valueList.append(pair[1])
        print valueList

        qValueList = [us*4 for us in valueList]
        print qValueList

        # for value in qValueList:
        #     lsb = value & 0x7f #7 bits for least significant byte
        #     msb = (value >> 7) & 0x7f #shift 7 and take next 7 bits for msb
        #     cmdSplitList.append(lsb)
        #     cmdSplitList.append(msb)
        # print cmdSplitList

        # Send Pololu intro, device number, command, channel, and target lsb/msb
        for chan, value in enumerate(qValueList):
            lsb = value & 0x7f #7 bits for least significant byte
            msb = (value >> 7) & 0x7f #shift 7 and take next 7 bits for msb
            set_speed_cmd = [0x07, chan, lsb, msb]
            cmd = self.PololuCmd + set_speed_cmd
            print cmd

            self.usb.write(bytes(bytearray(cmd)))
        

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
        pass
        # cmd = self.PololuCmd + chr(0x13)
        # self.usb.write(cmd)
        # if self.usb.read() == chr(0):
        #     return False
        # else:
        #     return True

# speed = speed_val * 4
# out_bytes[4] = speed & 0x7F #Second byte holds the lower 7 bits of speed.
# out_bytes[5] = (speed >> 7) & 0x7F # Third data byte holds the bits 7-13 of speed.
# out_bytes[10] = speed & 0x7F #Second byte holds the lower 7 bits of speed.
# out_bytes[11] = (speed >> 7) & 0x7F # Third data byte holds the bits 7-13 of speed.

# target1 = angle_us1 * 4
# target2 = angle_us2 * 4
# out_bytes[17] = target1 & 0x7F #Second byte holds the lower 7 bits of target.
# out_bytes[18] = (target1 >> 7) & 0x7F # Third data byte holds the bits 7-13 of target.
# out_bytes[19] = target2 & 0x7F #Second byte holds the lower 7 bits of target.
# out_bytes[20] = (target2 >> 7) & 0x7F # Third data byte holds the bits 7-13 of target.

# print out_bytes
# myPort.write(bytes(bytearray(out_bytes)))
board0 = Controller(0x00)
parseSpeeds(*speed_val)
parseTargets(*angle_us1)
board0.setSpeeds(*board0speeds)
board0.setTargets(0x62, 0x00,*board0targets)

