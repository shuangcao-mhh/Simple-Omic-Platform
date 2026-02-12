#!/bin/bash
#SBATCH --job-name=RNAseq_GUI
#SBATCH --nodes=1
#SBATCH --cpus-per-task=15
#SBATCH --mem=80G
#SBATCH --time=24:00:00
#SBATCH --output=gui_server_%j.log

# 1. set up proxy
export http_proxy=http://your.proxy.server:port
export https_proxy=http://your.proxy.server:port

# 2. get current path
export USER_RUN_DIR=$(pwd)

# 3. activate env
source /your/path/to/miniforge3/bin/activate rnaseq_gui

# 4. define
PORT=8501
NODE=$(hostname)
USER_NAME=$(whoami) 

# 5. Define absloute path 
PY_APP="/your/path/to/rnaseq_app.py"

echo "---------------------------------------------------"
echo "RNAseq GUI Starting up..."
echo "Operator: $USER_NAME"
echo "Running nodes: $NODE"
echo ""
echo "Please access the local（Terminal/PowerShell）Execute the following command to open the tunnel："
echo "ssh -N -L ${PORT}:${NODE}:${PORT} ${USER_NAME}@${LOGIN_NODE}"
echo ""
echo "Now you can visit: http://localhost:${PORT}"
echo "---------------------------------------------------"

# start server
streamlit run $PY_APP --server.port $PORT --server.address 0.0.0.0 --server.headless true
