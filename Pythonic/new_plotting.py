
import matplotlib.pyplot as plt
import numpy as np

temp_x_ys = np.load("nbody_positions.npy")

fig = plt.figure(figsize=(10,10), dpi=80)
grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.3)
ax1 = plt.subplot(grid[0:2,0])

size = np.max([np.max(temp_x_ys[:,:,0]),np.max(temp_x_ys[:,:,1])])


for i in temp_x_ys:
    plt.cla()
    temp_xy = i.T
    ax1.set(xlim=(-size, size), ylim=(-size, size))
    plt.scatter(temp_xy[0], temp_xy[1])
    plt.pause(0.001)
    
