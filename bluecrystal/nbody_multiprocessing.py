
#Bring in all libraries
import numpy as np
from time import perf_counter
import sys
from multiprocessing import Pool, Array
from itertools import repeat

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
def get_total_acceleration_v2(index, args):
    
    all_positions, masses, G = args[0], args[1], args[2]
    body_position = all_positions[index]
    # print(body_position)
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


#Takes acc vector and timesteps, returning new position, new velocity
def time_step(index, args):
    position, velocity, acceleration, dt = args[0][index], args[1][index], args[2][index], args[3]
    #Do relevent calculations based on SUVAT
    #This method is bad for energy conservation
    new_position = position + velocity*dt
    new_velocity = velocity + acceleration*dt
    returnable = np.concatenate((new_position, new_velocity))
    return returnable

#Simple info function
def info(iterations, time_per_step, init_time, sim_time, threads, num_bodies):
    print("\n**********************************\n")
    print(f'Number of bodies \t = \t {num_bodies}')
    print(f'Threads used \t \t = \t {threads}')
    print(f'Initialisation Time \t = \t {init_time}(s)')
    print(f'Simulation Time \t = \t {sim_time}(s)')
    print("\n**********************************\n\n")  

def main(steps,days,threads,bodies):
    #Timing variables to monitor the simulation denoted by variables starting with _<name>
    _initialisation_start = perf_counter()

    #Any global parameters within main()
    TIMESTEP = 60*60*24*days        #time step in seconds
    G = 6.6743E-11                 #Gravitational Constant  
    TOTAL_BODIES = bodies

    #Choose whioch state to INITIALISE
    # pos_array, vel_array, mass_array = initialise_solar_system()
    pos_array, vel_array, mass_array = initialise(TOTAL_BODIES)
    # pos_array, vel_array, mass_array = initialise_sun_earth()
    
    #Setup variables for the simulation
    simulation_positions = pos_array
    simulation_velocities = vel_array
    stored_positions = []
    stored_energy = []
    
    _initialisation_end = perf_counter()
    _simulation_start = perf_counter()

    #time step through the simulation
    for i in range(steps):
        #Open a pool of workers and shared index
        with Pool(threads) as p:
            indexes = Array('i', range(len(simulation_positions)))
            
            #Zip args,
            get_acc_arguments = [simulation_positions, mass_array, G]
            #send iterable,, through star map
            acc_vectors = p.starmap(get_total_acceleration_v2, zip(indexes, repeat(get_acc_arguments)))
            
            time_step_arguments = [simulation_positions, simulation_velocities, acc_vectors, TIMESTEP]
            result = p.starmap(time_step, zip(indexes, repeat(time_step_arguments)))
            ### Result[body][new_pos,new_vel] 
            new_pos = np.asarray([result[i][:3] for i in range(len(result))])
            new_vel = np.asarray([result[i][3:] for i in range(len(result))])

            p.close()
            p.join()

        #Holds the new positions
        simulation_positions = new_pos
        simulation_velocities = new_vel
        #
        # Removed energy
        #
        #Store every x time steps to an array
        # if i%5 == 0:
        #     stored_positions.append(new_pos.copy())
        

    #Runs an information function that writes data cleanly
    _simulation_end = perf_counter()
    initialisation_time = _initialisation_end - _initialisation_start
    simulation_time = _simulation_end - _simulation_start
    info(steps, TIMESTEP, initialisation_time, simulation_time, threads, TOTAL_BODIES)
    
    #Save stroed positions to numpy file
    # np.save("nbody_positions", stored_positions)
    # np.save("nbody_energies", stored_energy)
    # np.save("nbody_masses", mass_array)

#Arg passing for easier testing
if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        print("Usage: Python {} <ITERATIONS> <DAYS PER ITERATION> <THREADS> <BODIES>".format(sys.argv[0]))


"""For Solar system set Days Per Iteration to 1"""