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


X = matrices(fonction)[0] #matrice des coord x des points objets par la fonction Q1
Y = matrices(fonction)[1] #matrice des coord y des points objets par fonction Q1
Z = matrices(fonction)[2] #matrice des coord z des points objets par fonction Q1
#print(X,Y,Z)

# Paramètres de la caméra (exemple : iPhone 15)
f = 3.99  # Focale en mm
taille_pixel = 1.22e-3  # Taille de pixel en mm (approximatif, à vérifier)
taille_capteur = (4032, 3024)  # Taille du capteur en pixels

#positions caméras(exemples)
angles_list : List[List] = [np.array([0, -45, -45]),
                            np.array([0, -30, 60]),
                            np.array([0, -30,0])]

Xe_Omega_1 = np.array([[-20, 0, 330]])   # Image 1
Xe_Omega_2 = np.array([[-20, -10, 370]])  # Image 2
Xe_Omega_3 = np.array([[-20, 0, 320]])    # Image 3
positions : List[List] = np.array([Xe_Omega_1,Xe_Omega_2,Xe_Omega_3])



# Boucle pour le calcul des matrices de projection : liste de liste

for i in range(len(angles_list)): #pour chaque prise de vue
    ang = angles_list[i] #on sort l'angle de la prise de vue
    Xe_cam = positions[i] #on sort la position de la caméra (en base caméra)
    R = matrice_rotation(ang) #calcul de la matrice de rotation à partir des angles (matrice chgmt de base objet -> base image)
    R_inv = np.linalg.inv(R) #matrice rotation inversée pour passer de la base image en base objet
    Xe_obj = np.dot(R_inv, np.reshape(Xe_cam, (3,1))) #on passe le vecteur position caméra en base objet
    Pth = matrice_projection(f, taille_pixel, taille_capteur, R, Xe_obj) #calcul de la matrice de projection perspective

    p, q = coordImages(X, Y, Z, Pth) #calcul des coord images des différents points
    p, q = np.flipud(p), np.flipud(q) #on inverse les axes pour correspondre au poly
    p_arrondi, q_arrondi = np.around(p), np.around(q) #on arrondi au pixel près
    print(p_arrondi, q_arrondi)

    #affichage des points sur le capteur de la caméra
    plt.axis("equal")
    plt.axis([0, 4032, 3064, 0])
    plt.xlabel("q [pixel]")
    plt.ylabel("p [pixel]")
    plt.title("Angle caméra (°): " + str(ang) + " ; Position caméra (mm): " + str(Xe_cam))
    plt.scatter(q_arrondi, p_arrondi)
    plt.show()





    












"""


#Code de calcul : Utiliser contrainte de colinéarité pour avoir les coordonnées image
#des points de calibrations et des points de mesures pour chaque image

####A REVOIR CAR CODE INCOMPLET#####
import numpy as np
import matplotlib.pyplot as plt
import cv2


points_2D= [p,q]


def afficher_points(chemin_image,points_2D, title="Projection des points"):
     Affiche une image avec les points projetés en 2D.
Entrées:
  X matrice des coord x des points objets par fonction Q1
  Y matrice des coord y des points objets par fonction Q1
  Z matrice des coord z des points objets par fonction Q1
  P matrice proj perspective trouvée par fonction Q4
Sorties:
  p matrice des coord p des points images 
  q matrice des coord q des points images 

    # Chargement de l'image
    img = cv2.imread(chemin_image)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Affichage de l'image
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    
    # Superposer les points projetés
    points_2D = np.array(points_2D)  # Conversion en tableau numpy
    plt.scatter(points_2D[:, 0], points_2D[:, 1], c='r', marker='o', label="Points projetés")
    
    # Personnalisation
    plt.legend()
    plt.title(title)
    plt.xlabel("u (pixels)")
    plt.ylabel("v (pixels)")
    plt.gca().invert_yaxis()  # Inverser l'axe Y pour correspondre au repère image
    plt.show()

# Exemple de points projetés (u, v) en pixels
points_exemple = [(500, 600), (1200, 800), (1500, 1000), (2000, 1200)]

# Appel de la fonction avec une image de test
afficher_points("image_test.jpg", points_exemple)
"""
