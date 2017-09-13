from datetime import datetime as dt, timedelta as td
import scriptcontext
import copy
import Grasshopper as gh

TRACK = scriptcontext.sticky
P = "panel"
B = "buttons"
S = "status"
T = "tick"

#key_list  = (P, B, S, T)
#for key in key_list:
#    if key in TRACK:
#        del TRACK[key]

button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_s = td(seconds = 10)


def updateComponent():
    
    """ Updates this component, similar to using a grasshopper timer """
    
    # Define callback action
    def callBack(e):
        ghenv.Component.ExpireSolution(False)
        
    # Get grasshopper document
    ghDoc = ghenv.Component.OnPingDocument()
    
    # Schedule this component to expire
    ghDoc.ScheduleSolution(update_frequency,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack)) # Note that the first input here is how often to update the component (in milliseconds)

# Instantiate/reset persisent starting time variable
if "startTime" not in globals() or Reset:
    startTime = dt.now()

class Effect:
    def __init__(self, current_time, triggered):
        self.start = None
        self.end = None
        if triggered:
            self.start = current_time
        else:
            self.end = current_time

def button_status():
    if B not in TRACK:
        TRACK[B] = {}
    for index, button in enumerate(buttons):
        if button == 1:
            if index not in TRACK[B]:
                TRACK[B][index] = Effect(dt.now(), True)
            #elif TRACK[B][index].start != None:
                #print TRACK[B][index].start
            elif TRACK[B][index].end != None:
                del TRACK[B][index] 
        else:
            if index not in TRACK[B]:
                pass
            elif TRACK[B][index].start != None:
                TRACK[B][index] = Effect(dt.now(), False)
                TRACK[B][index].start = None

def button_trigger(current_time):
    if P not in TRACK:
        TRACK[P] = {}
        for value in range(0, 98):
            TRACK[P][value] = None
    if TRACK[B]:
        for key, effect in TRACK[B].items():
            #print effect.start, "Start timestamp"
            if effect.start != None: 
                if (abs(effect.start - current_time)).seconds % hold_interval_s.seconds == 0:
                    TRACK[P][key] = effect.start
                    panel_trigger(True, current_time, key)
            elif effect.end != None:
                #if (abs(effect.end - current_time)).seconds % hold_interval_s.seconds == 0:
                    #print effect.end, "End timestamp"
                panel_trigger(False, current_time, key)
#        print TRACK[B]
#        print TRACK[P]

def panel_trigger(start, time, key = None):
    if start:
        for panel, timestamp in TRACK[P].items():
            if timestamp != None:
                for neighbor in proximity.Branch(panel):
                    if TRACK[P][neighbor] == None:
                        TRACK[P][neighbor] = time
    else: 
        #print TRACK[B][key].end
        for panel, timestamp in TRACK[P].items():
            #print timestamp, "panel trigger end"
            #print TRACK[B][key].end
            print timestamp
            if timestamp != None:
                #print "Timestamp is not None"
                #print timestamp, TRACK[B][key].end
                print (abs(timestamp - TRACK[B][key].end)).seconds
                if (abs(timestamp - TRACK[B][key].end)).seconds >= hold_interval_s.seconds:
                    print "Ending"
                    TRACK[B][key].end = timestamp
                    TRACK[P][panel] = None
        #print TRACK[P]
                    
 
def panel_status():
    if S not in TRACK:
        TRACK[S] = [0]*98
    else:
        for panel, status in TRACK[P].items():
            if status != None:
                TRACK[S][panel] = 1
    print TRACK[S]

def set_angles():
    for index, status in enumerate(TRACK[S]):
        if status == 1:
            button_angles[index] = flip_angle(TRACK[T])
        #print button_angles

def flip_angle(tick):
    new_angle = 1500
    if tick % 2 == 0:
        new_angle = 1425
    else:
        new_angle = 1525
    return new_angle

def ticker():
    if T not in TRACK:
        TRACK[T] = 0
    else:
        if TRACK[T] == 999:
            TRACK[T] = 0
        else:
            TRACK[T] += 1
ticker()
button_status()
button_trigger(dt.now())
panel_status()
set_angles()

print TRACK[T]
print button_angles
b = button_angles

# Update the component
if start:
    updateComponent()




