
#Bring in all libraries
import numpy as np
import matplotlib.pyplot as plt
import time

def initialise(n):
    xyzs = np.random.randint(-10,10,size=(n,3))*10E12
    vels = np.random.randint(-10,10, size=(n,3))*0
    mass = np.random.randint(1, 10, size=(n))*10E30
    return xyzs, vels, mass
    
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

def initialise_solar_system():
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
    softening_factor = 1

    #Iterate through all positions in ralation to our body
    for i, position in enumerate(all_positions):
        
        #Find the seperation as a vector and split into seperate variable
        r = body_position - position
        dx, dy, dz = r[0], r[1], r[2]
        
        #Calc for finding acceleration factor
        squared_sep = dx*dx + dy*dy + dz*dz + softening_factor
        sq_root = np.sqrt(squared_sep)
        factor = -G*masses[i]/(squared_sep*sq_root)
        
        ax += factor*dx
        ay += factor*dy
        az += factor*dz
    
    return np.array([ax, ay, az])

    

#Function calculates Potential Energy (PE) and Kinetic Energy (KE) from Velocity and position vector
def get_Energy(velocity, mass):
    
    #Kinetic Energy 1/2 m v^2
    KE = 0.5*mass*(sum(velocity**2))
    
    return KE


#Takes acc vector and timesteps, returning new position, new velocity
def time_step(position, velocity, acceleration, dt):
    
    #Do relevent calculations
    new_position = position + velocity*dt
    
    new_velocity = velocity + acceleration*dt
    
    return new_position, new_velocity
    
def main():
    _initialisation_start = time.time()

    #Any global parameters
    TIMESTEP = 60*60         #time step in seconds
    G = 6.6743E-11          #Gravitational Constant  
    TOTAL_BODIES = 10

    pos_array, vel_array, mass_array = initialise_solar_system()
    #pos_array, vel_array, mass_array = initialise(TOTAL_BODIES)

    simulation_positions = pos_array
    simulation_velocities = vel_array

    stored_positions = []

    total_time = 1000

    _initialisation_end = time.time()

    _simulation_start = time.time()

    for i in range(total_time):

        for j in range(len(pos_array)):
            #Calculate the total acceleration 
            acc_vector = get_total_acceleration_v2(simulation_positions[j], pos_array, mass_array, G)
            
            #Update position, vels
            new_pos, new_vel = time_step(simulation_positions[j], simulation_velocities[j], acc_vector, TIMESTEP)
            
            simulation_positions[j] = new_pos
            simulation_velocities[j] = new_vel
        
        #Store every x timestep
        if i%1 == 0:
            stored_positions.append(simulation_positions.copy())

    _simulation_end = time.time()


    initialisation_time = _initialisation_end - _initialisation_start
    simulation_time = _simulation_end - _simulation_start

    print(f'Initialisation Time \t = \t {initialisation_time}(s)')
    print(f'Simulation Time \t = \t {simulation_time}(s)')

    #Save inputs to numpy file
    np.save("nbody_positions", stored_positions)


if __name__ == "__main__":
    main()

