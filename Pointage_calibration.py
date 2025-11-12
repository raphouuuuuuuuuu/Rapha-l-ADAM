#determiner les coordonnées des points a partir des photos 2D prises 
"""
Ce script permet de charger plusieurs images, d'afficher chacune d'elles et de cliquer sur des points d'intérêt.
Les coordonnées des points cliqués sont stockées dans une liste.
Les images sont affichées une par une, et un rectangle est dessiné autour d'une zone neutre pour indiquer où les clics ne seront pas pris en compte.
"""

# Importer les bibliothèques nécessaires
import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as patches  # Importer pour dessiner des rectangles


# Liste des chemins vers les images (modifie-les selon tes fichiers)
image_paths = ['IMG_1.jpg', 'IMG_2.jpg', 'IMG_3.jpg', 'IMG_4.jpg', 'IMG_5.jpg', 'IMG_6.jpg', 'IMG_7.jpg', 'IMG_8.jpg', 'IMG_9.jpg', 'IMG_10.jpg', 'IMG_11.jpg']  # ← remplace ou ajoute des noms d’images


############################### Charger les images #################################
# Charger et convertir les images
images_rgb = []
k = 0 # nombre d'images qu'il y aura dans le folder
for path in image_paths:
    img = cv2.imread(path)
    if img is None:
        #raise FileNotFoundError(f"Image non trouvée : {path}")
        break # Si l'image n'est pas trouvée, on sort de la boucle (on limite le nombre d'image qui s'affiche)
    # Convertir l'image de BGR à RGB
    # OpenCV charge les images en BGR, on les convertit en RGB pour Matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    images_rgb.append(img_rgb)
    k += 1

# Vérifier si des images ont été chargées 
if k == 0:
    raise ValueError("Aucune image n'a été chargée. Vérifiez les chemins d'accès.")

#####################################################################################




###################################### Affichage des images et clics ######################################
# Dictionnaire pour stocker les points cliqués
clicked_points = {}
point_counter = [0] * k  # Compteur pour chaque image

# Liste pour stocker les coordonnées des points cliqués par image
L = [[] for _ in range(k)]  # Une sous-liste pour chaque image


# Générer dynamiquement une liste de zones neutres en fonction du nombre d'images
neutral_zones = []
for i in range(k):
    img = images_rgb[i]
    height, width = img.shape[:2]
    xmin = 0
    xmax = width
    ymin = height  # juste en dessous de l'image
    ymax = height + height // 4  # un quart de la hauteur de l'image
    neutral_zones.append((xmin, xmax, ymin, ymax))



# Fonction de clic
current_image = 0  # Variable pour suivre l'image actuelle

def onclick(event):
    global current_image  # Permet de modifier la variable globale
    ax = axes[current_image]  # Sélectionne l'axe de l'image actuelle
    if event.inaxes == ax:
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            # Vérifier si le clic est dans la zone neutre
            if neutral_zone[0] <= x <= neutral_zone[1] and neutral_zone[2] <= y <= neutral_zone[3]:
                L[current_image].append([None, None])  # Ajouter None si le clic est dans la zone neutre
                print(f"Image {current_image+1} : clic dans la zone neutre")
            else:
                L[current_image].append([x, y])  # Ajouter les coordonnées si le clic est hors de la zone neutre
                print(f"Image {current_image+1} : x = {x}, y = {y}")
                # Ajoute un numéro à la position cliquée
                ax.text(x, y, str(len(L[current_image])), color='red', fontsize=12, ha='center', va='center')
                fig.canvas.draw()
            # Passe à l'image suivante (ou revient à la première si c'est la dernière)
            current_image = (current_image + 1) % k


"""
def onclick(event):
    for i, ax in enumerate(axes):
        if event.inaxes == ax:
            if event.xdata is not None and event.ydata is not None:
                x, y = int(event.xdata), int(event.ydata)
                clicked_points[i] = (x, y)
                print(f"Image {i+1} : x = {x}, y = {y}")
                # Dessine un point sur l'image
                ax.text(x, y, str(point_counter[i]), color='red', fontsize=12, ha='center', va='center')
                fig.canvas.draw()
            break
""" 

# Vérifier que le nombre de zones neutres correspond au nombre d'images
if len(neutral_zones) != k:
    raise ValueError("Le nombre de zones neutres doit correspondre au nombre d'images.")

# Affichage des images
fig, axes = plt.subplots(1, k, figsize=(5 * k, 5))
if k == 1:
    axes = [axes]  # pour rendre axes itérable si k = 1

for ax, img_rgb, path, neutral_zone in zip(axes, images_rgb, image_paths, neutral_zones):
    ax.imshow(img_rgb)
    # Étendre l'axe y pour voir la zone neutre sous l'image
    height = img_rgb.shape[0]
    ax.set_ylim(height + height // 4, 0)
    ax.set_title(f"Clique sur l'image\n{path}")
    ax.axis('off')
    # Dessiner la zone neutre
    rect = patches.Rectangle(
        (neutral_zone[0], neutral_zone[2]),  # Coin inférieur gauche (xmin, ymin)
        neutral_zone[1] - neutral_zone[0],  # Largeur
        neutral_zone[3] - neutral_zone[2],  # Hauteur
        linewidth=2, edgecolor='blue', facecolor='none', linestyle='--'
    )
    ax.add_patch(rect)  # Ajouter le rectangle à l'image

fig.canvas.mpl_connect('button_press_event', onclick)
plt.tight_layout()
plt.show()

"""
# Affichage final des points cliqués (facultatif)
print("\nPoints cliqués :")
for i, points in enumerate(L):
    print(f"Image {i+1} : {points}")
"""

######################################################################################################

# Convertir les listes de coordonnées en tableaux numpy
Xp = np.array([[point[0] for point in L[i]] for i in range(k)])
Yp = np.array([[point[1] for point in L[i]] for i in range(k)])




#print(L)
print("X_calib = ", Xp)
print("Y_calib = ", Yp)

