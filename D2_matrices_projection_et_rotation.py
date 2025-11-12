
import numpy as np

def matrice_rotation(angles):
    """Entrée : angles est un 3 uplet
    Sortie : R est une matrice de rotation
    Calcule la matrice de rotation 3x3 à partir des angles (theta_x, theta_y, theta_z) en degrés."""
    
    theta_x, theta_y, theta_z = np.radians(angles)  # Conversion en radians pour le calcul
  
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(theta_x), -np.sin(theta_x)],
                   [0, np.sin(theta_x), np.cos(theta_x)]])
    
    Ry = np.array([[np.cos(theta_y), 0, np.sin(theta_y)],
                   [0, 1, 0],
                   [-np.sin(theta_y), 0, np.cos(theta_y)]])
    
    Rz = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
                   [np.sin(theta_z), np.cos(theta_z), 0],
                   [0, 0, 1]])
    
    R = np.dot(np.dot(Rx, Ry), Rz)  # Multiplication matricielle pour obtenir la matrice rotation
    return R




def matrice_projection(f, taille_pixel, taille_capteur, R, Xe_Omega):
    """Entrées : f la focale
    taille_capteur liste de 2 elements
    Calcule la matrice de projection perspective Pth."""
  
    #coord du centre du capteur dans les coord images1 (en mm)
    cx_H, cy_H = taille_capteur[1]*taille_pixel / 2, taille_capteur[0]*taille_pixel / 2 
    #print("cx_H, cy_H", cx_H, cy_H)
    # Matrice K (voir (4) page 5)
    K = np.array([[-f, 0, cx_H],
                  [0, -f, cy_H],
                  [0, 0, 1]])
    
    #Création matrice N (voir (5) page 6)
    N = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, taille_pixel]])
    RT = np.dot(R, np.concatenate((np.identity(3),-np.reshape(Xe_Omega, (3,1))), axis = 1))  # multiplication matricielle et concaténation
    Pth = np.dot(np.dot(N,K),RT)
    return Pth
