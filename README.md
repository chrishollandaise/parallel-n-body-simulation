# parallel-n-body-simulation

Here are the steps for getting the repository up and running on your local machine. You'll need conda.

>**Note:** you must have CUDA and Nvidia device installed on your machine in order to install cupy library. Here are the steps for that:
https://docs.cupy.dev/en/stable/install.html


```text
git clone https://github.com/chrishollandaise/parallel-n-body-simulation.git
cd parallel-n-body-simulation
conda create -n nbody-sim python=3.8.8
conda activate nbody-sim
conda install -c conda-forge ffmpeg
pip install -r requirements.txt
```
