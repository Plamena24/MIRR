import rhinoscriptsyntax as rs
from datetime import datetime as dt, timedelta as td
import scriptcontext

TRACK = scriptcontext.sticky
T = "tick"
TC = "tickcounter"
H = "hold"
HC = "holdcounter"
TR = "triggered_buttons"

button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_us = td(seconds = 2)
run_interval_us = td(microseconds = 5000)

TRACK[T] = dt.now() + run_interval_us

def triggered():
    for index, button in enumerate(buttons):
        if (button == 1):
            TRACK[TR] = [index]
            TRACK[H] = dt.now() + hold_interval_us
            TRACK[HC] += 1
        else:
            TRACK[TR] = []
            TRACK[H] = dt.now()
            TRACK[HC] = 0
    print TRACK[TR]
    print TRACK[H]
    print TRACK[HC]

def hold_action(current_time):
    triggered()
    live_buttons = list(TRACK[TR])
    if (current_time >= TRACK[H]) and (TRACK[HC] > 0):
        print "Next round"
        for count in range(TRACK[HC]):
            for button in TRACK[TR]:
                live_buttons.append(proximity.Branch(*button))
                print proximity.Branch(button)
            TRACK[TR].append(*live_buttons)
            print TRACK[TR]


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