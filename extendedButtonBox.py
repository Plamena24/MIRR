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


button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_s = td(seconds = 2)
run_interval_us = td(microseconds = 5000)

TRACK[T] = dt.now() + run_interval_us

def triggered():
    for index, button in enumerate(buttons):
        if TR not in TRACK:
            TRACK[TR] = {}
            TRACK[TC] = {}
            if button == 1:
                TRACK[TR][index] = dt.now()
                TRACK[HC][index] += 1
        elif TR in TRACK:
            if (button == 1) and (index not in TRACK[TR].keys()):
                TRACK[TR][index] = dt.now()
                TRACK[HC][index] += 1
    if TRACK[TR]:
        print TRACK[TR]
    if TRACK[HC]:
        print TRACK[HC]

def hold_action(current_time):
    triggered()
    live_buttons = copy.deepcopy(triggered_buttons)
    for key, time in triggered_buttons.items():
        if ((time - dt.now()) >= (hold_interval_s * hold_counter[key])) and (key not in triggered_buttons):
                live_buttons[proximity.Branch(*key)] = dt.now()
                hold_counter[key] += 1
                print proximity.Branch(key)
    print live_buttons
    print hold_counter


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