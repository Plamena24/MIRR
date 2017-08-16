import time
import Grasshopper as gh
import scriptcontext as sc

STEP = sc.sticky
S = "index"

def updateComponent():
    
    """ Updates this component, similar to using a grasshopper timer """
    
    # Define callback action
    def callBack(e):
        ghenv.Component.ExpireSolution(False)
        
    # Get grasshopper document
    ghDoc = ghenv.Component.OnPingDocument()
    
    # Schedule this component to expire
    ghDoc.ScheduleSolution(speed,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack)) # Note that the first input here is how often to update the component (in milliseconds)


# Instantiate/reset persisent starting time variable
if "startTime" not in globals() or Reset:
    startTime = time.time()

eval_list = []
for x in range(1, 1001):
    eval_list.append((1/1000) * x)

if S not in STEP:
    STEP[S] = 0
else:
    if STEP[S] == 999:
        STEP[S] = 0
        t = eval_list[STEP[S]]
    else:
        t = eval_list[STEP[S]]
        print t
        print STEP[S]
        STEP[S] += 1

# Update the component
if start:
    updateComponent()