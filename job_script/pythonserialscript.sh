#!/bin/bash
# ======================
# pythonserialscript.sh
# ======================

#SBATCH --job-name=seriel_1_cpu
#SBATCH --partition=teach_cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=100M

module add languages/anaconda/2020-3.8.5

cd $SLURM_SUBMIT_DIR
python ../N-Body/bluecrystal/nbody_pythonic.py 5 1 9000
python ../N-Body/bluecrystal/nbody_pythonic.py 5 1 10000


