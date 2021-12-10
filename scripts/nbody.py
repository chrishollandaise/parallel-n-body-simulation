class Environment():
    def __init__( self, particles, x_size, y_size, duration):
        self.particles = particles # 2D Array
        self.x_size = x_size
        self.y_size = y_size
        self.duration = duration

class Particle():
    def __init__( self, mass, x, y, z, r=255, g=255, b=255, v=0, xvel=0, yvel=0, zvel=0 ):
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.v_x = xvel
        self.v_y = yvel
        self.v_z = zvel