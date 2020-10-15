"""
Spline definition : strongly inspired from INSA course on splines (3MIC)
DraggablePoints class : strongly inspired from https://stackoverflow.com/questions/21654008/matplotlib-drag-overlapping-points-interactively
"""


import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import numpy as np


### spline evaluation
def eval_spline(xeval,x,sigma,sigma_prime,sigma_seconde,sigma_tierce) :
    n = len(x)-1
    j = -1; A = sigma[0]; B = sigma_prime[0]; C = 0; D = 0
    Sigmaxx = np.zeros_like(xeval)
    ieval = 0
    for xeval1pt in xeval:
        while j<n and xeval1pt>=x[j+1]:
            j+=1
            A = sigma[j]
            B = sigma_prime[j]
            C = sigma_seconde[j]/2
            D = sigma_tierce[j]/6
        h = xeval1pt-x[max(0,j)]
        Sigmaxx[ieval] = A + h*(B + h*(C + h*D))
        ieval+=1
    return Sigmaxx
   
    

class DraggablePoints(object):
    """inspired from https://stackoverflow.com/questions/21654008/matplotlib-drag-overlapping-points-interactively"""
    def __init__(self, artists,ax,neval,courbePeriodique, tolerance=5):
        
        self.courbePeriodique = courbePeriodique
        self.neval = neval

        ## Lecture des donnees ##
        X = []
        Y = []
        for artist in artists:
            artist.set_picker(tolerance)
            x,y = artist.center
            X+=[x]; Y+=[y]
        X = np.array(X); Y = np.array(Y);
        
        self.n = len(X)-1


        
        ## Calcul de la spline aux points d'evaluation ##
        
        if courbePeriodique == 1 :  # prolongement "périodique"
             X = np.r_[X[-2],X,X[1],X[2]]
             Y = np.r_[Y[-2],Y,Y[1],Y[2]]
        else :                      # prolongement "spline naturelle"
             X = np.r_[2*X[0]-X[1],X,2*X[-1]-X[-2],3*X[-1]-2*X[-2]]
             Y = np.r_[2*Y[0]-Y[1],Y,2*Y[-1]-Y[-2],3*Y[-1]-2*Y[-2]]
        
        h = 1 # car t = np.arange(0,n+1) : pas de 1

        sigma_x = (X[2:-1] + 4*X[1:-2] + X[:-3])/6
        sigmaPrime_x = (X[2:-1] - X[:-3])/(2*h)
        sigmaSeconde_x = (X[2:-1] - 2*X[1:-2] + X[:-3])/h**2
        sigmaTierce_x = (X[3:] - 3*X[2:-1] + 3*X[1:-2] - X[:-3])/h**3
        
        sigma_y = (Y[2:-1] + 4*Y[1:-2] + Y[:-3])/6
        sigmaPrime_y = (Y[2:-1] - Y[:-3])/(2*h)
        sigmaSeconde_y = (Y[2:-1] - 2*Y[1:-2] + Y[:-3])/h**2
        sigmaTierce_y = (Y[3:] - 3*Y[2:-1] + 3*Y[1:-2] - Y[:-3])/h**3

        t_eval = np.linspace(0,self.n,neval)
        t = np.arange(0,self.n+1)
        X_graphe = eval_spline(t_eval,t,sigma_x,sigmaPrime_x,sigmaSeconde_x,sigmaTierce_x)
        Y_graphe = eval_spline(t_eval,t,sigma_y,sigmaPrime_y,sigmaSeconde_y,sigmaTierce_y)
        
        ## fin ##
               


        
        self.artists = artists
        self.currently_dragging = False
        self.current_artist = None
        self.offset = (0, 0)
        self.drawing = Line2D(X_graphe,Y_graphe,color='black')
        self.ax = ax
        self.ax.add_line(self.drawing)

        for canvas in set(artist.figure.canvas for artist in self.artists):
            canvas.mpl_connect('button_press_event', self.on_press)
            canvas.mpl_connect('button_release_event', self.on_release)
            canvas.mpl_connect('pick_event', self.on_pick)
            canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        self.currently_dragging = True

    def on_release(self, event):
        self.currently_dragging = False
        self.current_artist = None

    def on_pick(self, event):
        if self.current_artist is None:
            self.current_artist = event.artist
            x0, y0 = event.artist.center
            x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
            self.offset = (x0 - x1), (y0 - y1)

    def on_motion(self, event):
        if not self.currently_dragging:
            return
        if self.current_artist is None:
            return
        dx, dy = self.offset
        self.current_artist.center = event.xdata + dx, event.ydata + dy
        self.current_artist.figure.canvas.draw()
        X = []
        Y = []
        for artist in self.artists:
            x,y = artist.center
            X+=[x]; Y+=[y]
        X = np.array(X); Y = np.array(Y); 
        
 

       
        ## Calcul de la spline aux points d'evaluation ##
        
        if self.courbePeriodique == 1 :  # prolongement "périodique"
             X = np.r_[X[-2],X,X[1],X[2]]
             Y = np.r_[Y[-2],Y,Y[1],Y[2]]
        else :                      # prolongement "spline naturelle"
             X = np.r_[2*X[0]-X[1],X,2*X[-1]-X[-2],3*X[-1]-2*X[-2]]
             Y = np.r_[2*Y[0]-Y[1],Y,2*Y[-1]-Y[-2],3*Y[-1]-2*Y[-2]]
        
        h = 1 # car t = np.arange(0,n+1) : pas de 1

        sigma_x = (X[2:-1] + 4*X[1:-2] + X[:-3])/6
        sigmaPrime_x = (X[2:-1] - X[:-3])/(2*h)
        sigmaSeconde_x = (X[2:-1] - 2*X[1:-2] + X[:-3])/h**2
        sigmaTierce_x = (X[3:] - 3*X[2:-1] + 3*X[1:-2] - X[:-3])/h**3
        
        sigma_y = (Y[2:-1] + 4*Y[1:-2] + Y[:-3])/6
        sigmaPrime_y = (Y[2:-1] - Y[:-3])/(2*h)
        sigmaSeconde_y = (Y[2:-1] - 2*Y[1:-2] + Y[:-3])/h**2
        sigmaTierce_y = (Y[3:] - 3*Y[2:-1] + 3*Y[1:-2] - Y[:-3])/h**3

        t_eval = np.linspace(0,self.n,self.neval)
        t = np.arange(0,self.n+1)
        X_graphe = eval_spline(t_eval,t,sigma_x,sigmaPrime_x,sigmaSeconde_x,sigmaTierce_x)
        Y_graphe = eval_spline(t_eval,t,sigma_y,sigmaPrime_y,sigmaSeconde_y,sigmaTierce_y)
        
        ## fin ##



        self.drawing.set_data(X_graphe,Y_graphe)
#        self.ax.plot(X,Y)



def DrawModifiableSpline(X,Y,courbePeriodique):
    """X,Y coordonnées des données (points de contrôle)"""
    ### Pour créer une figure avec des échelles adaptées aux données
    fig, ax = plt.subplots()
    minX = min(X); maxX = max(X); minY = min(Y); maxY = max(Y); LLX = maxX-minX ; LLY = maxY-minY
    ax.set(xlim=[minX-LLX/10, maxX+LLX/10], ylim=[minY-LLY/10, maxY+LLY/10])
    Rc = min([LLX,LLY])/40
    
    ### Création des points modifiables
    circles = []
    for nn in range(len(X)):
        circles+=[patches.Circle((X[nn], Y[nn]), Rc, fc='b', alpha=0.5)]
    # Ajout des points sur la figure    
    for circ in circles:
        ax.add_patch(circ)
    
    ### Affichage 
    neval = 200    
    dr = DraggablePoints(circles,ax,neval,courbePeriodique)
    plt.show()
    plt.axis('equal')
    return dr
        


#%% DONNEES
###############################################################################        

# flute
X = np.array([ 22., 34., 39., 39., 24., 24., 25., 39., 39., 30., 30., 14., 14., 5., 5., 19., 20., 20., 5., 5., 10., 22.])
Y = np.array([ 4.8, 4., 4., 8., 8., 8., 35., 55., 82., 99., 99., 99., 99., 82., 55., 35., 8., 8., 8., 4., 4., 4.8 ])

# verre
#X = np.array([22., 34., 39., 39., 24.8, 25., 27., 42., 42., 34.5, 34., 10., 9.5, 2., 2., 17., 19., 19.2, 5., 5., 10., 22.])
#Y = np.array([ 4.8, 4., 4., 8., 8., 9., 30., 39., 56., 68.5, 69., 69., 68.5, 56., 39., 30., 9., 8., 8., 4., 4., 4.8 ])

# aile d'avion
#X = np.array([ 42., 32., 19., 1., 1., 22., 34., 42. ])
#Y = np.array([ 1., 4., 1., 1., 8., 11., 6.5,  1.2])



### Affichage
courbePeriodique = 1
dr = DrawModifiableSpline(X,Y,courbePeriodique)



