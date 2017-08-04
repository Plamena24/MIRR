import rhinoscriptsyntax as rs
from datetime import datetime as dt, timedelta as td
import scriptcontext
import copy

TRACK = scriptcontext.sticky
T = "tick"
TC = "tickcounter"
H = "hold"
HC = "holdcounter"
TR = "triggered_buttons"

#key_list  = (T, TC, H, HC, TR)
#for key in key_list:
#    if key in TRACK:
#        del TRACK[key]

button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_s = td(seconds = 10)
run_interval_us = td(microseconds = 5000)

TRACK[T] = dt.now() + run_interval_us

if TR not in TRACK:
    TRACK[TR] = {}
    TRACK[HC] = {}

def triggered():
    for index, button in enumerate(buttons):
        if button == 1:
            if index not in TRACK[TR]:
                TRACK[TR][index] = dt.now()
            if index not in TRACK[HC]:
                TRACK[HC][index] = 1
            else:
                TRACK[HC][index] += 1
    if TRACK[TR]:
        print TRACK[TR]
    if TRACK[HC]:
        print TRACK[HC]

def hold_action(current_time):
    triggered()
    live_buttons = copy.deepcopy(TRACK[TR])
    for key, time in TRACK[TR].items():
#        print proximity.Branch(key)
#        print abs(time - dt.now()).seconds
#        print (hold_interval_s * TRACK[HC][key]).seconds
        if (abs(time - dt.now()).seconds >= (hold_interval_s * TRACK[HC][key]).seconds):
                live_buttons[proximity.Branch(key)] = dt.now()
                TRACK[HC][key] += 1
                print proximity.Branch(key)
#    TRACK[TR] = live_buttons
#    print TRACK[TR]
#    print TRACK[HC]


#def ticker(current_time):
#   while 1:
#       if (current_time >= TRACK[T]) and (TRACK[TC] < 1000):
#           flipper(TRACK[TC], current_time)
#           TRACK[TC] += 1
#       elif (current_time >= TRACK[T]) and (TRACK[TC] >= 1000):
#           flipper(TRACK[TC], current_time)
#           TRACK[TC] -= 1000
#       else:
#           pass
#
#def flipper(remainder, current_time):
#   flip = hold_action(current_time)
#   for index, button in enumerate(flip):
#       if not flip:
#           if remainder % 2 == 0:
#               button_angles[index] = 1425
#           else:
#               button_angles[index] = 1525
#
#
#
#ticker(dt.now())       

hold_action(dt.now())    
print button_angles
b = button_angles