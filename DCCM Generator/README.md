# DCCM Analysis Tool
A Python script to compute and visualize the Dynamical Cross-Correlation Matrix (DCCM) from Molecular Dynamics (MD) trajectories using MDAnalysis.
This tool helps analyze residue-level correlations in protein dynamics, which is useful for understanding functional motions and allosteric activity in biomolecules.

## Features
- Reads topology and trajectory files (e.g., PDB and XTC).
- Supports customizable atom selection (default: alpha-carbons).
- Aligns trajectory frames to remove rotational and translational motion.
- Computes covariance and correlation matrices.
- Generates a high-resolution heatmap of the cross-correlation matrix.

## Requirements
 pip install numpy matplotlib MDAnalysis

## Input Files
1. Topology File : A structure file like .pdb.
2. Trajectory File : Trajectory file such as .xtc, .dcd, etc.

## How to Run
1. Clone or download the repository.
2. Open terminal in the project directory.
3. Run the script: python "dccm_analysis.py <topology_file.pdb> <trajectory_file.xtc>"

## Output
The script produces two things:
1. A NumPy matrix representing the DCCM (not saved by default but can be extended).
2. A publication-quality heatmap (dccm.png) showing:
    - Positive correlations (red)
    - Negative correlations (blue)
    - No correlation (white)

📬 Contact
For questions or suggestions, reach out at:
📧 kristiadimikael@gmail.com
