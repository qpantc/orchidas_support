# Any user-defined file "paramdef.py" must start with this command importing Paramdef class definition
from lib import Paramdef

# The second command must be the creation of the class instance with assignment of the number of PFTs
paramdef = Paramdef(npft = 15)

# Parameters setup used for the ORCHIDEE-TRUNK tuning
fmin = 0.5       # fraction of default parameter value to calculate lower boundary
fmax = 2.0       # fraction of default parameter value to calculate upper boundary
fmin_vmax = 0.25 # fmin value for vmax uptake parameters


### the following codes are added parameters
