from mpi4py import MPI
import numpy as np
import sys


def double(dictionary):
    dictionary['key1'] = first_array
    dictionary['key2'] = second_array
    x= sum(first_array*second_array)
    return x

def main(nodes):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    #initialise arrays
    array = np.arange(20)
    split_arrays = np.array_split(array, nodes)
    
    if rank == 0:
        data = split_arrays
    else:
        data = None
        
    #This is the part to for loop(time stepping loop)
    for i in range(3):
        
        #Comm scatter and gather
        data = comm.scatter(data, root=0)
        
        #Noraml functions
        for i,number in enumerate(data):
            data[i] = double(number)
            
        data = comm.gather(data, root=0)
        if rank == 0:
            print()
            print(data)

        
if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        print("Usage: Python {} <NODES> ".format(sys.argv[0]))
    
