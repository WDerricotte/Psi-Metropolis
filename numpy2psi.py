import time
import psi4
import numpy as np

def numpy2psi(natoms, labels, New_Geometry, Old_Geometry):
	Psi_Geometry_New = []
        for i in range(natoms):
                Psi_Geometry_New.append("%s" %labels[i])
                for j in range(3):
                        if (j == 2):
                                Psi_Geometry_New.append("    %f \n" %(New_Geometry[i][j]))
                        else:
                                Psi_Geometry_New.append("    %f" %(New_Geometry[i][j]))
        Psi_Geometry_Old = []
        for i in range(natoms):
                Psi_Geometry_Old.append("%s" %labels[i])
                for j in range(3):
                        if (j == 2):
                                Psi_Geometry_Old.append("    %f \n" %(Old_Geometry[i][j]))
                        else:
                                Psi_Geometry_Old.append("    %f" %(Old_Geometry[i][j]))

        # Add the miscellaneous stuff at the bottom of the strings.
        Psi_Geometry_New.append("symmetry c1 \n")
        Psi_Geometry_New.append("units ang \n")
        Psi_Geometry_New.append("no_reorient \n") #VERY IMPORTANT: Psi4 will reorient your molecule unless you tell it not to!!
        Psi_Geometry_New.append("nocom")

        Psi_Geometry_Old.append("symmetry c1 \n")
        Psi_Geometry_Old.append("units ang \n")
        Psi_Geometry_Old.append("no_reorient \n") #VERY IMPORTANT: Psi4 will reorient your molecule unless you tell it not to!!
        Psi_Geometry_Old.append("nocom")

        # Join the list of strings into one single string, the function
        # create_molecule_from_string will turn this into a molecule
        # object for the next run
	Psi_Geometry_New_String = "".join(Psi_Geometry_New)
	Psi_Geometry_Old_String = "".join(Psi_Geometry_Old)

	return (Psi_Geometry_New_String, Psi_Geometry_Old_String)
