import sys
import os
import random as r

def main(out_path):
    n_bodies = int(sys.argv[2])
    mass_mean = float(sys.argv[3])
    x_bounds = float(sys.argv[4])
    y_bounds = float(sys.argv[5])

    try:
        method = int(sys.argv[6])
    except:
        method = 0


    std = mass_mean * r.uniform(0.1, 0.8)
    distribs =  [
                lambda a, b : r.gauss(a, b),
                r.choice([lambda a, b : r.triangular(a, b, 0.5*(a+b)), lambda a, b : r.triangular((a+b), b, 0.5*a), lambda a, b : r.triangular(0.5*(a+b), b, a)]),
                lambda a, b : r.paretovariate(a),
                lambda a, b : r.uniform(a, b),
                ]
    strategy = distribs[method]

    masses = [strategy(mass_mean, std) for i in range(n_bodies)]
    x_positions = [strategy(-x_bounds, x_bounds) for i in range(n_bodies)]
    y_positions = [strategy(-y_bounds, y_bounds) for i in range(n_bodies)]

    with open(out_path, 'w') as f:
        for mass, x, y in zip(masses, x_positions, y_positions):
            f.write(f'{abs(mass)},{x},{y},0,0,0,0\n')

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("\nIncorrect number of arguments.")
        print(f'Usage: python {sys.argv[0]} <CONFIGURATION_NAME> <N_BODIES> <MASS> <X_BOUNDS> <Y_BOUNDS> <STRATEGY>\n')
        print("\tSTRATEGY: 0 - Gaussian, 1 - Triangular, 2 - Pareto, 3 - Uniform\n")
        print("\tBy default, the strategy is gaussian.\n")
        print("Examples:\n python {sys.argv[0]} test.txt 10 1.0 0.5 0.5\n  python {sys.argv[0]} test.txt 10 1.0 0.5 0.5 1\n")
        sys.exit(1)
    
    configuration_name = sys.argv[1]
    out_path = os.path.join(os.getcwd(), 'configurations', f'{configuration_name}')
    out_dir = os.path.dirname(out_path)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    main(out_path)