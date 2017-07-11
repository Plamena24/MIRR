import rhinoscriptsyntax as rs
from datetime import datetime as dt, timedelta as td
import scriptcontext

HOLD = scriptcontex.sticky
K = "savedtime"

button_speeds = 0
button_angles = [1500]*98
a = button_speeds
hold_interval_us = td(microseconds = 1500000)
run_interval_us = td(microseconds = 1000)

def triggered():
	triggered_panels = []
	for index, button in enumerate(buttons):		
		if button == 1:
			hold_time_us = dt.now()




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
