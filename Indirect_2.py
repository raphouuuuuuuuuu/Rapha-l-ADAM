#partie 6.2 

'''on cherche a résoudre (trouver X) tel que MX = O 
   et Mi = produit vectoriel des points sur l'image et de Pi
   et M = [M1,M2...] transposé  '''
'''
PARTIE 6.2 – Triangulation linéaire par produit vectoriel et SVD

On cherche à reconstruire un point 3D X à partir de ses projections dans plusieurs images.

Données :
- P_i : matrice de projection de la caméra i (3x4)
- n_i : coordonnées homogènes du point détecté dans l’image i (3x1)

Étapes :
1. Pour chaque image i :
   - On calcule la matrice antisymétrique [n_i]^∧ correspondant au produit vectoriel.
   - On construit M_i = [n_i]^∧ · P_i  → matrice 3x4
   - On garde uniquement les 2 premières lignes indépendantes de M_i → M_i ∈ ℝ^{2×4}

2. On empile verticalement toutes les M_i :
   M = [M_1 ; M_2 ; ... ; M_n] ∈ ℝ^{2n×4}

3. On résout M · X = 0 via SVD :
   - M = U · Σ · V^T
   - On récupère la dernière ligne de V^T (i.e. le vecteur associé à la plus petite valeur singulière)
   - C’est la solution homogène X ∈ ℝ^4 telle que M · X ≈ 0

4. On divise X par sa dernière coordonnée pour obtenir le point 3D en coordonnées cartésiennes (X, Y, Z)

Résultat :
- X_homogène : coordonnées homogènes du point 3D
- X_cartésien : coordonnées cartésiennes du point 3D (X, Y, Z)
'''

import numpy as np
import matplotlib.pyplot as plt

points_3D = []

# Produit vectoriel sous forme matricielle
def produit_vectoriel(n):
    return np.array([
        [0, -n[2], n[1]],
        [n[2], 0, -n[0]],
        [-n[1], n[0], 0]
    ])

# Construction de M_i = [n_i]^ ∧ . P_i
def M_i(n_i, P_i):
    vect = produit_vectoriel(n_i)
    M_i_3 = vect @ Pi
    return M_i_3[:2]  # On garde seulement 2 lignes indépendantes

# Triangulation d'un point à partir de plusieurs observations
def triangulate_point(P_Mat, n_list):
   """
    Reconstruit un point 3D à partir de ses projections dans plusieurs images.

    Paramètres :
    - P_Mat : liste de matrices de projection (3x4) pour chaque caméra
    - n_list : liste des points projetés (coordonnées homogènes 3x1) dans chaque image

    Étapes :
    1. Pour chaque image, on construit une matrice M_i = [n_i]^∧ * P_i et on en extrait deux lignes indépendantes.
    2. On empile tous les M_i verticalement pour former une grande matrice M.
    3. On résout M · X = 0 par SVD : X est le vecteur homogène associé à la plus petite valeur singulière.
    4. On retourne les coordonnées cartésiennes du point 3D en normalisant X.

    Retour :
    - X_cartesien : tableau (4,) représentant les coordonnées homogénéisées du point 3D
    """
    M_list = [M_i(n_i, P_i) for n_i, P_i in zip(n_list, P_Mat)]
    M = np.vstack(M_list)
    U, S, Vt = np.linalg.svd(M)
    X_homogene = Vt[-1]
    X_cartesien = X_homogene / X_homogene[-1]
    return X_cartesien



def triangulate_multiple_points(P_Mat, n_points_list):
    """
    P_list : liste des matrices de projection (une par image)
    n_points_list : liste contenant, pour chaque image, une liste de points projetés (n x 3 homogène)

    ATTENTION : chaque point doit avoir une correspondance sur toutes les images.
    """
    num_points = len(n_points_list[0])  # Nombre de points à trianguler

    for i in range(num_points):
        n_list = [n_points[i] for n_points in n_points_list]  # On rassemble le i-ème point sur toutes les images
        X = triangulate_point(P_Mat, n_list)
        points_3D.append(X)



# Projection d’un ensemble de points 3D sur une caméra
def project_points(P, points_3D):
    projections = []
    for X in points_3D:
        x = P @ X
        x = x / x[2]  # homogénéisation
        projections.append(x)
    return projections



# Affichage des points 3D
def plot_points(points_3D):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for point in points_3D:
        ax.scatter(point[0], point[1], point[2], c='r', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Points en 3D')
    plt.show()


