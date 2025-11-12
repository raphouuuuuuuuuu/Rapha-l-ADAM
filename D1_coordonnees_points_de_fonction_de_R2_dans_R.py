
#Pointage des figures 3D (à mettre sous forme de matrices)

import matplotlib.pyplot as plt
import numpy as np

#Définition de la fonction de R2 dans R
def f(x,y):
  return np.sin(np.sqrt(x**2 + y**2))

def bouclier(X, Y, r=125, z_center=-100):
  d2 = X**2 + Y**2
  inside = d2 <= r**2
  Z = np.zeros_like(X, dtype=float)
  Z[inside] = z_center + np.sqrt(r**2 - d2[inside])
  Z[Z < 0] = 0  # on limite à z >= 0 (portion visible)
  return Z

#Représentation de la fonction sous forme de nappe
def representation_surface(fonction):
  x, y = np.meshgrid(np.linspace(-5, 5, 100), np.linspace(-5, 5, 100))

  fig = plt.figure(figsize=(14, 7))

  # graphique (surface)
  ax = fig.add_subplot(1, 2, 2, projection="3d")
  ax.plot_surface(x, y, fonction(x,y), cmap="viridis")
  ax.set_title("Graphique en surface")

  plt.show()

#representation_surface(f)

taille_matrice = 9
#Passer de la fonction f aux matrices
def matrices(fonction) :
    mat_x = np.array([range(-80,100,20) for i in range(taille_matrice)])
    mat_y = np.array([range(80,-100,-20) for i in range(taille_matrice)]).T
    mat_z = fonction(mat_x,mat_y)
    return(mat_x,mat_y,mat_z)
  

mat_x = matrices(f)[0]
mat_y = matrices(f)[1]
mat_z = matrices(f)[2]

def representation_nuage(matrice_x, matrice_y, matrice_z) : 
  x, y = np.meshgrid(np.linspace(-4, 5, 100), np.linspace(-4, 5, 100))
  fig = plt.figure(figsize=(14, 7))
  ax = fig.add_subplot(1, 2, 2, projection="3d")
  ax.scatter(matrice_x, matrice_y, matrice_z, color="red")
  plt.show()

#representation_nuage(mat_x, mat_y, mat_z)


def superposition_nuage_nappe(matrice_x, matrice_y, matrice_z, fonction) : 
  x, y = np.meshgrid(np.linspace(-4, 5, 100), np.linspace(-4, 5, 100))
  fig = plt.figure(figsize=(14, 7))
  ax = fig.add_subplot(1, 2, 2, projection="3d")
  ax.plot_surface(x, y, fonction(x,y), cmap="viridis")
  ax.scatter(matrice_x, matrice_y, matrice_z, color="red")
  plt.show()


#superposition_nuage_nappe(mat_x, mat_y, mat_z, f)
