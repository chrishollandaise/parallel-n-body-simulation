import pickle as pkl
import sys
from os import path, mkdir

# python generate_dummy_output.py {epochs} {particle_count}

# X_SIZE X Y_SIZE canvas
X_SIZE = 720
Y_SIZE = 480

# In the GUI, particles have a radius that is greater than 1
PARTICLE_RADIUS = 40

# Pickle file output
out_dir = "profiles/"

# steps contains each step as array
# each step contains each particle
# each particle contains [x, y, z] elements

def create_dummy_pkl(step_count=100, particle_count=10):
    y_stride = Y_SIZE/(step_count-1)
    x_stride = X_SIZE/(particle_count-1) + PARTICLE_RADIUS
    
    # Creates matrix of evenly spaced particle [x, y, z] coordinates
    steps = []
    for step in range(step_count):
        steps.append([])
        for particle in range(particle_count):
            steps[step].append([particle*x_stride, step*y_stride, 0.0]) # [x, y, z]
        print(steps[step])
    
    if not path.exists(out_dir):
        mkdir(out_dir)

    file = open(f"{out_dir}steps_{step_count}_particles_{particle_count}.pkl", 'wb')
    pkl.dump(steps, file)

def main():
    if (len(sys.argv) > 2):
        create_dummy_pkl(int(sys.argv[1]), int(sys.argv[2]))
    else:
        create_dummy_pkl()

if __name__ == "__main__":
    main()