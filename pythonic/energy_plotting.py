
import matplotlib.pyplot as plt
import numpy as np


energies = np.load("nbody_energies.npy") #KE,GPE,total

fig = plt.figure(figsize=(10,10), dpi=80)
grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.3)
ax1 = plt.subplot(grid[0:2,0])

plt.plot(energies)
plt.show()