"""
class ( for objects) and functions for Objects_and_functions_Cantilever_beam
FE code for T3 simple mesh
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse as sps
import numpy.linalg as npl


# =============================================================================
#%% Mesh class
# =============================================================================

class Mesh:
    def __init__(self,mshfile,dim=2):
        self.filename = mshfile
        self.dim = dim
        self.e, self.n = self.ReadMSH(self.dim)
        self.nn = self.n.shape[0]
        self.ndof = self.dim * self.nn
        
                
    def ReadMSH(self,dim):
        '''
        Reads .msh ASCII2 file and creates a mesh object (created thanks to this class)
        inspired from pyxel.py, Jean-Charles Passieux's Github
        https://github.com/jcpassieux
        '''
        file = open(self.filename, 'r')
        line = file.readline()
        # Nodes detection
        while(line.find("$Nodes") < 0):
            line = file.readline()
            pass
        line = file.readline()
        nnodes = int(line)
        nodes=np.zeros((nnodes,3))        
        for jn in range(nnodes):
            coord = file.readline().split()
            nodes[jn]=np.double(coord[1:])
        # Elements detection
        while(line.find("$Elements") < 0):
            line = file.readline()
            pass
        line = file.readline()
        nelems = int(line)
        elems=dict()
        ne=0
        for je in range(nelems):
            line=np.int32(file.readline().split())
            if line[1]==2:  #tri3
                elems[ne]=np.append(line[1],line[5:]-1)
                ne+=1
        # remove 3rd node coordinate if dim=2
        if dim==2:
            nodes=np.delete(nodes,2,1)
        return elems, nodes
 
    
    def Plot(self,newfigure=True,U=None):
        '''Plots (only the nodes of) the mesh.
        It is possible to write code to plot the elements (see e.g. https://github.com/jcpassieux )'''
        if newfigure:
            plt.figure()
        plt.plot(self.n[:,0],self.n[:,1],'ko')
        plt.axis('equal')
        #TODO : plot deformed mesh
        if not np.sum(U)==None:
            plt.plot(self.n[:,0]+U[:self.nn],self.n[:,1]+U[self.nn:],'bo')
        
        
    def K_matrix(self,hooke):
        """
        Since we only use T3 elements, here is a simplified code for this special case
        """
        # initialization of sparse matrix K
        data = np.array([])
        line = np.array([],dtype='int')
        column = np.array([],dtype='int')
        # Loop on elements to compute elementary stiffness matrices
        for ie in range(len(self.e)):
            # from physical element to reference element : Jacobian matrix
            J = np.array([[(self.n[self.e[ie][1],0]-self.n[self.e[ie][3],0]), (self.n[self.e[ie][2],0]-self.n[self.e[ie][3],0])],\
                           [(self.n[self.e[ie][1],1]-self.n[self.e[ie][3],1]), (self.n[self.e[ie][2],1]-self.n[self.e[ie][3],1])]])
            # matrix of Lagrange functions derivatives _ for t3 meshes it does not depend x, but it does for other meshes
            dN1dxi = np.array([1,0]); dN2dxi = np.array([0,1]); dN3dxi = np.array([-1,-1])
            dN1dx = npl.solve(J.T,dN1dxi); dN2dx = npl.solve(J.T,dN2dxi); dN3dx = npl.solve(J.T,dN3dxi)
            Be = np.array([[dN1dx[0],dN2dx[0],dN3dx[0],0,0,0],\
                           [0,0,0,dN1dx[1],dN2dx[1],dN3dx[1]],\
                           [dN1dx[1],dN2dx[1],dN3dx[1],dN1dx[0],dN2dx[0],dN3dx[0]]],dtype='float64')
            Be[-1] *= np.sqrt(2)/2 # w.r.t. chosen convention / see Hooke function
            # jacobian matrix determinant _ for t3 meshes it does not depend x, but it does for other meshes
            detJ = J[0,0]*J[1,1]-J[0,1]*J[1,0]
            # Gauss weight for a single Gauss point in a triangle
            w = 1/2
            # Elementary stiffness / no sum because only 1 Gauss point
            Ke = Be.T @ hooke @ Be * abs(detJ) * w
            
            # Filling K (sparse coo matrix)
            data = np.append(data,Ke.ravel())
            Ke_dof = np.r_[self.e[ie][1:],self.e[ie][1:]+self.nn]  # np.r_ and np.append do the same thing here
            line = np.append(line,np.repeat(Ke_dof,Ke.shape[0]))
            column = np.append(column,np.tile(Ke_dof,Ke.shape[0]))
        # Constructing K
        K = sps.csc_matrix((data,(line,column)),shape=(self.ndof,self.ndof))
        return K






# =============================================================================
#%% Other functions
# =============================================================================

def Hooke(E,nu):
    """Returns Hooke matrix for plane stress
    Chosen convention : (eps_xx, eps_yy, sqrt(2) eps_xy) and (sig_xx, sig_yy, sqrt(2) sig_xy) Voigt notation
    """
    terme1 = E/(1-nu**2)
    H = np.array([[terme1, terme1*nu, 0], [terme1*nu, terme1, 0], [0,0,E/(1+nu)]])
    return H
    

    
















