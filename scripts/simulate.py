import nbody_cpu
from simulation import simulation
import argparse
import sys
try:
    import nbody_gpu
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def _arg_parse():
    parser = argparse.ArgumentParser(description="Run NBody Simulation on either the CPU or GPU")
    parser.add_argument('--epochs' , '-e' , metavar = "{EPOCH_COUNT}" , type = int , help = "Number of epochs to calculate" , required = True)
    parser.add_argument('--step' , '-s' , metavar = "{TIME_STEP}" , type = int , help = "How many seconds to calculate per epoch" , required = True)
    parser.add_argument('--title' , '-t' , metavar = "{TITLE}" , type = str , help = "Title of the simulation" , required = False)
    parser.add_argument('--particles' , '-p' , metavar = "{PARTICLE_FILE}" , type = str , help = "Full file path to .txt containing starting particle information" , required= True)
    parser.add_argument('--out_dir' , '-o' , metavar = "{OUT_DIRECTORY}" , type = str , help = "File to output sim.pkl simulation results" , required = True)
    parser.add_argument('--mode' , '-m' , metavar = "{MODE}" , default='cpu' , type = str , choices=['cpu','gpu'] ,  help = "Selects compute engine")
    return parser.parse_args() 

def _main():
    args = _arg_parse()
    print(args)
    sim = simulation( args.title , args.epochs , args.step )
    start_env = simulation.state()
    try:
        file = open( args.particles , 'r' )
        for line in file.readlines():
            p = line.strip().split(",")
            for i, ele in enumerate(p):
                p[i] = float(eval(ele))
            #print(p)
            start_env.add_particle(p[0],p[1],p[2],p[3],p[4],p[5],p[6])
        sim.add_epoch(start_env)
    except FileNotFoundError:
        raise FileNotFoundError(f"{args.particle_file} not found")
    
    if args.mode == "cpu":
        nbody_cpu.run_simulation(sim)
    elif args.mode == "gpu":
        if not GPU_AVAILABLE:
            raise Exception("CUDA support not available")
            
        nbody_gpu.run_simulation(sim, args.out_dir)
    
    sim.output_results(args.out_dir)

if __name__ == "__main__":
    _main()