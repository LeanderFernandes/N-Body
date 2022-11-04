
import matplotlib.pyplot as plt
import numpy as np

temp_x_ys = np.load("nbody_positions.npy")

#stored position is [timestep, body, xyz]
temp = np.reshape(temp_x_ys[:,:,0:2], (len(temp_x_ys)*len(temp_x_ys[:][:][0]),2))
x_max = np.max(temp[:,0])
y_max = np.max(temp[:,1])

# Set the figure size
plt.rcParams["figure.figsize"] = [7.50, 7.50]
plt.rcParams["figure.autolayout"] = True

# plt.scatter(temp[:,0], temp[:,1], s = 0.01)
# plt.show()

fig = plt.figure(figsize=(10,10), dpi=80)
grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.3)
ax1 = plt.subplot(grid[0:2,0])

clear_rate = temp_x_ys.shape[1]
for i in range(int(len(temp[:,0])/clear_rate)):
    for j in range(clear_rate):
        plt.sca(ax1)
        ax1.set(xlim=(-x_max, x_max), ylim=(-y_max, y_max))
        xx = temp[i+j,0]
        yy = temp[i+j,1]
        plt.scatter(xx, yy)
        plt.pause(0.0001)
    plt.cla()