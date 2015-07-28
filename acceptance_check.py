import time
import psi4
import numpy as np
import random as rand

def acceptance_check(Energy_Difference, temperature, new_mol, old_mol, natoms, mc_iteration):
	Boltz = np.exp(- Energy_Difference/(8.617e-5 * temperature))
        R = rand.random()
	mc_out = open("mc_output.dat" , "a")
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
