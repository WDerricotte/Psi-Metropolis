
import time
import psi4
import numpy as np

def header(outfile):
	outfile.write(" --------------------------------------------------------------------------- \n")
	outfile.write("  PsiMetropolis: Implementation of Metropolis Quantum Monte-Carlo for Psi4   \n")
	outfile.write("                   Code Author: Wallace D. Derricotte                        \n \n")
	outfile.write("  Description: Tool for performing on-the-fly Metropolis Monte-Carlo         \n")
	outfile.write("  simulations for the purpose of sampling molecular geometries using         \n")
	outfile.write("  pre-existing ab-inito methods in Psi4 to compute the necessary             \n")
	outfile.write("  energy gradients.                                                          \n")
	outfile.write(" --------------------------------------------------------------------------- \n")

