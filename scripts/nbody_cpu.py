import nbody
import pickle as pkl
from math import sqrt

G_MULTIPLIER = 1 * 10 ** 8
G = 6.6743 * 10 ** -11 * G_MULTIPLIER# m^3/(kg*s^2)
TIME_STEP = 0.1
STEPS = 80000
DECAY_RATE = 0.999
# Force of gravity = (G * M * m) / d^2
# G = 6.6743 * 10^-11 newton square meter kg^-2
g_force = lambda p1, p2: ( ( p2.mass * p1.mass ) / (dist( p1, p2 ) ** 2) ) * G
dist = lambda p1, p2: sqrt( ( p1.x - p2.x ) ** 2 + ( p1.y - p2.y ) ** 2 + ( p1.z - p2.z ) ** 2 )

'''
Updates p1 final velocity after being affected by p2
'''
def update_velocity(p1, p2):
    # Net force in 3D
    f_net = g_force( p1 , p2 )

    # Total distance in 3 planes
    d = dist( p1, p2 )

    # Compute each force vector
    f_x = f_net * ( ( p2.x - p1.x ) / d )
    f_y = f_net * ( ( p2.y - p1.y ) / d )
    f_z = f_net * ( ( p2.z - p1.z ) / d )

    # Calculate new velocity with decay in consideration plus new acceleration relative to time_step
    p1.v_x = p1.v_x * DECAY_RATE + ( f_x / p1.mass ) * TIME_STEP
    p1.v_y = p1.v_y * DECAY_RATE + ( f_y / p1.mass ) * TIME_STEP
    p1.v_z = p1.v_z * DECAY_RATE + ( f_z / p1.mass ) * TIME_STEP

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
            epochs[epoch].append( [ p.x , p.y , p.z ] )
        print(f"{epoch} | {particles[0].x} {particles[0].y} | {particles[1].x} {particles[1].y}")

def output_results(epochs):
    file = open(f"{STEPS}steps_{len(particles)}_particles_{TIME_STEP}spe.pkl", 'wb')
    pkl.dump(epochs, file)

if __name__ == "__main__":
    # import random as rand
    # Generate 100 random particles between x=0 to 500
    # particles = []
    # for i in range(1_000_000):
    #    particles.append(nbody.Particle(x=rand.randint(0, 500), y=rand.randint(0, 500), z=0, mass=rand.randint(10, 500000)))

    particles = [ nbody.Particle( 100_000, 100 , 0 , 0 , yvel=-2 ), nbody.Particle( 100_000 , -100 , 0 , 0 , yvel=2 )]
    epochs = []
    #run_simulation(epochs, particles)
    #file = open(f"{STEPS}steps_{len(particles)}_particles_{TIME_STEP}spe.pkl", 'wb')
    # particles = [nbody.Particle( 120 , -100 , -100 , 0, xvel=0.0001, yvel=0.0001), nbody.Particle( 120 , 100 , 100 , 0 , xvel=-0.0001, yvel=-0.0001)]
    run_simulation(epochs, particles)
    #output_results(epochs)
    
    print(f"\nTime Step: {TIME_STEP}")
    print(f"Epochs: {STEPS}")
    #for d in epochs:
    #    print(d)
    for p in particles:
        print("X, Y, Z Velocities")
        print(p.v_x)
        print(p.v_y)
        print(p.v_z)
        print("X, Y, Z Locations")
        print(p.x)
        print(p.y)
        print(f"{ p.z }\n")