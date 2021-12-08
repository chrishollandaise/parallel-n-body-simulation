import nbody
from math import sin, cos, sqrt, radians, atan2, degrees, tan

G = 6.67 * 10**-11
# Force of gravity = (G * M * m) / d^2
# G = 6.67 * 10^-11 newton square meter kg^-2
# M is mass of colleague
# m is current mass
def g_force(p1, p2):
    return (G * p2.mass * p1.mass) / dist(p1, p2)**2

def dist(p1, p2):
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

if __name__ == "__main__":
    p1 = nbody.Particle( 1 , 6.4 * 10 ** 6 , 0 , 0 ) # One kg particle
    p2 = nbody.Particle( 6 * 10 ** 24 , 0 , 0 , 0 ) # EARTH
    '''
    cade = nbody.Particle( 86.1826, 0, 0, 0)
    chris = nbody.Particle( 74.8427, 2, 5, 7)
    p1 = cade
    p2 = chris
    '''
    d = dist(p1, p2)
    f = g_force(p1, p2)
    print(f"Net Force: {f}")
    fx, fy, fz = f*((p1.x-p2.x)/dist(p1, p2)), f*((p1.y-p2.y)/dist(p1, p2)), f*((p1.z-p2.z)/dist(p1, p2))
    print(f"X Force Vector: {fx}")
    print(f"Y Force Vector: {fy}")
    print(f"Z Force Vector: {fz}")
    #theta = atan2(abs(p1.x-p2.x), abs(p1.y-p2.y))
    #print(cos(theta) * f)
    #print(sin(theta) * f)
    #print(tan(theta) * f)