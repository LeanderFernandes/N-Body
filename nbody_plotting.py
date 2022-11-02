#%%
import matplotlib.pyplot as plt
import numpy as np

temp_x_ys = np.load("nbody_positions.npy")

#stored position is [timestep, body, xyz]
temp = np.reshape(temp_x_ys[:,:,0:2], (len(temp_x_ys)*len(temp_x_ys[:][:][0]),2))

# Set the figure size
plt.rcParams["figure.figsize"] = [7.50, 7.50]
plt.rcParams["figure.autolayout"] = True

plt.scatter(temp[:,0], temp[:,1], s = 0.01)
plt.show()
