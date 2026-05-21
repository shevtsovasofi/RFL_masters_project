#!/bin/bash
#SBATCH --job-name=rki_fastapi
#SBATCH --partition=normal
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=12:00:00
#SBATCH --output=rki_fastapi_%j.log

source ~/.bashrc
conda activate sofia_env
cd /home/vignatenko/rki_video_app

PORT=8000

echo "===================================="
echo "SLURM job started"
echo "Node: $(hostname)"
echo "Port: ${PORT}"
echo "Job ID: ${SLURM_JOB_ID}"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES}"
echo "===================================="

uvicorn app.main:app --host 0.0.0.0 --port ${PORT}