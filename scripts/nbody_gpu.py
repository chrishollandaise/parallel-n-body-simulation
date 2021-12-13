from pathlib import Path
import cupy as cp
import numpy as np

def run_simulation(sim):
    device = cp.cuda.Device(0)
    device.use()
    kernel_code = Path('nbody_kernel.cu').read_text()
    kernel = cp.RawModule(code=kernel_code)

    PARTICLE_COUNT = len(sim.get_last_state().get_particles())

    TPB = 32
    BLOCKS = (PARTICLE_COUNT // TPB)

    # Get device constants
    d_g_pointer = kernel.get_global('g')
    #d_mass_pointer = kernel.get_global('mass')
    d_time_step_pointer = kernel.get_global('time_step')
    d_particle_count_pointer = kernel.get_global('particle_count')

    # Allocate array space
    #d_mass_point = cp.empty(PARTICLE_COUNT, dtype=cp.int64)

    # Create reference
    d_g = cp.ndarray(1, cp.int64, d_g_pointer)
    d_time_step = cp.ndarray(1, cp.int64, d_time_step_pointer)
    d_particle_count = cp.ndarray(1, cp.int64, d_particle_count_pointer)
    #d_mass = cp.ndarray(PARTICLE_COUNT, cp.int64, d_mass_pointer)

    # Set device constant values
    d_g[0] = sim.get_gravity()
    d_time_step[0] = sim.get_time_step()
    d_particle_count[0] = PARTICLE_COUNT

    h_mass = []
    for p in sim.get_last_state().get_particles():
        h_mass.append(p.mass)
    
    #d_mass = cp.asarray(np.asarray(h_mass),dtype=np.int64)

    d_x = cp.empty(PARTICLE_COUNT, dtype=np.float64)
    d_y = cp.empty(PARTICLE_COUNT, dtype=np.float64)
    d_z = cp.empty(PARTICLE_COUNT, dtype=np.float64)

    # HOST Get list of all X, Y, and Z coordinates in their own respective lists
    particles = [(p.x, p.y, p.z, p.v_x, p.v_y, p.v_z) for p in sim.get_last_state().get_particles()]
    h_x, h_y, h_z, h_v_x, h_v_y, h_v_z = [p[0] for p in particles], [p[1] for p in particles], [p[2] for p in particles], [p[3] for p in particles], [p[4] for p in particles], [p[5] for p in particles]

    # Put all host arrays on device
    d_x = cp.asarray(np.asarray(h_x))
    d_y = cp.asarray(np.asarray(h_y))
    d_z = cp.asarray(np.asarray(h_z))
    d_v_x = cp.asarray(np.asarray(h_v_x))
    d_v_y = cp.asarray(np.asarray(h_v_y))
    d_v_z = cp.asarray(np.asarray(h_v_z))
    

    update_velocity = kernel.get_function('update_velocity')
    update_position = kernel.get_function('update_position')

    #update_velocity(BLOCKS, TPB, ( d_x, d_y, d_z, d_v_x, d_v_y, d_v_z ) )
    # Syncronize
    #update_position(BLOCKS, TPB, ( d_x, d_y, d_z, d_v_x, d_v_y, d_v_z ) )
    # Syncronize 