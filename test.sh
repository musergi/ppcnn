#!/bin/bash

#SBATCH --chdir=/scratch/nas/4/norma/ppcnn
#SBATCH --job-name="ppcnn"
#SBATCH --output=/scratch/nas/4/norma/.log/stdout-%j.out
#SBATCH --error=/scratch/nas/4/norma/.log/stderr-%j.out
#SBATCH --wait-all-nodes=1

echo Host name: $HOSTNAME

CHILD_HOSTNAMES=""
for node in `scontrol show hostnames $SLURM_JOB_NODELIST`; do
    if ["$HOSTNAME" == "$node"] ; then
    #    CHILD_HOSTNAMES="$CHILD_HOSTNAMES $node"
    else
        echo $node
    fi
done

echo Child names: $CHILD_HOSTNAMES