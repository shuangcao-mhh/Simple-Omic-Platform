import streamlit as st
import subprocess
import os

# --- Static Path Configuration ---
BASE_DIR = "/your/path/to/app_tool"
REF_DIR = os.path.join(BASE_DIR, "cellranger_reference")
CELLRANGER_EXE = os.path.join(BASE_DIR, "cellranger-10.0.0/cellranger")

# --- Dynamic Path Extraction from environment ---
# This variable is exported in the .sh script to lock the output to the user's current folder
user_run_dir = os.environ.get('USER_RUN_DIR')

st.set_page_config(page_title="CellRanger Count Hub", layout="wide")

# --- Security Check: Force launch via sbatch ---
if not user_run_dir:
    st.error("### ❌ Error: Execution Directory Not Detected!")
    st.info("Please launch the app using `sbatch` from your project directory.")
    st.stop()

# --- Software Status Check ---
if not os.path.exists(CELLRANGER_EXE):
    st.error(f"❌ CellRanger binary not found at: {CELLRANGER_EXE}")
else:
    st.sidebar.success("✅ CellRanger Engine: Ready")

st.title("🧬 CellRanger GEX & CRISPR Platform")
st.sidebar.markdown(f"**Target Workspace:**\n`{user_run_dir}`")
st.markdown("---")

# --- Parameter Configuration ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Analysis Configuration")
    # Users can choose between standard mRNA or CRISPR screening
    mode = st.radio("Experiment Type", ["Standard GEX (3'/5')", "CRISPR / Feature Barcoding"])
    sample_id = st.text_input("Sample ID", placeholder="e.g., AKI_Day3_Project")
    
    # Identify available GEX reference genomes
    try:
        ref_options = [d for d in os.listdir(REF_DIR) if os.path.isdir(os.path.join(REF_DIR, d))]
    except:
        ref_options = ["Reference directory not found"]
    reference = st.selectbox("Select Reference Genome", ref_options)

with col2:
    st.subheader("2. Input Data Settings")
    
    if mode == "Standard GEX (3'/5')":
        # Only one folder path is needed for standard sequencing
        fastq_path = st.text_input("FASTQ Folder Path", placeholder="/absolute/path/to/fastqs")
    else:
        # CRISPR mode requires specific mapping files
        st.warning("⚠️ CRISPR mode requires Libraries and Feature Reference CSV files.")
        libraries_csv = st.text_input("Libraries CSV Path", placeholder="/path/to/libraries.csv")
        feature_ref = st.text_input("Feature Reference CSV Path", placeholder="/path/to/feature_ref.csv")
    
    # Locked result path (User's current dir)
    output_root = st.text_input("Output Directory", value=user_run_dir, disabled=True)

# --- Resource Allocation ---
st.subheader("3. Resource Allocation")
c1, c2 = st.columns(2)
cores = c1.number_input("Cores (Max 16)", min_value=1, max_value=16, value=15)
memory = c2.number_input("Memory (GB, Max 120)", min_value=1, max_value=120, value=110)

# --- Task Execution ---
if st.button("🚀 Launch CellRanger Count", type="primary"):
    # Build the standard 'cellranger count' command base
    cmd = [
        CELLRANGER_EXE, "count",
        f"--id={sample_id}",
        f"--transcriptome={os.path.join(REF_DIR, reference)}",
        f"--create-bam=true",
        f"--localcores={int(cores)}",
        f"--localmem={int(memory)}"
    ]

    # Add mode-specific flags
    if mode == "Standard GEX (3'/5')":
        if not fastq_path: st.error("Please enter FASTQ path!"); st.stop()
        cmd.append(f"--fastqs={fastq_path}")
    else:
        if not libraries_csv or not feature_ref: st.error("CSV paths required!"); st.stop()
        cmd.append(f"--libraries={libraries_csv}")
        cmd.append(f"--feature-ref={feature_ref}")

    full_cmd = " ".join(cmd)
    st.code(full_cmd, language="bash")
    
    with st.spinner(f"Processing {sample_id}... Do not close this tab."):
        try:
            # Execute in the user's run directory so results appear there
            process = subprocess.Popen(
                full_cmd, shell=True, cwd=user_run_dir,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            
            log_placeholder = st.empty()
            log_text = ""
            for line in process.stdout:
                log_text += line
                # Display the last 15 lines to keep the UI clean
                recent_logs = "\n".join(log_text.splitlines()[-15:])
                log_placeholder.text_area("Live Processing Log", recent_logs, height=300)
            
            process.wait()
            if process.returncode == 0:
                st.success(f"✅ Analysis for {sample_id} successfully finished!")
                st.balloons()
            else:
                st.error("❌ CellRanger failed. Check the logs in your project directory.")
        except Exception as e:
            st.error(f"Error occurred: {e}")

st.markdown("---")

st.caption("MHH CellRanger Pipeline v1.1 | Developed for AG Schmidt-Ott")
