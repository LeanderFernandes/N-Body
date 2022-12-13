#!/bin/bash
# ======================
# pythonserialscript.sh
# ======================

#SBATCH --job-name=test_job
#SBATCH --partition=teach_cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --cpus-per-task=1
#SBATCH --time=0:45:00
#SBATCH --mem=0
#SBATCH --exclusive


cd $SLURM_SUBMIT_DIR

for i in {1..3}
do
    echo "1-12 threads 500 bodies"
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 1 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 2 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 4 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 6 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 8 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 10 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 12 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 14 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 16 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 18 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 20 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 22 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 24 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 26 500
    python ../N-Body/bluecrystal/nbody_multiprocessing.py 5 1 28 500
done