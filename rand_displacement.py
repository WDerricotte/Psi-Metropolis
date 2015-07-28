import time
import psi4
import numpy as np
import random as rand

def rand_displacement(natoms, max_step, mc_iteration, labels, New_Geometry, Old_Geometry):
	# Choose Random Atom
	rand_atom = rand.randint(0 , natoms-1)
	
	# Choose 3 random numbers within +/- the given 
	# maximum step size allowing full range of movement
	# over coordinate space.
        rand_disp_x = rand.uniform(-max_step , max_step)
        rand_disp_y = rand.uniform(-max_step , max_step)
        rand_disp_z = rand.uniform(-max_step , max_step)

	# Print details of the current Monte-Carlo move to the output
	mc_out = open("mc_output.dat" , "a")
        mc_out.write("-------------------------------- \n")
        mc_out.write("Metropolis Monte-Carlo Step %d \n" %(mc_iteration + 1))
        mc_out.write("-------------------------------- \n")
        mc_out.write("Currently Displacing %s by x:%f y:%f z:%f (Angstroms) \n" %(labels[rand_atom] , rand_disp_x, rand_disp_y, rand_disp_z))
	mc_out.close()
	
	# Displace old geometry by random displacements
	New_Geometry[rand_atom][0] = disp_coordx = Old_Geometry[rand_atom][0] + rand_disp_x
	New_Geometry[rand_atom][1] = disp_coordy = Old_Geometry[rand_atom][1] + rand_disp_y
	New_Geometry[rand_atom][2] = disp_coordz = Old_Geometry[rand_atom][2] + rand_disp_z

	return (New_Geometry)
