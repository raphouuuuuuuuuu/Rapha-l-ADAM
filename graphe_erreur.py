import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def evaluation_erreur(points_3D_reconstruit, points_3D_theorique):
    """
    Évalue l'erreur de reconstruction en calculant la distance euclidienne
    entre chaque point reconstruit et son équivalent théorique.

    Paramètres :
    - points_3D_reconstruit : liste des points 3D reconstruits (n x 3 ou n x 4 homogène)
    - points_3D_theorique : liste des points 3D théoriques (n x 3)

    Retour :
    - distances : liste des distances (rayons) entre chaque point reconstruit et théorique
    """
    distances = []
    for reconstruit, theorique in zip(points_3D_reconstruit, points_3D_theorique):
        # Si les points reconstruits sont en coordonnées homogènes, on homogénéise
        if len(reconstruit) == 4:
            reconstruit = np.array(reconstruit[:3]) / reconstruit[3]
        else:
            reconstruit = np.array(reconstruit)
        theorique = np.array(theorique)
        # Calcul de la distance euclidienne
        distance = np.linalg.norm(reconstruit - theorique)
        distances.append(distance)
    return distances


# le point_3D_reconstruit correspont a points_3D obtenu a la fin du code indirect 


def graphique_erreur(points_3D_reconstruit, distances):
    """
    Affiche un graphe 3D des points reconstruits avec une couleur
    plus foncée en fonction de la distance (erreur), exprimée en millimètres.

    Paramètres :
    - points_3D_reconstruit : liste des points 3D reconstruits (n x 3 ou n x 4 homogène)
    - distances : liste des distances (erreurs) entre les points reconstruits et théoriques
    """
    # Si les points sont en homogène, les convertir en cartésien
    points_cartesien = []
    for point in points_3D_reconstruit:
        if len(point) == 4:
            point = np.array(point[:3]) / point[3]
        points_cartesien.append(point)
    points_cartesien = np.array(points_cartesien)

    # Convertir les distances en millimètres
    distances_mm = np.array(distances) * 1000

    # Normaliser les distances pour les mapper à une échelle de couleurs
    distances_normalized = (distances_mm - np.min(distances_mm)) / (np.max(distances_mm) - np.min(distances_mm))

    # Création du graphe 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot avec une colormap
    scatter = ax.scatter(
        points_cartesien[:, 0],  # Coordonnées X
        points_cartesien[:, 1],  # Coordonnées Y
        points_cartesien[:, 2],  # Coordonnées Z
        c=distances_normalized,  # Couleurs basées sur les distances normalisées
        cmap='plasma_r',           # Colormap (peut être changé, ex : 'plasma', 'coolwarm','viridis_r')
        s=50                     # Taille des points
    )

    # Ajouter une barre de couleur pour indiquer l'échelle des distances
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Erreur (distance en mm)')

    # Labels des axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('Graphe d\'erreur des points reconstruits (échelle en mm)')
    plt.show()


#calcul incertitudes



def calculer_incertitudes(distances):
    """
    Calcule les incertitudes à partir des distances (erreurs).

    Paramètres :
    - distances : liste des distances (erreurs) entre les points reconstruits et théoriques

    Retour :
    - moyenne : moyenne des distances
    - ecart_type : écart-type des distances
    - rmse : erreur quadratique moyenne (Root Mean Square Error)
    """
    distances = np.array(distances)
    moyenne = np.mean(distances)
    ecart_type = np.std(distances)
    rmse = np.sqrt(np.mean(distances**2))
    return moyenne, ecart_type, rmse




# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de points 3D reconstruits et théoriques
    points_3D_reconstruit = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    points_3D_theorique = [
        [1.1, 2.1, 3.1],
        [4.2, 5.2, 6.2],
        [7.3, 8.3, 9.3]
    ]

    # Calculer les distances
    distances = evaluation_erreur(points_3D_reconstruit, points_3D_theorique)

    # Afficher le graphique d'erreur
    graphique_erreur(points_3D_reconstruit, distances)

    # Calculer les incertitudes
    moyenne, ecart_type, rmse = calculer_incertitudes(distances)
    print(f"Moyenne des erreurs : {moyenne:.4f}")
    print(f"Écart-type des erreurs : {ecart_type:.4f}")
    print(f"RMSE : {rmse:.4f}")