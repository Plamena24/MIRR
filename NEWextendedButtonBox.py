import rhinoscriptsyntax as rs
from datetime import datetime as dt, timedelta as td
import scriptcontext
import copy

TRACK = scriptcontext.sticky
T = "tick"
TC = "tickcounter"
H = "hold"
P = "panel"
B = "buttons"
A = "angles"

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


class Effect(current_time, triggered):
    def __init__(self):
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
        else:
            if index in TRACK[B]:
                TRACK[B][index] = Effect(dt.now(), False)
            elif TRACK[B][index].end:
                del TRACK[B][index]

def panel_status(current_time):
    if P not in TRACK:
        TRACK[P] = {}
    if TRACK[B]:
        for button, effect in TRACK[B].items():
            if (abs(time - current_time).seconds >= (hold_interval_s * TRACK[HC][key]).seconds):
                for neighbor in proximity.Branch(key):
                    if neighbor not in live_buttons:
                        live_buttons[neighbor] = dt.now()
                    if neighbor not in TRACK[HC]:
                        TRACK[HC][neighbor] = 1
                    else:
                        TRACK[HC][neighbor] += 1



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
     

hold_action(dt.now())    
print button_angles
b = button_angles