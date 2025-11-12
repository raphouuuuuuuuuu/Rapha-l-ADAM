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

def produit_vectoriel(n):
    """
    Entrée:
        * n: vecteur image sous forme homogène[p,q,t]
    """

    return np.array([
        [0, -n[2], n[1]],
        [n[2], 0, -n[0]],
        [-n[1], n[0], 0]
    ])

# Construction de M_i = [n_i]^  . P_i
def M_i(n_i, P_i):
    vect = produit_vectoriel(n_i)
    M_i_3 = vect @ P_i
    return M_i_3[:2]  # On garde seulement 2 lignes indépendantes

# Triangulation d'un point à partir de plusieurs images
def triangulate_point(P_list, liste_point_i):
    """
    Entrées:
        *P_list : liste des matrices de projection (une par image)
        *liste_point_i : liste contenant, les coordonnées d'un point projeté sur toutes les images
    Sorties:
        *X_cartésien : coordonées cartésiennes du point triangulé (X, Y, Z)
    """
    # On construit la matrice M
    M = np.vstack([M_i(liste_point_i[i], P_list[i]) for i in range(len(P_list))])

    # On effectue la SVD
    U, S, Vt = np.linalg.svd(M)

    # On récupère le vecteur associé à la plus petite valeur singulière
    X_homogène = Vt[-1]

    # On divise par la dernière coordonnée pour obtenir les coordonnées cartésiennes
    X_cartésien = X_homogène[:3] / X_homogène[3]

    return X_cartésien

#Triangulation des points à partir de plusieurs observations
def triangulate_multiple_points(P_list, n_list):
    """
    Entrées:
        *P_list : liste des matrices de projection (une par image)
        *n_list : liste contenant les coordonnées d'un point projeté sur toutes les images
    Sorties:
        *points_3D : liste contenant les coordonnées 3D triangulées
    """
    points_3D = []
    for i in range(len(n_list)):
        point_3D = triangulate_point(P_list, n_list[i])
        points_3D.append(point_3D)
    return np.array(points_3D)

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