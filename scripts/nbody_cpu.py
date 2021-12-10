import nbody
import pickle as pkl
from math import sqrt

G = 6.67 * 10 ** -11
TIME_STEP = 2500
STEPS = 1000
# Force of gravity = (G * M * m) / d^2
# G = 6.67 * 10^-11 newton square meter kg^-2
# M is mass of colleague
# m is current mass
g_force = lambda p1, p2: ( G * p2.mass * p1.mass ) / (dist( p1, p2 ) ** 2)
dist = lambda p1, p2: sqrt( ( p1.x - p2.x ) ** 2 + ( p1.y - p2.y ) ** 2 + ( p1.z - p2.z ) ** 2 )
f_vector = lambda total_f, vector_d, total_d: total_f * ( ( -vector_d ) / total_d )
# Return acceleration given force and mass
# Used on a per vector basis
a = lambda f, m: f / m

'''
def f_vector(c_p1, c_p2, total_f, total_d):
    f = abs(total_f * ( ( c_p2 - c_p1 ) / total_d ))
    print(f"{-f}\n" if c_p2-c_p1 > 0 else f"{f}\n" if f != 0 else "",end="")
    return f if c_p2-c_p1 > 0 else -f
'''

'''
Returns final velocity of p1 after being effected by p2
'''
def update_velocity(p1, p2):
    # Net force
    f_net = g_force( p1 , p2 )
    # Total distance in 3 planes
    d = dist( p1, p2 )

    f_x, f_y, f_z = f_vector( p1.x - p2.x , f_net , d ) , f_vector( p1.y - p2.y , f_net , d ) , f_vector( p1.z - p2.z , f_net , d )
    p1.v_x += a(f_x, p1.mass) * TIME_STEP
    p1.v_y += a(f_y, p1.mass) * TIME_STEP
    p1.v_z += a(f_z, p1.mass) * TIME_STEP

def update_pos(p):
    p.x += p.v_x * TIME_STEP
    p.y += p.v_y * TIME_STEP
    p.z += p.v_z * TIME_STEP

def run_simulation(epochs, particles):
    for epoch in range(STEPS):
        epochs.append([])
        for p1 in particles:
            for p2 in particles:
                if p1 is not p2:
                    update_velocity( p1 , p2 )
        for p in particles:
            update_pos(p)
            epochs[epoch].append([p.x, p.y, p.z])

def output_results(epochs):
    file = open(f"{STEPS}steps_{len(particles)}_particles_{TIME_STEP}spe.pkl", 'wb')
    pkl.dump(epochs, file)

if __name__ == "__main__":
    #p1 = nbody.Particle( 1 , 0 , 0 , 0 ) # One kg particle
    #earth = nbody.Particle( 6 * 10 ** 24 , 0 , 6.4 * 10 ** 6 , 0 ) # EARTH
    #particles = [ nbody.Particle( 10000 , 250 , 250 , 0 ), nbody.Particle( 1000000 , -125 , -125 , 0 )]
    particles = [nbody.Particle( 120 , -100 , -100 , 0, xvel=0.0001, yvel=0.0001), nbody.Particle( 120 , 100 , 100 , 0 , xvel=-0.0001, yvel=-0.0001)]
    epochs = []
    run_simulation(epochs, particles)
    output_results(epochs)
    for d in epochs:
        print(d)
    for p in particles:
        print("X, Y, Z Velocities")
        print(p.v_x)
        print(p.v_y)
        print(p.v_z)
        print("X, Y, Z Locations")
        print(p.x)
        print(p.y)
        print(f"{ p.z }\n")