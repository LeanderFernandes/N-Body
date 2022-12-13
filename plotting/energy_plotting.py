
import matplotlib.pyplot as plt
import numpy as np


energies = np.load("nbody_energies.npy") #KE,GPE,total

fig = plt.figure(figsize=(10,10), dpi=80)
grid = plt.GridSpec(1, 1, wspace=0.0, hspace=0.3)
ax1 = plt.subplot(grid[0:2,0])

plt.style.use("classic")

plt.plot(energies, linewidth=3)

plt.xlabel("Time (5 days)")
plt.ylabel("Energy (J)")
ax1.legend(['Kinetic', 'Potential', 'Total'], loc='best')
ax1.set_ylim(0)


plt.show()