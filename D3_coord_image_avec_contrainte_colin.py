#calcul des points image à partir des points objets et des matrices de projections perspectives.
#on utilise la relation (15) page 9 "n = PX", sachant que P est codé en code Q4

import numpy as np

def coordImages(X, Y, Z, P):
  """
  Entrées
  X matrice des coord x des points objets par fonction Q1
  Y matrice des coord y des points objets par fonction Q1
  Z matrice des coord z des points objets par fonction Q1

  P matrice proj perspective trouvée par fonction Q4

  Sorties
  p matrice des coord p des points images 
  q matrice des coord q des points images 
  """
  
  p = np.zeros(np.shape(X)) #création de la matrice qui aura les coord p des pnts images
  q = np.zeros(np.shape(X)) #création de la matrice qui aura les coord q des pnts images

  for i in range (np.shape(X)[0]) : 
    for j in range (np.shape(X)[1]) : #pour chaque point (donc chaque coordonnées)
      Xvect = np.array([[X[i,j]], [Y[i,j]], [Z[i,j]], [1]]) #on recrée le vecteur associé à chaque point (le 1 correspond au paramètre T qui n'est pas utile dans le pb direct)
      n = np.dot(P, np.reshape(Xvect, (4, 1))) #on utilise l'équation (15) page 9 pour avoir les coordonnées des points images en coordonées homogènes (vecteur 3*1)
     
      p[i,j] = n[0] / n[2] #chaque coord est divisée par le paramètre t (n[2]) afin de passer en coordonnées cartésiennes, et est rentrée dans le tableau correspondant 
      q[i,j] = n[1] / n[2] 
 
  return p, q
    

