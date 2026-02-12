#!/bin/bash
#SBATCH --job-name=CellRanger_GUI
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16             
#SBATCH --mem=128G                      
#SBATCH --time=48:00:00                
#SBATCH --output=cellranger_gui_%j.log

# 1. Set up network proxy
export http_proxy=http://your.proxy.server:port
export https_proxy=http://your.proxy.server:port

# 2. Capture the directory where the user submitted sbatch
# This ensures results are saved in the user's current folder
export USER_RUN_DIR=$(pwd)

# 3. Activate environment and tool paths
# Ensure the path to your cellranger-10.0.0 is correct
export PATH=/path/to/your/cellranger-10.0.0:$PATH
source /path/to/your/miniforge3/bin/activate rnaseq_gui

# 4. Define connection variables
PORT=8502                              
NODE=$(hostname)
USER_NAME=$(whoami)
PY_APP="/path/to/your/cellranger_app.py"

echo "---------------------------------------------------"
echo "CellRanger GUI Starting up..."
echo "Operator: $USER_NAME"
echo "Current Directory: $USER_RUN_DIR"
echo "Running on node: $NODE"
echo ""
echo "Please run the following command on your LOCAL machine:"
echo "ssh -N -L ${PORT}:${NODE}:${PORT} ${USER_NAME}@${LOGIN_NODE}"
echo ""
echo "Access the platform at: http://localhost:${PORT}"
echo "---------------------------------------------------"

# 5. Start the Streamlit server
streamlit run $PY_APP --server.port $PORT --server.address 0.0.0.0 --server.headless true
