import streamlit as st
import os
import subprocess

# --- Static Path Configuration ---
# Path to the shared tool directory
BASE_DIR = "/your/path/to/app_tool"
# Path to the Nextflow pipeline code
PIPELINE_PATH = os.path.join(BASE_DIR, "rnaseq")

# --- Dynamic Path Extraction ---
# Get the directory from which the user submitted sbatch
# If the variable is missing, it returns None
user_run_dir = os.environ.get('USER_RUN_DIR')

st.set_page_config(page_title="MHH RNA-seq Tool", page_icon="🧬", layout="wide")
st.title("🧬 MHH RNA-seq Automated Platform")

# --- Security Check: Force run via sbatch ---
if not user_run_dir:
    st.error("### ❌ Error: Execution Directory Not Detected!")
    st.info("""
    **To ensure results are saved correctly, please follow these steps:**
    1. Navigate to your project folder in the terminal.
    2. Launch the app using: 
       `sbatch /your/path/to/RNAseq_app.sh`
    3. Do NOT run this script directly using 'streamlit run' on the login node.
    """)
    st.stop()  # Stop script execution here

# --- UI Content (Only loaded if security check passes) ---
st.sidebar.success(f"📂 Target Workspace: \n{user_run_dir}")

st.markdown(f"""
### User Guidelines:
- Analysis results will be stored in: `{user_run_dir}/[Your_Project_Name]`
- Ensure your `samplesheet.csv` is prepared and accessible.
""")

# Input Fields
project_id = st.text_input("1. Project Name (folder name)", "Pilot_Study_01")
csv_path = st.text_input("2. Absolute path to samplesheet.csv")
genome = st.selectbox("3. Reference Genome (Species)", ["GRCh38", "mm10"])

# --- Execution Logic ---
if st.button("🚀 Start Automated Analysis", type="primary"):
    # Validation: Check if inputs are empty or if file doesn't exist
    if not csv_path or not project_id:
        st.error("❌ Please fill in all required fields.")
    elif not os.path.exists(csv_path):
        st.error(f"❌ Samplesheet file not found at: {csv_path}")
    else:
        # Define the final output path relative to user's current directory
        final_output_path = os.path.join(user_run_dir, project_id)
        
        # Construct the Nextflow command
        # -profile singularity: Uses containerized tools
        # -bg: Runs in background so closing the browser doesn't kill the job
        cmd = (
            f"nextflow run {PIPELINE_PATH} "
            f"--input {csv_path} "
            f"--outdir {final_output_path} "
            f"--genome {genome} "
            f"-profile singularity -bg"
        )
        
        # Execute the command as a background process
        subprocess.Popen(cmd, shell=True)
        
        st.success("✅ Analysis Task Submitted!")
        st.markdown(f"**Results Directory:** `{final_output_path}`")
        st.info("You may now close this browser tab. Progress logs will be generated in your project folder.")
        st.caption("MHH RNAseq Pipeline v1.1 | Developed for the AG_Schmidt-Ott Research Group")

