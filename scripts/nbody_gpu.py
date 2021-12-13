import simulation as simulation
import cupy as cp

# Create particles
# Create EPOCH Structure
# Send particles to device memory
# Call process epoch function and pass in epochs structure

# Define simulation constants

G = 6.6743 * 10 ** -11
TIME_STEP = 1
EPOCHS = 31536000

# Define CUDA specific variables / constants
N = 2097152

# Threads per block
TPB = 128
# Total Blocks
BLOCKS = (N // TPB)

device = cp.cuda.Device(0)
device.use()

#kernel = cp.RawModule(code=kernel_code)
start = cp.cuda.Event()
stop = cp.cuda.Event()


#ycalculator_func = kernel.get_function('ycalculator')
#reduce_func = kernel.get_function('reduce')