"""
Python and (a little of) object programming
FE mesh (cantilever beam)
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse.linalg as spsl

import class_and_functions as caf


# =============================================================================
#%% Mesh creation
# =============================================================================

file_msh = 'BeamMesh.msh' # créé avec gmsh, rectangle de longueur 3 et hauteur 0.6
m = caf.Mesh(file_msh)

m.Plot()
plt.title('Mesh nodes')


# =============================================================================
#%% Mechanical parameters
# =============================================================================

E = 210e9
nu = 0.
hooke = caf.Hooke(E,nu)


# =============================================================================
#%% Boundary conditions
# =============================================================================

### left side : clamped
ls_nodes, = np.where(m.n[:,0]==0)
remaining_nodes = np.delete(np.arange(m.nn),ls_nodes)
remaining_dofs = np.r_[remaining_nodes,remaining_nodes+m.nn]

U = np.zeros(m.ndof)

### point right side down : nodal force F downward
F_value = 6.7e6
F = U.copy()

nodenumber = 57
plt.plot(m.n[nodenumber,0],m.n[nodenumber,1],'c*',label='Nodal force application')
plt.legend()
F[nodenumber+m.nn] = -F_value


# =============================================================================
#%% Rigidity operator K
# =============================================================================

K = m.K_matrix(hooke)


# =============================================================================
#%% Solving KU=F
# =============================================================================

### Removing clamped dof
K_clamped = K[remaining_dofs][:,remaining_dofs]
F_clamped = F[remaining_dofs]

### Solving 
Kc_LU = spsl.splu(K_clamped)
U[remaining_dofs] = Kc_LU.solve(F_clamped)


# =============================================================================
#%% Post processing + Plot
# =============================================================================
amp = 10 # amplification factor
m.Plot(U=amp*U)
plt.title('Nodal displacements')

