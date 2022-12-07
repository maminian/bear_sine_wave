import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os

##

plt.style.use('dark_background')

##

# load the "stamp" once; trim out detail
df = pd.read_csv('bear.csv')
df['x'] = -df['x']
df['y'] = -df['y'] # matrix vs image coordinates
prescale = (df['x'].max() - df['x'].min())
df['x'] = df['x']/prescale
df['y'] = df['y']/prescale

df = df.iloc[::20]

##

def rotate(XY,angle):
    '''
    rotates XY, n-by-2, by angle in degrees theta.
    returns XY2, the rotated coords.
    '''
    th = angle*np.pi/180
    A = np.array([[np.cos(th), np.sin(th)],
                  [-np.sin(th), np.cos(th)]])
    return np.dot(XY,A)
    

# I want a tool that can let me say, 
# "Let's plop down a bear centered 
# at the given (x0, y0) coordinate.
def bearstamp(axis, x0, y0, size=1, rot=0):
    '''
    Inputs:
        axis : pyplot axis object as the result 
            of fig,ax = plt.subplots()
        x0   : horizontal center of the bear
        y0   : vertical center of the bear
        size : scaling factor of the bear (default: 1)
            
    Outputs:
        obj : the pyplot object as the result of axis.fill()
        
    The point is to plot the given bear 
    stamp loaded prior to this function
    centered at the given (x0,y0) coord.

    Examples:
    bearstamp(ax, 0, 0) # bear at 0,0 with size=1
    bearstamp(ax, 2, 4, 0.5) # bear at 2,4 with size=0.5 (half the size in each dim)
    
    '''

    XY = size*rotate(df[['x','y']],angle=rot) + np.array([x0,y0])

    
    obj = axis.fill(XY[:,0], 
              XY[:,1], 
              edgecolor=np.random.uniform(0,1,3),
              lw=2,
              facecolor=[1,1,0.85] # cream color?
              )
    axis.set_aspect('equal')
    
    return obj
#
fig,ax = plt.subplots(constrained_layout=True)

x = np.linspace(0, 2*np.pi, 13)[:-1]
y = np.sin(x)

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([min(x)-0.5, max(x)+0.5])
ax.set_ylim([min(y)-0.4, max(y)+0.4])


MAXBEARS = 9
MAXFRAMES = 240
count = 0
coll = []

if not os.path.exists('frames/'):
    os.mkdir('frames/')

for i in range(MAXFRAMES):
    ii = i%len(x)
    # What goes here????
    if i==0:
        angle=45
    else:
        angle = 180/np.pi*np.arctan2(y[ii%len(x)]-y[ii-1], np.mod(x[ii%len(x)]-x[ii-1], 2*np.pi))
    obj = bearstamp(ax, x[ii], y[ii], size=0.8, rot=angle)
    coll.append(obj)
    count += 1
    if count > MAXBEARS:
        oldbear = coll.pop(0)
        oldbear[0].remove()
        count -= 1
    for j,obj in enumerate(coll):
        obj[0].set_alpha((j+1)/len(coll))
    
    fname = os.path.join('frames', 'frame_%03d.png'%i)
    fig.savefig(fname, bbox_inches='tight')
#
