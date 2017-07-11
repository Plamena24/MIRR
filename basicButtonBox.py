import rhinoscriptsyntax as rs

button_speeds = 0
button_angles = [1500]*98
a = button_speeds

for index, button in enumerate(buttons):
    if button == 1:
        print index
        if flip == 1:
            button_angles[index] = 1425
        else:
            button_angles[index] = 1525
            
print button_angles
b = button_angles
