import time
import Grasshopper as gh
import scriptcontext as sc

STEP = sc.sticky
S = "next_step"
V = "next_value"

def updateComponent():
    
    """ Updates this component, similar to using a grasshopper timer """
    
    # Define callback action
    def callBack(e):
        ghenv.Component.ExpireSolution(False)
        
    # Get grasshopper document
    ghDoc = ghenv.Component.OnPingDocument()
    
    # Schedule this component to expire
    ghDoc.ScheduleSolution(100,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack)) # Note that the first input here is how often to update the component (in milliseconds)


# Instantiate/reset persisent starting time variable
if "startTime" not in globals() or Reset:
    startTime = time.time()

eval_list = []
for x in range(1, 1001):
    eval_list.append((1/1000) * x)

#print eval_list
    
# Calculate the elapsed time (in seconds)
ElapsedTime = int(time.time() - startTime)

# Output something every N seconds (using modulus to check)
if ElapsedTime > 0 and  ElapsedTime % Interval == 0:
    if STEP[S] == 1000:
        STEP[S] = 1
        Foo = eval_list[STEP[S]]
    else:
        Foo = eval_list[STEP[S]]
        print Foo
        print STEP[S]
        STEP[S] += 1
    STEP[V] = Foo
else:
    if V not in STEP:
        STEP[V] = 0
    else:
        Foo = STEP[V]
#else:
#    Foo = False
    
# Update the component
if start:
    updateComponent()