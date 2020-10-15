"""
Python as a calculator / basic engineering tool
Cantilever beam
"""

import numpy as np                  # for vectors and matrices calculus (close to Matlab)
import matplotlib.pyplot as plt     # to plot the results


#plt.close('all')                    # closes all existing figures


### Data

L = 3                               # beam length (m)
b, h = 1, 0.6                     # base (m) and height (m)
F = 6.7e6                           # force (N)
E = 210e9                           # Young modulus (Pa)

Iz = b*h**3/12                      # inertia (m^4)

X = np.linspace(0,L,100)            # points where the displacement value will be calculated


#%% Cantilever beam for a given value of F

### Displacement for all x (Bernoulli)

v = -F/(E*Iz)*(L*X**2/2 - X**3/6)   # deflection for all chosen x values

### Plot

plt.figure() # creates a new figure
plt.plot(X,v) # plots the points (X,v)

# plot options
plt.title("Ceci n'est pas une poutre")
plt.xlabel('x')
plt.ylabel('v(x)')

#%% Cantilever beam for several values of F

# list of values for F
F_list = [2., 100, 5e3, 10743.27] # Python list. Can't be used for calculus, but can be used to store values.
#or F = np.array([2., 100, 5e3, 10743.27]) which creates a 1D array, that can be used for calculus.

### v calculation and plot

plt.figure("Hey, that's my new figure !") # new figure, with name

for ii in range(len(F_list)):
    print('We are showing the value number '+str(ii)+' : '+str(F_list[ii])+' Pa.') # printing in the console
    
    v = -F_list[ii]/(E*Iz)*(L*X**2/2 - X**3/6) # deflection for all chosen x values, for ii^th value of F_list
    
    plt.plot(X,v,label = f'F = {F_list[ii]} Pa') # plot + legend title
    
# plot options
plt.title("Several curves and legends")
plt.xlabel('x'); plt.ylabel('v(x)')  # ';' is rarely used : possibility to write 2 lines in one.
plt.legend() # adds the legend in the figure
plt.grid() # adds grid
#plt.subplot_tool()
#plt.subplots_adjust(left=0.16)






