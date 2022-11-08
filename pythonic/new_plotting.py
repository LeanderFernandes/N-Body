import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
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

size = np.max([np.max(temp_x_ys[:,:,0]),np.max(temp_x_ys[:,:,1])])

#Plots images
for counter, i in enumerate(temp_x_ys):
    plt.cla()
    temp_xy = i.T
    ax1.set(xlim=(-size, size), ylim=(-size, size))
    plt.scatter(temp_xy[0], temp_xy[1], color = 'white')
    plt.pause(0.001)
    plt.savefig(f'images\{counter}.jpg')


#Turns images into video