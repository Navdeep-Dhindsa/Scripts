#!/bin/bash

#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=check_run
#SBATCH --partition=nandaq
#SBATCH --output=Job.%j.out
#SBATCH --error=Job.%j.err
#SBATCH --export=all
#SBATCH --mail-user=navdeepsingh@imsc.res.in
#SBATCH --mail-type=ALL
#SBATCH --time=24:00:00


while true; do
  njs=`qstat -u navdeepsingh | grep JOB_NAME | wc -l`
  #njs=`qstat -u navdeepsingh | grep JOB_NAME | grep -v " R " | wc -l`
  if [[ $njs ==0 ]] ; then
    break
  else
    sleep 1200
  fi
done

wait
