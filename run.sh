#!/bin/bash

#SBATCH --chdir=/scratch/nas/4/norma/ppcnn
#SBATCH --job-name="ppcnn"
#SBATCH --output=/scratch/nas/4/norma/.log/stdout-%j.out
#SBATCH --error=/scratch/nas/4/norma/.log/stderr-%j.out
#SBATCH --wait-all-nodes=1

# Paths
#PYTHON="/scratch/nas/4/norma/venv/bin/python"
PYTHON="python3"
SERVER_INIT_FILE=".sync/server_ready.out"

# Search for host node and start server on it
$PYTHON -m ppcnn --server &

# Save server process id
SERVER_JOB_PID=`jobs -p`

# Wait for server to initialize
echo "Waiting for server"
SERVER_INIT=0
while [ $SERVER_INIT -eq 0 ]
do
    if test -f "$SERVER_INIT_FILE"; then
        SERVER_INIT=1
    fi
done

# Read address from file
SERVER_ADDRESS=`cat $SERVER_INIT_FILE`

# Run client on guest nodes
CLIENT_PIDS=""
for node in `scontrol show hostnames $SLURM_JOB_NODELIST`; do
    if [ "$HOSTNAME" != "$node" ] ; then
        $PYTHON -m ppcnn --address=$SERVER_ADDRESS --target=
        CLIENT_PIDS="$CLIENT_PIDS $!"
    fi
done

# Active wait for only server pid
wait $CLIENT_PIDS

# Delete sync file
rm $SERVER_INIT_FILE

# Kill server
kill $SERVER_JOB_PID
