from mpi4py import MPI
import numpy as np
import sys


def double(x):
    return x*2

def main(nodes):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    #initialise arrays
    position = np.arange(20)
    
    if rank == 0:
        split_arrays = np.array_split(position, nodes)
    else:
        split_arrays = None
        
    #Need to scatter position arrays so each
    #nodes knows which body to work on
    
    #inital scatter
    positions = comm.scatter(split_arrays, root=0)
    
    #This is the part to for loop(time stepping loop)
    for i in range(3):

        #In loop scatter
        positions = comm.scatter(positions, root=0)
        
        #Need to broadcast position, mass, velocities
        masses = comm.brdcast(masses, root = 0)
        
        #Need to collect positions and masses
        
        #iterate through allocated positions
        for i,position in enumerate(positions):
            
            #Run get_acceleration()
            
            #Get new_pos and new_vel
            
            #update positions and velocites
            data[i] = double(number)
        
        #gather positions and velocities            
        position = comm.gather(position, root=0)
        if rank == 0:
            print()
            print(data)

        
if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        print("Usage: Python {} <NODES> ".format(sys.argv[0]))
    
    #MAIN
        #initialise arrays
        #Need to scatter position arrays so each
        #nodes knows which body to work on
        #Broadcast constants
        
        #inital scatter
        #Timestep loop
            #In loop scatter
            #Need to broadcast position, mass, velocities
            #Need to collect positions and masses
            #iterate through allocated positions
                #Run get_acceleration()
                #Get new_pos and new_vel
                #update positions and velocites
            #gather positions and velocities            
