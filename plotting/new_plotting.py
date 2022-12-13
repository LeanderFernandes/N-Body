import matplotlib.pyplot as plt
import numpy as np
import os
import glob

#Removes files
files = glob.glob('images\*')
for f in files:
    os.remove(f)

#Sets image
temp_x_ys = np.load("nbody_positions.npy")

fig = plt.figure(figsize=(10,10), dpi=80)
grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.3)
ax1 = plt.subplot(grid[0:2,0])
ax1.set_facecolor((0, 0, 0))

left, bottom, width, height = [0.125, 0.11, 0.3, 0.3]
ax2 = fig.add_axes([left, bottom, width, height])
ax2.set_facecolor((0, 0, 0))

size = np.max([np.max(temp_x_ys[:,:,0]),np.max(temp_x_ys[:,:,1])])

ax1.set(xlim=(-size, size), ylim=(-size, size))
ax2.set(xlim=(-size/10, size/10), ylim=(-size/10, size/10))
ax2.set_yticklabels([])
ax2.set_xticklabels([])
ax2.set_xticks([])
ax2.set_yticks([])

ax2.patch.set_edgecolor('white')  

ax2.patch.set_linewidth('3') 
 
#Plots images
for counter, i in enumerate(temp_x_ys):
    # plt.cla()
    temp_xy = i.T
    ax1.scatter(temp_xy[0], temp_xy[1], color = 'white', s=0.1)
    ax2.scatter(temp_xy[0], temp_xy[1], color = 'white', s=0.2)
    
    plt.pause(0.001)
    plt.savefig(f'images\{counter}.jpg')


 