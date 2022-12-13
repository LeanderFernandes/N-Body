#!/bin/bash
#
# mpi4pyscript.sh

#SBATCH --job-name=10proc
#SBATCH --partition=teach_cpu
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=5
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem-per-cpu=0
#SBATCH --exclusive

# Load modules required for runtime e.g
module add languages/anaconda3/2020-3.8.5

cd $SLURM_SUBMIT_DIR

for i in {1..3}
do
    echo "10 processes 10"
    mpiexec -n 10 python ../N-Body/bluecrystal/nbody_distributed.py 5 1 10
done

for i in {1..3}
do
    echo "10 processes 50"
    mpiexec -n 10 python ../N-Body/bluecrystal/nbody_distributed.py 5 1 50
done

for i in {1..3}
do
    echo "10 processes 100"
    mpiexec -n 10 python ../N-Body/bluecrystal/nbody_distributed.py 5 1 100
done

for i in {1..3}
do
    echo "10 processes 500"
    mpiexec -n 10 python ../N-Body/bluecrystal/nbody_distributed.py 5 1 500
done

for i in {1..3}
do
    echo "10 processes 1000"
    mpiexec -n 10 python ../N-Body/bluecrystal/nbody_distributed.py 5 1 1000
done

