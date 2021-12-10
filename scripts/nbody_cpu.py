import nbody
import pickle as pkl
from math import sqrt

G = 6.67 * 10 ** -11
TIME_STEP = 2750
STEPS = 600
# Force of gravity = (G * M * m) / d^2
# G = 6.67 * 10^-11 newton square meter kg^-2
# M is mass of colleague
# m is current mass
def g_force(p1, p2):
    return ( G * p2.mass * p1.mass ) / (dist( p1, p2 ) ** 2)

def dist(p1, p2):
    return sqrt( ( p1.x - p2.x ) ** 2 + ( p1.y - p2.y ) ** 2 + ( p1.z - p2.z ) ** 2 )

def f_vector(c_p1, c_p2, total_f, total_d):
    return total_f * ( ( c_p2 - c_p1 ) / total_d )

# Return acceleration given force and mass
# Used on a per vector basis
a = lambda f, m: f / m

'''
Returns final velocity of p1 after being effected by p2
'''
def update_velocity(p1, p2):
    # Net force
    f_net = g_force( p1 , p2 )
    # Total distance in 3 planes
    d = dist( p1, p2 )

    f_x, f_y, f_z = f_vector( p1.x , p2.x , f_net , d ) , f_vector( p1.y , p2.y , f_net , d ) , f_vector( p1.z , p2.z , f_net , d )

    p1.v_x = p1.v_x + a(f_x, p1.mass) * TIME_STEP
    p1.v_y = p1.v_y + a(f_y, p1.mass) * TIME_STEP
    p1.v_z = p1.v_z + a(f_z, p1.mass) * TIME_STEP

def update_pos(p):
    p.x = p.x + p.v_x * TIME_STEP
    p.y = p.y + p.v_y * TIME_STEP
    p.z = p.z + p.v_z * TIME_STEP

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

if __name__ == "__main__":
    #p1 = nbody.Particle( 1 , 0 , 0 , 0 ) # One kg particle
    #earth = nbody.Particle( 6 * 10 ** 24 , 0 , 6.4 * 10 ** 6 , 0 ) # EARTH
    particles = [ nbody.Particle( 10000 , 250 , 250 , 0 ), nbody.Particle( 1000000 , -125 , -125 , 0 )]
    epochs = []
    run_simulation(epochs, particles)
    file = open(f"{STEPS}steps_{len(particles)}_particles_{TIME_STEP}spe.pkl", 'wb')
    pkl.dump(epochs, file)
    print(epochs)
    for p in particles:
        print("X, Y, Z Velocities")
        print(p.v_x)
        print(p.v_y)
        print(p.v_z)
        print("X, Y, Z Locations")
        print(p.x)
        print(p.y)
        print(f"{ p.z }\n")
    '''
    kiyomi = nbody.Particle( 63.5029, 0, 0, 0)
    cade = nbody.Particle( 86.1826, 1, 0, 0)
    large_brick = nbody.Particle( 1 * 10 ** 9, 2, 4, 6)
    particles = [cade, large_brick]
    for _ in range(STEPS):
        for p1 in particles:
            for p2 in particles:
                if p1 is not p2:
                    update_velocity(p1, p2)
    for p in particles:
        update_pos(p)
        print("X, Y, Z Velocities")
        print(p.v_x)
        print(p.v_y)
        print(p.v_z)
        print("X, Y, Z Locations")
        print(p.x)
        print(p.y)
        print(f"{ p.z }\n")
    '''



    '''
    cade = nbody.Particle( 86.1826, 0, 0, 0)
    chris = nbody.Particle( 74.8427, 2, 5, 7)
    p1 = cade
    p2 = chris
    '''
    #d = dist(p1, p2)
    #f = g_force(p1, p2)
    #print(f"Net Force: {f}")
    #fx, fy, fz = f*((p1.x-p2.x)/dist(p1, p2)), f*((p1.y-p2.y)/dist(p1, p2)), f*((p1.z-p2.z)/dist(p1, p2))
    #print(f"X Force Vector: { fx }")
    #print(f"Y Force Vector: { fy }")
    #print(f"Z Force Vector: { fz }")
    #theta = atan2(abs(p1.x-p2.x), abs(p1.y-p2.y))
    #print(cos(theta) * f)
    #print(sin(theta) * f)
    #print(tan(theta) * f)