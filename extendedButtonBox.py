import rhinoscriptsyntax as rs
from datetime import datetime as dt, timedelta as td
import scriptcontext

TRACK = scriptcontex.sticky
T = "tick"
H = "hold"
C = "holdcounter"

button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_us = td(microseconds = 1500000)
run_interval_us = td(microseconds = 5000)

TRACK[T] = dt.now()

def triggered():
    triggered_buttons = []
	for index, button in enumerate(buttons):		
		if button == 1:
            if index in triggered_buttons:
                pass
            else:
                triggered_buttons.append(index)
			TRACK[H] = dt.now() + hold_interval_us
            TRACK[C] += 1
        else:
            TRACK[C] = 0
    return triggered_buttons

def hold_action(current_time):
    if (current_time >= TRACK[H]) and (TRACK[C] > 0):





for index, button in enumerate(buttons):
	hold_time_s = time.time()
    if button == 1:
    	hold_time_s += hold_interval_s
        print index
        if flip == 1:
            button_angles[index] = 1425
        else:
            button_angles[index] = 1525
    elif button == 1 and time.time() >= hold_time_s:

            
print button_angles
b = button_angles
 