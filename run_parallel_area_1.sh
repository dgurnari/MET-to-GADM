#!/bin/bash --login
###
# Number of processors we will use (80 will fill two nodes)
#SBATCH --ntasks 37
# job name
#SBATCH --job-name=grid_dict_parall_1
# job stdout file
#SBATCH --output=logs/grid_dict_parall_1.out.%J
# job stderr file
#SBATCH --error=logs/grid_dict_parall_1.err.%J
# maximum job time in D-HH:MM
#SBATCH --time=0-10:00
###

# Ensure that parallel is available to us
module load parallel
module load anaconda/2019.03
source activate geo_env

# Define srun arguments:
srun="srun --nodes 1 --ntasks 1"
# --nodes 1 --ntasks 1         allocates a single core to each task

# Define parallel arguments:
parallel="parallel --max-procs $SLURM_NTASKS --joblog parallel_joblog"
# --max-procs $SLURM_NTASKS  is the number of concurrent tasks parallel runs, so number of CPUs allocated
# --joblog name     parallel's log file of tasks it has run

# Run the tasks:
$parallel "$srun python grid_to_gid_1.py {1}" :::: input/countries.txt
