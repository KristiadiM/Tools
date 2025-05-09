#python DCCM.py HRV1.pdb md_Cov1_center.xtc

import numpy as np
import MDAnalysis as mda
import matplotlib.pyplot as plt
from MDAnalysis.analysis import align

def calculate_dccm(topology_file, trajectory_file, selection='name CA', stride=1):
    """
    Calculate Dynamical Cross-Correlation Matrix (DCCM) from MD trajectory.
    
    Parameters:
    topology_file (str): Path to topology file (PDB)
    trajectory_file (str): Path to trajectory file (XTC, DCD, etc.)
    selection (str): Atom selection string (default: alpha-carbons)
    stride (int): Frame stride for sampling (default: 1)
    
    Returns:
    np.ndarray: DCCM matrix
    """
    
    # Load the universe
    u = mda.Universe(topology_file, trajectory_file)
    
    # Select atoms
    atoms = u.select_atoms(selection)
    n_atoms = len(atoms)
    
    # Create a reference universe from the initial frame
    ref = mda.Universe(topology_file)
    ref.load_new(u.trajectory[0].positions)
    
    # Calculate displacement vectors
    displacements = []
    for ts in u.trajectory[::stride]:
        # Align current frame to reference
        align.alignto(u, ref, select=selection, weights='mass')
        
        # Get coordinates of selected atoms
        coords = atoms.positions
        
        # Calculate displacement vectors
        if len(displacements) == 0:
            displacements = coords
        else:
            displacements = np.append(displacements, coords, axis=0)
    
    # Reshape displacements
    n_frames = int(len(displacements) / n_atoms)
    displacements = displacements.reshape(n_frames, n_atoms, 3)
    
    # Calculate mean displacement
    mean_displacement = np.mean(displacements, axis=0)
    
    # Calculate covariance matrix
    covariance = np.zeros((n_atoms, n_atoms))
    for i in range(n_atoms):
        for j in range(n_atoms):
            # Calculate covariance between atoms i and j
            covariance[i,j] = np.mean((displacements[:,i,:] - mean_displacement[i,:]) * 
                                     (displacements[:,j,:] - mean_displacement[j,:]))
    
    # Normalize covariance to get correlation matrix
    std = np.sqrt(np.diag(covariance))
    correlation = covariance / np.outer(std, std)
    
    return correlation

def plot_dccm(correlation_matrix, output_file='dccm.png'):
    """
    Plot Dynamical Cross-Correlation Matrix as a heatmap.
    
    Parameters:
    correlation_matrix (np.ndarray): DCCM matrix to plot
    output_file (str): Output file name (default: 'dccm.png')
    """

    plt.figure(figsize=(10, 8))
    # Create the heatmap and assign the image object to 'im'
    im = plt.imshow(correlation_matrix, cmap='YlGn', vmin=-1, vmax=1)
    
    # Add color bar
    cbar = plt.colorbar(im)
    cbar.set_label('Correlation Coefficient', fontsize=13, weight='bold')
    cbar.ax.tick_params(labelsize=12)  # Adjust tick label font size

    # Set labels for axes
    plt.xlabel('Residue Index', weight='bold', fontsize=13)
    plt.ylabel('Residue Index', weight='bold', fontsize=13)
    plt.xticks(fontsize=13, weight='bold')
    plt.yticks(fontsize=13, weight='bold')
    
    # Optional: Apply bold font weight to the tick labels
    for label in cbar.ax.get_yticklabels():
        label.set_fontweight('bold')  # Set tick labels fontweight
    
    # Save the figure
    plt.savefig(output_file, dpi=900)
    plt.close()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python dccm_analysis.py <topology_file> <trajectory_file>")
        sys.exit(1)
    
    topology_file = sys.argv[1]
    trajectory_file = sys.argv[2]
    
    print("Calculating DCCM...")
    dccm = calculate_dccm(topology_file, trajectory_file)
    
    print("Plotting DCCM...")
    plot_dccm(dccm)
    
    print("DCCM calculation complete. Results saved to 'dccm.png'")