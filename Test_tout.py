from D4_v2 import *
from Indirect_1 import *
from Indirect_2_v2 import triangulate_multiple_points, plot_points



##Creation des vecteurs objets 
X = np.asarray(matrices(fonction)[0]) #matrice des coord x des points objets par la fonction Q1
Y = np.asarray(matrices(fonction)[1]) #matrice des coord y des points objets par fonction Q1
Z = np.asarray(matrices(fonction)[2]) #matrice des coord z des points objets par fonction Q1
#matrice contenant les coordonnées x,y,z des points objets
Vects_obj = vects_obj(X,Y,Z) #matrice contenant les vecteurs homogène réels

##Creation des vecteurs images
Xp_ims,Xq_ims = prog_direct(X,Y,Z)

##Creation des matrices vects_image pour chaque image
Vects_image_1 = vects_image_i(Xp_ims[0]-20,Xq_ims[0]-20) #matrice contenant les vecteurs homogène de l'image 1
Vects_image_2 = vects_image_i(Xp_ims[1]-20,Xq_ims[1]-20) #matrice contenant les vecteurs homogène de l'image 2    
Vects_image_3 = vects_image_i(Xp_ims[2]-20,Xq_ims[2]-20) #matrice contenant les vecteurs homogène de l'image 3


##Def points de calibration
Vects_calib_image_1= np.array([[872,3800,1],[2330,2842,1],[2524,2016,1],
                                [1254,2625,1],[2330,1190,1],
                                [140,2016,1],[1254,1407,1],[872,232,1]]) #matrice contenant les vecteurs de calibration sur l'image 1

Vects_calib_image_2= np.array([[133,1769,1],[1077,2491,1],[843,3605,1],
                                [1319,1382,1],[2112,2932,1],
                                [1533,454,1],[2463,1616,1],[2855,2725,1]]) #matrice contenant les vecteurs de calibration sur l'image 2  

Vects_calib_image_3= np.array([[166,3170,1],[1716,3038,1],[2521,3799,1],
                                [923,2016,1],[2803,2016,1],
                                [166,862,1],[1716,994,1],[2521,233,1]]) #matrice contenant les vecteurs de calibration sur l'image 3

Vects_calib_objets = np.array([[-100,100,100,1],[0,100,0,1],[100,100,100,1],
                                [-100,0,0,1],[100,0,0,1],
                                [-100,-100,100,1],[0,-100,0,1],[100,-100,100,1]]) #matrice contenant les vecteurs de calibration réels

##Creation de P_list pour partie triangulation
#P_list contient les matrices de projection pour chaque image
P_list = np.array([P_proj(Vects_calib_image_1, Vects_calib_objets),
                P_proj(Vects_calib_image_2, Vects_calib_objets),
                P_proj(Vects_calib_image_3, Vects_calib_objets)])
P_list=np.around(P_list, decimals=7) #arrondi de la matrice P_list

print("Proj im 1", P_list[0])
print("Proj im 2", P_list[1])


##Creation de n_list pour partie triangulation
n_list =  np.array([[Vects_image_1[0], Vects_image_2[0], Vects_image_3[0]]]) #matrice contenant les coordonnées des points sur toutes les images


for i in range(1,len(Vects_image_1)) :
    n_list=np.append(n_list,np.array([[Vects_image_1[i], Vects_image_2[i], Vects_image_3[i]]]), axis=0) #On rassemble le i-ème point sur toutes les images



##Triangulation des points 3D
points_3D = triangulate_multiple_points(P_list, n_list) #matrice contenant les points 3D

##Affichage des points 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for point in points_3D:
    ax.scatter(point[0], point[1], point[2], c='r', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.title('Points en 3D')
plt.show()
