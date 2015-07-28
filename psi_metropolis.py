import time
import psi4
from p4util.util import *
import numpy as np
from header import header
from numpy2psi import numpy2psi
from rand_displacement import rand_displacement
from acceptance_check import acceptance_check
import random as rand
#from scipy import linalg as SLA
np.set_printoptions(precision=5, linewidth=200, suppress=True)

# Memory for numpy in GB
numpy_memory = 2

hartree2eV = 27.2107

def monte_carlo(mol, method, temperature, max_step, total_mc_moves):	
	# Import MintsHelper
	# mints = MintsHelper()

	# Open Up Trajectory File for storing vizualization
	create_trajectory = open("trajectory.xyz" , "w+")
	mc_output = open("mc_output.dat", "w+")
	header(mc_output)
	mc_output.close()

	# Calculate initial energy from given geometry
	for mc_iteration in range(total_mc_moves):
		psi4.set_active_molecule(mol)
		E1 = psi4.scf()
		coords = mol.save_string_xyz()
		coordinates = coords.split()
	        # Deleting charge and multiplicity from the array of coordinates
		del coordinates[0] #Deletes Charge
		del coordinates[0] #Deletes Multiplicity


		natoms = mol.natom() #Number of Atoms
		labels = [] #Store labels (used in print statements)

		# Store the coordinates in an natoms x 3 matrix, this makes it easier
		# to assign the Monte Carlo displacements later
		Old_Geometry = np.zeros( (natoms,3) )
		New_Geometry = np.zeros( (natoms,3) )
		for i in range(natoms):
			labels.append(coordinates[i*3+i])
			for j in range(3):
				Old_Geometry[i][j] = float(coordinates[(i*3+i) + (j+1)])
				New_Geometry[i][j] = float(coordinates[(i*3+i) + (j+1)])

		# Execute Metropolis Monte-Carlo displacements on a random coordinate and 
		# return the updated geometry.
		New_Geometry = rand_displacement(natoms, max_step, mc_iteration, labels, New_Geometry, Old_Geometry)

		# Convert Numpy Matrices to Psi4 input using "numpy2psi" function and a function
		# from the Molecule class in Psi4. 
		Psi_Geometry_New_String,Psi_Geometry_Old_String = numpy2psi(natoms, labels, New_Geometry,Old_Geometry) #Conversion
		new_mol = psi4.Molecule.create_molecule_from_string(Psi_Geometry_New_String) #New Coordinates
		old_mol = psi4.Molecule.create_molecule_from_string(Psi_Geometry_Old_String) #Old Coordinates

		#print("New Coordinate Matrix: \n %s" %New_Geometry)

		mc_out = open("mc_output.dat" , "a")
		mc_out.write("Current MC Move: \n Geometry from iteration: %d \n %s \n" %(mc_iteration,Old_Geometry))
		mc_out.write("\n Attempted Geometry Move: %d \n %s \n" %(mc_iteration+1,New_Geometry))

		# Activate the Molecule object created from the new coordinates
		# and run the QM method on it
		psi4.set_active_molecule(new_mol)
		E2 = psi4.scf()

		mc_out.write("%s energy with old geometry: %f\n" %(method,E1))
		mc_out.write("%s energy with new geometry: %f\n" %(method,E2))

		Energy_Difference = E2 - E1
		mc_out.write("energy difference: %f\n" %(Energy_Difference))
		Energy_Difference_eV = Energy_Difference*hartree2eV
		#mol = acceptance_check(Energy_Difference,temperature, new_mol, old_mol, natoms, mc_iteration)  
		Boltz = np.exp(- Energy_Difference/(8.617e-5 * temperature))
		R = rand.random()
		trajectory_file = open("trajectory.xyz" , "a")
		if (abs(Energy_Difference) >= 1e-10):
			mc_out.write("\n Significant Change in Energy Performing acceptance check (R = %f) \n" %R)
			if (Boltz > R):
				mc_out.write("Coordinates Accepted: Using New Coordinates for Next Monte Carlo Run \n")
				mol = new_mol
				trajectory_file.write("%d \n" %natoms)
				trajectory_file.write("Step %d of Psi4 Monte-Carlo Simulation (Coordinates Updated) \n" %(mc_iteration))
				for i in range(natoms):
					trajectory_file.write("%s  " %labels[i])
					for j in range(3):
						if (j == 2):
							trajectory_file.write("    %f \n" %(New_Geometry[i][j]))
						else:
							trajectory_file.write("    %f" %(New_Geometry[i][j]))
			else:
				mc_out.write("Coordinates Denied: Repeating Monte Carlo Run With Coordinates From Previous Run \n")
				mol = old_mol
		else:
			mc_out.write("No Change in Energy: Repeating Monte Carlo Run With Old Coordinates \n")
			mol = old_mol
		trajectory_file.close()
		mc_out.close()
