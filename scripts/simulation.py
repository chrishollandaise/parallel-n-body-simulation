import pickle as pkl
import os

class simulation():
    def __init__( self , title , epoch_count , time_step , gravity = 6.6743 * 10 ** -11 ):
        self.title = title
        self.epoch_count = epoch_count
        self.time_step = time_step
        self.gravity = gravity
        self.epochs = []

    def get_last_state( self ):
        return self.epochs[len(self.epochs)-1]

    def get_epoch_count( self ):
        return self.epoch_count
    
    def get_gravity( self ):
        return self.gravity

    def get_epochs( self ):
        return self.epochs
    
    def get_time_step( self ):
        return self.time_step

    def add_epoch( self , epoch ):
        self.epochs.append( epoch )
    
    def output_results( self , directory ):
        file = open( os.path.join( directory , f"SIM_{self.title}.sim.pkl" ) , 'wb' )
        out_data = []
        for i, state in enumerate(self.epochs):
            out_data.append( [] )
            for p in state.get_particles():
                out_data[i].append( [ p.x , p.y , p.z ] )
        pkl.dump(out_data, file)

    class state():
        def __init__( self , particles = [] ):
            self.particles = particles
        
        def add_particle( self , mass , x , y , z , xvel = 0.0 , yvel = 0.0 , zvel = 0.0 ):
            self.particles.append(simulation.state._particle( mass , x , y , z , xvel = 0.0 , yvel = 0.0 , zvel = 0.0 ))
        
        def get_particles( self ):
            return self.particles

        def print_particles_location( self ):
            for p in self.particles:
                print(f"{p.x} , {p.y} , {p.z}" , end= " | ")

        class _particle():
            def __init__( self , mass , x , y , z , xvel = 0.0 , yvel = 0.0 , zvel = 0.0 ):
                self.mass = mass
                self.x = x
                self.y = y
                self.z = z
                self.v_x = xvel
                self.v_y = yvel
                self.v_z = zvel