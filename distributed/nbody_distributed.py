
#Bring in all libraries
import numpy as np
import sys
from time import perf_counter
from mpi4py import MPI


def initialise(n):
    #Initialises random xyz, velocity and mass state 
    xyzs = np.random.randn(n,3)*10E12
    vels = np.random.randn(n,3)*0.0E3
    mass = np.random.uniform(0,1,n)*100E30
    return xyzs, vels, mass
    
def initialise_sun_earth():
    #create solar system dict with x_pos, y_vel, mass
    solar_system_info = {'sun': [0, 0, 1.989E30],
                         'earth': [148.88E9, 29.8E3, 5.972E24],
                         }
    #Puts solar system 
    xyz = []
    vels = []
    mass = []
    for i in solar_system_info:
        temp_pos = [solar_system_info[i][0], 0, 0]
        temp_vel = [0, solar_system_info[i][1], 0]
        temp_mass = solar_system_info[i][2]
        
        xyz.append(temp_pos)
        vels.append(temp_vel)
        mass.append(temp_mass)

    return np.asarray(xyz),np.asarray(vels),np.asarray(mass)
def initialise_solar_system():
    #create solar system dict with x_pos, y_vel, mass
    solar_system_info = {'sun': [0, 0, 1.989E30],
                         'mercury': [91E9, 47.9E3, 3.285E23],
                         'venus': [108.04E9, 35.0E3, 4.867E24],
                         'earth': [148.88E9, 29.8E3, 5.972E24],
                         'mars': [221.79E9, 24.1E3, 6.39E23],
                         'jupiter': [741.13E9, 13.1E3, 1.898E27],
                         'saturn': [1.4719E12, 9.7E3, 5.683E26],
                         'uranus': [2.9432E12, 6.8E3, 8.681E25],
                         'neptune': [4.4738E12, 5.4E3, 1.024E26],
                         }
    #Puts solar system 
    xyz = []
    vels = []
    mass = []
    for i in solar_system_info:
        temp_pos = [solar_system_info[i][0], 0, 0]
        temp_vel = [0, solar_system_info[i][1], 0]
        temp_mass = solar_system_info[i][2]
        
        xyz.append(temp_pos)
        vels.append(temp_vel)
        mass.append(temp_mass)

    return np.asarray(xyz),np.asarray(vels),np.asarray(mass)

#Gets the acceleration in x,y,z of a single body and returns its as an array
def get_total_acceleration_v2(body_position, all_positions, masses, G):
    
    #Set acceleration in each dimension to 0
    ax = ay = az = 0
    #Define a softening factor to negate dived by 0 erros or inf accelerations
    softening_factor = 1.3E9

    #Iterate through all positions in ralation to our body
    for i, position in enumerate(all_positions):
        #Find the seperation as a vector and split into seperate variable
        r = body_position - position
        dx, dy, dz = r[0], r[1], r[2]
        #Calc for finding acceleration factor
        squared_sep = dx*dx + dy*dy + dz*dz + softening_factor
        sq_root = np.sqrt(squared_sep)
        factor = -G*masses[i]/(squared_sep*sq_root)
        #Adding acceleration factor in each dimension
        ax += factor*dx
        ay += factor*dy
        az += factor*dz
    
    return np.array([ax, ay, az])

#Function calculates Potential Energy (PE) and Kinetic Energy (KE) from Velocity and position vector
def get_Energy(velocity, mass, body_position, all_positions, masses, G):
    #Kinetic Energy 1/2 m v^2
    KE = 0.5*mass*(sum(velocity**2))
    #Gravitational Energy GMm/r
    softening_factor = 1
    GPE = 0
    #finds the GPE for each body then sums up
    for i, position in enumerate(all_positions):
        r = body_position - position
        radius = np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
        if radius > 0:
            GPE += 0.5*G*masses[i]*mass/(radius)
    return KE, GPE

#Takes acc vector and timesteps, returning new position, new velocity
def time_step(position, velocity, acceleration, dt):
    #Do relevent calculations based on SUVAT
    #This method is bad for energy conservation
    new_position = position + velocity*dt
    new_velocity = velocity + acceleration*dt
    return np.array(new_position), np.array(new_velocity)

#Simple info function
def info(iterations, time_per_step, init_time, sim_time, num_bodies, nodes):
    print("\n**********************************\n")
    print(f"This simulation runs for {iterations} iterations in steps of {time_per_step} seconds")
    print(f"Total simulation time is {iterations*time_per_step/(60*60*24*365.25)}yrs")
    print(f'This was for {num_bodies} bodies.')
    print("\n**********************************\n")  
    print(f'Initialisation Time \t = \t {init_time}(s)')
    print(f'Simulation Time \t = \t {sim_time}(s)')

    print(f"Number of nodes used : {nodes}")
def main(steps,days,bodies):
    #Timing variables to monitor the simulation denoted by variables starting with _<name>
    _initialisation_start = perf_counter()
    
    #Finds rank of nodes and number of nodes
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nodes = comm.Get_size()


    #Any global parameters within main()
    TIMESTEP = 60*60*24*days        #time step in seconds
    G = 6.6743E-11                 #Gravitational Constant  
    TOTAL_BODIES = bodies

    #Choose whioch state to INITIALISE
    # pos_array, vel_array, mass_array = initialise_solar_system()
    pos_array, vel_array, mass_array = initialise(TOTAL_BODIES)
    # pos_array, vel_array, mass_array = initialise_sun_earth()
    
    #Setup variables for the simulation
    ##### BROADCAST MASS POS AND VEL ARRAYS #####
    simulation_velocities = vel_array
    simulation_positions = pos_array
    
    # stored_positions = []

    _initialisation_end = perf_counter()
    _simulation_start = perf_counter()
    
    index = np.arange(TOTAL_BODIES)
    ##### SCATTER INDEXES #####
    if rank == 0:
        all_indexes = np.array_split(index, nodes)
        communication_time_total = 0
        computation_time_total = 0
    else:
        all_indexes = None
    
    rank_index = comm.scatter(all_indexes, root = 0)

    #time step through the simulation
    for i in range(steps):
        one = MPI.Wtime()
        ###NEED TO BROADCAST CORRECT ARRAYS AT START
        simulation_positions = comm.bcast(simulation_positions, root=0)
        simulation_velocities = comm.bcast(simulation_velocities, root=0)
        
        pos_buffer = np.ones(len(rank_index), dtype='object')
        vel_buffer = np.ones(len(rank_index), dtype='object')
        # if rank == 1:
        #     print(len(rank_index))
        #     print(rank_index)
            
        #Runs through each body
        for j,body in enumerate(rank_index):
            three = MPI.Wtime()
            #Calculate the total acceleration 
            acc_vector = get_total_acceleration_v2(simulation_positions[body], simulation_positions, mass_array, G)
            #Update position and velocities
            new_pos, new_vel = time_step(simulation_positions[body], simulation_velocities[body], acc_vector, TIMESTEP)
            #Holds the new positions
            pos_buffer[j] = new_pos
            vel_buffer[j] = new_vel
            # if rank == 1:
            #     print(f'inloop {acc_vector}')
            four = MPI.Wtime()
        
        ##### GATHER POSITIONS AND VELS #####
        pos_gathered = comm.gather(pos_buffer, root=0)
        vel_gathered = comm.gather(vel_buffer, root=0)
        if rank == 0:
            simulation_positions = np.concatenate(pos_gathered)
            simulation_velocities = np.concatenate(vel_gathered)
        
        two = MPI.Wtime()
        if rank == 0:
            computation_time = four - three
            communication_time = (two - one) - computation_time
            computation_time_total += computation_time
            communication_time_total += communication_time
        
        # if rank == 1:
        #     print(f"Run number {i}",simulation_positions)
        
        #Store every x time steps to an array
        # if i%2 == 0:
        #     stored_positions.append(simulation_positions.copy())

    #Runs an information function that writes data cleanly
    _simulation_end = perf_counter()
    # print(_initialisation_end - _initialisation_start, _initialisation_start, _initialisation_end)
    initialisation_time = _initialisation_end - _initialisation_start
    simulation_time = _simulation_end - _simulation_start
    if rank == 0:
        info(steps, TIMESTEP, initialisation_time, simulation_time, TOTAL_BODIES, nodes)
        print(f'communication: {communication_time}, computation: {computation_time}')
    #Save stroed positions to numpy file
    # np.save("nbody_positions", stored_positions)
    # np.save("nbody_energies", stored_energy)
    # np.save("nbody_masses", mass_array)

#Arg passing for easier testing
if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("Usage: Python {} <ITERATIONS> <DAYS PER ITERATION> <BODIES>".format(sys.argv[0]))
        print("This program automatically finds how many nodes are available")

"""For Solar system set Days Per Iteration to 1"""