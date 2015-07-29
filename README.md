![Psi-Metropolis](media/artworkthechase.png)
=============

#####Author: Wallace D. Derricotte
#####Contact: wallace.derricotte@emory.edu

Psi-Metropolis is an implementation of Metropolis Monte-Carlo for the purpose of sampling different molecular configurations, written
entirely in python and integrated into the PSI4 ab-initio quantum chemistry package. Psi-Metropolis is made possible by recent work
to bridge together the python and C side of PSI4, spearheaded by Daniel G. A. Smith at Auburn University. I will add more features to
Psi-Metropolis over time as I have a need for them

The current Metropolis Monte Carlo algorithm does the following:

1. User specifies initial atom position. Coordinates can be specified in any format (Z-Matrix, Internal, or XYZ) however the algorithm deals
specifically with the xyz coordinates after the intial input. An SCF calculation is performed at this geometry.

2. A random atom is selected and is then moved by a random displacement in the x, y, and z direction. The largest possible magnitude of this displacement is 
chosen by the user provided maximum step size (max_step).

3. The SCF in PSI4 is called again to perform an SCF calculation at the displaced geometry.

4. If the change in the SCF energy is greater than zero then a random number R is selected within a range of [0,1] in order to determine whether or not to accept
this trajectory for the next Monte Carlo run.

5. If the Boltzmann factor (ratio of the two Boltzmann distributions) is greater than the random number then generated in step 4 then the geometry is accepted, otherwise we maintain the previous geometry. The user can specify a temperature, effectively changing the width of the Boltzmann distribution, allowing more geometries to be accepted. 

6. After the geometry for the next run is chosen, we return to step 2.

Example Input:
```
import time
import psi4
import numpy as np
from psi_metropolis import monte_carlo

molecule mol {
O
H 1 1.1
H 1 1.1 2 104.5
symmetry c1
}

set {
basis cc-pVDZ
scf_type pk
e_convergence 1e-8
}

monte_carlo(mol, "rhf", 275.15, 0.05, 20) #Function args are (Molecule(psi_molecule_object), Method(string), Temperature(float), Max_Step_Size(float), Total_Attempts(int))

``` 
