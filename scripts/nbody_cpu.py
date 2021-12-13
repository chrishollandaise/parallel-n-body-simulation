from simulation import simulation
from math import sqrt
from tqdm import tqdm
import copy

def _update_velocity( p1 , p2 , G , time_step ):
    '''
    Updates p1 final velocity after being affected by p2
    '''
    # Total distance in 3 planes
    d = sqrt( ( p1.x - p2.x ) ** 2 + ( p1.y - p2.y ) ** 2 + ( p1.z - p2.z ) ** 2 )

    # 3D - Force of gravity = G * ( ( M * m ) / d^2 )
    f_net = ( ( p2.mass * p1.mass ) / (d ** 2) ) * G

    # Compute each force vector
    f_x = f_net * ( ( p2.x - p1.x ) / d )
    f_y = f_net * ( ( p2.y - p1.y ) / d )
    f_z = f_net * ( ( p2.z - p1.z ) / d )

    # Calculate new velocity with decay in consideration plus new acceleration relative to time_step
    p1.v_x = p1.v_x + ( f_x / p1.mass ) * time_step
    p1.v_y = p1.v_y + ( f_y / p1.mass ) * time_step
    p1.v_z = p1.v_z + ( f_z / p1.mass ) * time_step

def _update_pos( p , time_step ):
    '''
    Updates x, y, z coordinates given velocity and time step
    '''
    p.x += p.v_x * time_step
    p.y += p.v_y * time_step
    p.z += p.v_z * time_step

def run_simulation(sim):
    for _ in tqdm(range(sim.get_epoch_count())):
        new_state = simulation.state(copy.deepcopy(sim.get_last_state().get_particles()))
        for p1 in new_state.get_particles():
            for p2 in new_state.get_particles():
                if p1 is not p2:
                    _update_velocity( p1 , p2 , sim.get_gravity() , sim.get_time_step() )
        for p in new_state.get_particles():
            _update_pos( p , sim.get_time_step() )
        sim.add_epoch(new_state)

if __name__ == "__main__":
    print("This file is not intended to be ran as a script. Please import for use.")