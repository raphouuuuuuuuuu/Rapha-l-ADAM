## Problème indirect photogrammétrie
"""
Objectif: Obtenir les coordonnées 3D des points de calibrage.
    Entrées:
        * Matrices des coordonnées images des points de calibrage (Matp et Matq) présents dans chaque image i
        * Matrices de Projection Perspective associées à chaque image i 
    Sortie:
        * Matrices des coordonnées objets des points de calibrage (MatX, MatY, MatZ)
"""

#Needed Imports
import numpy as np
from typing import List
import copy

##Recontrustion des vecteurs coordonnées images des points de calibrage 
#(les vecteurs utilisés sont homogènes)

def vects_image_i (Xp_i: List[int], Xq_i: List[int]) -> List[int]:
    """
        Cette fonction prend les Matrices de coordonnées p et q des points de calibration présents sur 
        une image i et retourne les vecteurs homogènes associés.
        Entrées:
            * Xp_i: Matrice des coordonnées p de points présents sur l'image i
            * Xq_i: Matrice des coordonnées q de points présents sur l'image i
        Sortie:
            *Vects: Matrice contenant les vecteurs homogènes associés aux matrices Xp et Xq
    """
    #Asserts
    assert(len (Xp_i) == len (Xq_i) and len(Xp_i[1]) == len(Xq_i[1]))

    #Initialisation
    Vects_image_i=np.array([[Xp_i[0][0],Xq_i[0][0],1]]) #Matrice contenant les vecteurs homogène de l'image i 

    for i in range(len(Xp_i)):
        for j in range(len(Xp_i[0])):
            if i==j==0:
                #do nothing
                pass
            else:
                #On ajoute le vecteur associé aux coordonnées Xp_i,j et Xq_i,j à Vects_image_i
                Vects_image_i= np.append(Vects_image_i, np.array([[Xp_i[i][j], Xq_i[i][j], 1]]), axis=0)
    
    return Vects_image_i

##Recontrustion des vecteurs coordonnées objet des points de calibrage 
#(les vecteurs utilisés sont homogènes)

def vects_obj (X: List[int], Y: List[int], Z: List[int]) -> List[int]:
    """
        Cette fonction prend les Matrices des coords réelles des points et  construit 
        les vecteurs associés aux coords x, y et z pour chaque élt de matrices.
        Entrées:
            * X: Matrice des coordonnées x de points présents sur l'image i
            * Y: Matrice des coordonnées y de points présents sur l'image i
            * Z: Matrice des coordonnées z de points présents sur l'image i
        Sortie:
            *Vects: Matrice contenant les vecteurs homogènes réels
    """
    #Asserts
    assert(len (X) == len (Y) == len(Z) and len(X[1]) == len(Y[1]) == len(Z[1]))

    #Initialisation
    Vects_obj = np.array([[X[0][0], Y[0][0], Z[0][0], 1]]) #Matrice contenant les vecteurs homogène de l'image i 

    for i in range(len(X)):
        for j in range(len(X[1])):
            if i==j==0:
                #do nothing
                pass
            else:
                #On ajoute le vecteur associé aux coordonnées (X[i],Y[i],Z[i],t) à Vects_obj
                Vects_obj = np.append(Vects_obj, [[X[i][j], Y[i][j], Z[i][j], 1]], axis=0)
    
    return Vects_obj


    ##Reconstruction des points 3D:

#1: Matrices de projection perspéctive 

def prod_vect_image (p: int, q: int) -> List[int] :
    """
        Cette fonction renvoie la matrice produit vectoriel associé au vecteur (p,q) d'un point sur une image
        Entrées:
            * p: coordonnée p d'un point sur une image
            * q: coordonnée q d'un point sur une image
        Sortie :
            * n_v : matrice de produit vectoriel associée au vecteur n= (p,q)
    """
    return np.array([[0, -1, q],[1, 0, -p],[-q, p, 0]])

def produit_tensoriel (A: List[int], B: List[int]) -> List[int]:
    """
        Cette fonction renvoie le produit tensoriel de deux vecteurs A et B
        Si on a en entrée A une matrice de taille (m,n), Bune matrice de taille (p,q),
        On renvoie une matrice C de taille (m*p,n*q) telle que:
                         __ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __
                        |                                               |
                        | A[0][0]*B   A[0][1]*B  ---------  A[0][n]*B   |
                    C=  |     |                                 |       |
                        |     |                                 |       |
                        |     |                                 |       |
                        | A[m][0]*B   A[m][1]*B  ---------  A[m][n]*B   |
                        |__ __ __ __ __ __ __ __ __ __ __ __ __ __ __ __|
        Entrées:
            * A: Matrice de taille (m,n)
            * B: Matrice de taille (p,q)
        Sortie:
            * C: Matrice de taille (m*p,n*q) contenant le produit tensoriel de A et B
    """
    ##Asserts
    #On s'assure que A et B sont des matrices
    assert(type(A) == np.ndarray and type(B) == np.ndarray) 
    assert(type(A[0]) == np.ndarray and type(B[0]) == np.ndarray) 
    
    ##Initialisation
    #Dimensions de A
    m = len(A)
    n=len(A[0])
    #Dimensions de B
    p = len(B)
    q=len(B[0])
    # Matrice du produit tensoriel
    C=np.zeros(((m*p),(abs(n)*abs(q))))
    
    ##Completion de la matrice C
    for i in range(m):
        for j in range(n):
            for k in range(p):
                for l in range(q):
                    C[i*p+k][j*q+l] = A[i][j]*B[k][l]

    return C      


def P_proj(Vects_calib_image_i: List[int], Vects_calib_objets: List[int]) -> List[int]:
    """
        Cette fonction utilise la formule donnée dans la partie 6.1 pour construire la matrice
        projection perspéctive d'une image i.
        Entrées:
            * Vects_calib_image_i: Matrice des coordonnées images des points de calibration présents sur l'image i 
            * Vects_calib_objets: Matrice des coordonnées objets des points de calibration présents sur l'image i 
        Sortie:
            * P: Matrice de projection perspéctive associée à l'image i
    """
    ##Assertions
    assert(len(Vects_calib_image_i)==len(Vects_calib_objets) and len(Vects_calib_image_i)>=6) #Il faut au minimum 6 points pour obtenir l'équation qui donne P

    ##Calcul de la matrice C
    
    #Initialisation
    p_0, q_0 = Vects_calib_image_i[0][0], Vects_calib_image_i[0][1] #Coordonnée en repère image
    n0_vec = prod_vect_image(p_0, q_0)  
    X_0 = np.array([Vects_calib_objets[0]]) 
    C_0=produit_tensoriel(n0_vec, X_0) 
    
    C=C_0[:2]  #Matrice nommée comme dans le cours pour plus de clarté

    #On fait l'hypothèse pour l'instant que le vecteur i dans Vects_images est équivalent 
    # au vecteur i dans Vects_objets

    #On implémente la matrice C
    for i in range(1, len(Vects_calib_image_i)):
        p_c,q_c = Vects_calib_image_i[i][0], Vects_calib_image_i[i][1]
        nc_vec = prod_vect_image(p_c, q_c) 
        X_c=  np.array([Vects_calib_objets[i]])
        Ci = produit_tensoriel(nc_vec, X_c)
        C= np.append(C,Ci[:2], axis=0)

    #On implemente le SVD de la matrice C
    U, D, Vt = np.linalg.svd(C)
    
    #On détermine maintenant les éléments de P
    #Pour cela, on détermine la valeur propre (vp) de norme minimale de C, en sachant que les vp de C sont les coefficients diagonaux de D.
    #On trouve ensuite le vecteur propre normé dans la matrice VT.

    #On initialise la recherche.
    ind_min=0 #indice de la valeur propre minimale de C
    for i in range(1,len(D)): #D est une liste de taille 12 contenant les valeurs propres de C 
        if D[ind_min] >= D[i]:
            ind_min = i

    #On extrait les 12 premiers éléments de Vt (qui est une matrice de taille 12x12) pour obtenir la matrice P
    #On écrit P sous la forme d'une matrice 3x4 que l'on retourne ensuite
    P_Mat = np.array([[Vt[ind_min][0], Vt[ind_min][1], Vt[ind_min][2], Vt[ind_min][3]],
                      [Vt[ind_min][4], Vt[ind_min][5], Vt[ind_min][6], Vt[ind_min][7]],
                      [Vt[ind_min][8], Vt[ind_min][9], Vt[ind_min][10], Vt[ind_min][11]]])

    #On normalise la matrice de projection pour éviter les erreurs d'arrondi 
    return P_Mat /np.linalg.norm(P_Mat) 
    