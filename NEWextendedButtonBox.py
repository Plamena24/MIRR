import grasshopper as gh
from datetime import datetime as dt, timedelta as td
import scriptcontext
import copy

TRACK = scriptcontext.sticky
P = "panel"
B = "buttons"
S = "status"
T = "tick"

#key_list  = (T, TC, H, HC, TR)
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
            elif TRACK[B][index].end != None:
                TRACK[B][index] = Effect(dt.now(), True)
                TRACK[B][index] = None
        else:
            if TRACK[B][index].start != None:
                TRACK[B][index] = Effect(dt.now(), False)
                TRACK[B][index].start = None

def button_trigger(current_time):
    if P not in TRACK:
        TRACK[P] = {}
        for value in range(0, 98):
            TRACK[P][value] = 0
    if TRACK[B]:
        for key, effect in TRACK[B].items():
            if (abs(effect - current_time)).seconds % hold_interval_s.seconds == 0:
                if TRACK[B][key].start != None:  
                    TRACK[P][key] = TRACK[B][key]
                    panel_trigger(True)
                elif TRACK[B][key].end != None:
                    panel_trigger(False, key)

def panel_trigger(start, key = None):
    if start:
        for panel in TRACK[P]:
            for neighbor in proximity.Branch(panel):
                TRACK[P][neighbor] = current_time
    else: 
        for panel, effect in TRACK[P].items():
            if (abs(effect - TRACK[B][key])).seconds == hold_interval_s.seconds:
                TRACK[P][panel] = None
                TRACK[B][key] = effect

def panel_status():
    if S not in TRACK:
        TRACK[S] = [0]*98
    else:
        for panel, status in TRACK[P].items():
            if status != None:
                TRACK[S][panel] = 1

def set_angles():
    for index, status in enumerate(TRACK[S]):
        if status == 1:
            button_angles[index] = flip_angle()

def flip_angle():
    pass
    #return new_angle 

def ticker():
    pass

# def flipper(remainder, current_time):
#   flip = hold_action(current_time)
#   for index, button in enumerate(flip):
#       if not flip:
#           if remainder % 2 == 0:
#               button_angles[index] = 1425
#           else:
#               button_angles[index] = 1525

     

hold_action(dt.now())    
print button_angles
b = button_angles