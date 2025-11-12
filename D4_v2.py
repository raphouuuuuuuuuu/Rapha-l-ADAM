from typing import List
import numpy as np
import matplotlib.pyplot as plt
from D3_coord_image_avec_contrainte_colin import coordImages
from D2_matrices_projection_et_rotation import matrice_projection, matrice_rotation
from D1_coordonnees_points_de_fonction_de_R2_dans_R import matrices


### Données
def fonction(X, Y, r=125, z_center=-100):
  d2 = X**2 + Y**2 
  inside = d2 <= r**2
  Z = np.zeros_like(X, dtype=float)
  Z[inside] = z_center + np.sqrt(r**2 - d2[inside])
  Z[Z < 0] = 0  # on limite à z >= 0 (portion visible)
  return Z

  
def prog_direct(X,Y,Z):
    # Paramètres de la caméra (exemple : iPhone 15)
    f = 3.99  # Focale en mm
    taille_pixel = 1.22e-3  # Taille de pixel en mm (approximatif, à vérifier)
    taille_capteur = (4032, 3064)  # Taille du capteur en pixels

    #positions caméras(exemples)
    angles_list : List[List] = [np.array([0, -45, -45]),
                                np.array([0, -30, 60]),
                                np.array([0, -30,0])]

    Xe_Omega_1 = np.array([[-20, 0, 330]])   # Image 1
    Xe_Omega_2 = np.array([[-20, -10, 370]])  # Image 2
    Xe_Omega_3 = np.array([[-20, 0, 320]])    # Image 3
    positions : List[List] = np.array([Xe_Omega_1,Xe_Omega_2,Xe_Omega_3])



    # Boucle pour le calcul des matrices de projection : liste de liste
    def Calcul_coords_image(X, Y, Z, angles_list, positions,i: int ):
        
        ang = angles_list[i] #on sort l'angle de la prise de vue
        Xe_cam = positions[i] #on sort la position de la caméra (en base caméra)
        R = matrice_rotation(ang) #calcul de la matrice de rotation à partir des angles (matrice chgmt de base objet -> base image)
        R_inv = np.linalg.inv(R) #matrice rotation inversée pour passer de la base image en base objet
        Xe_obj = np.dot(R_inv, np.reshape(Xe_cam, (3,1))) #on passe le vecteur position caméra en base objet
        Pth = matrice_projection(f, taille_pixel, taille_capteur, R, Xe_obj) #calcul de la matrice de projection perspective

        p, q = coordImages(X, Y, Z, Pth) #calcul des coord images des différents points
        p_arrondi, q_arrondi = np.around(p), np.around(q) #on arrondi au pixel près
        return np.flipud(p_arrondi), np.flipud(q_arrondi)

    #On va stocker les Mats p_arr et q_arr dans les arrays Xp et Xq pour permettre un traitement plus simple
    p_0,q_0 = Calcul_coords_image(X, Y, Z, angles_list, positions,0)
    Xp = np.array([p_0]) #on initialise Xp avec les coordonnées de la première image
    Xq = np.array([q_0]) #on initialise Xq avec les coordonnées de la première image
    
    for i in range(1,len(angles_list)): #pour chaque prise de vue
        p_i,q_i = Calcul_coords_image(X, Y, Z, angles_list, positions,i)
        Xp = np.append(Xp, np.array([p_i]), axis=0)
        Xq = np.append(Xq, np.array([q_i]), axis=0)
    
    return Xp, Xq #on retourne les coordonnées de tous les points sur toutes les images
