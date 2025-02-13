# -*- coding: utf-8 -*-
"""
Projet PAI sur le voilier 
Created on Thu Jan  2 15:14:54 2025

@author: Hamza KHITOUS
"""

import numpy as np
import heapq
import matplotlib.pyplot as plt

def diagonale_k(n,k,c):
    
    M = np.zeros((n,n))
    
#Générer une matrice toute nulle sauf la kième diagonale
    if c == 'down' :
      for i in range(k) :
        M[n-1-i][k-i-1] = 1
        
    if c == 'up' :
       for j in range(k) :
        M[k-j-1][n-1-j] = 1
        
    return M

def distance(a, b):
    """ distance euclidienne."""
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_neighbors(pos, grid_size):
    """Retourne les cases voisines valides autour de la position."""
    neighbors = [
        (pos[0] + dx, pos[1] + dy)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ]
    return [
        n for n in neighbors
        if 0 <= n[0] < grid_size and 0 <= n[1] < grid_size
    ]

def cost_function(pos, bathymetry, ocean_current, wind_speed, min_depth=5):
    """Fonction de coût basée sur la bathymétrie, le vent et le courant."""
    depth = bathymetry[pos]
    wind = wind_speed[pos]
    current = ocean_current[pos]

    # Si la profondeur est inférieure au minimum requis, coût infini (impossible).
    if depth < min_depth:
        return float('inf')
    
    # Le vent favorable et le courant favorable réduisent le coût.
    # Ceci est un exemple arbitraire : plus de vent => déplacement plus facile
    # et un courant négatif diminue le coût (courant dans le bon sens).
    return 10 / wind - current / 10

def a_star(start, end, grid_size, bathymetry, ocean_current, wind_speed, min_depth=5):
    """Algorithme A* pour trouver le chemin optimal."""
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priorité, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance(start, end)}
    
    while open_set:
        # print("open_set: ", open_set)
        
        _, current = heapq.heappop(open_set)
        # print("current :", current)
    

        if current == end:
            # On reconstruit le chemin
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
                
            path.append(start)
            #print(path)
            return path[::-1]

        for neighbor in get_neighbors(current, grid_size):
            # print("neighbor :", neighbor)
            tentative_g_score = g_score[current] + cost_function(neighbor, bathymetry, ocean_current, wind_speed, min_depth)
            # print("tentative_g_score :", tentative_g_score)
            # print("g_score.get(neighbor, float('inf')) :",g_score.get(neighbor, float('inf')))
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                # print("came_from : ", came_from)
                g_score[neighbor] = tentative_g_score
                # print("g_score : ", g_score)
                f_score[neighbor] = tentative_g_score + distance(neighbor, end)            
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Aucun chemin trouvé
     
        
        
def test():
  # --- Données simulées ---
  GRID_SIZE = 10
  np.random.seed(0)
  #bathymetry = np.random.randint(4, 20, size=(GRID_SIZE, GRID_SIZE))  # Profondeur en mètres
  bathymetry = 10 * np.ones((GRID_SIZE, GRID_SIZE))
  #wind_speed = np.random.randint(1, 10, size=(GRID_SIZE, GRID_SIZE))  # Vitesse du vent (unité arbitraire)
  #wind_speed = 10 * np.ones((GRID_SIZE, GRID_SIZE))
  wind_speed = 10 * diagonale_k(GRID_SIZE,5,'up') + np.ones((GRID_SIZE,GRID_SIZE))
  #wind_speed[(3,0)] = 20
  #wind_speed[(2,0)] = 20
  #wind_speed[(4,6)] = 15
  #ocean_current = np.random.randint(-2, 2, size=(GRID_SIZE, GRID_SIZE))  # Courant (unité arbitraire)
  ocean_current = 2 * np.ones((GRID_SIZE, GRID_SIZE))
  #ocean_current = 10 * diagonale_k(GRID_SIZE,7,'down') + np.ones((GRID_SIZE,GRID_SIZE))
  #ocean_current[(4,4)] = -4


  # --- Contraintes et paramètres ---
  MIN_DEPTH = 5
  START = (0, 0)
  END = (9,9)
  
  # --- Exécution de l'algorithme ---
  path = a_star(START, END)
  print("Path:", path)

  # --- Visualisation du résultat ---
  if path is not None:
      # Extraire les coordonnées X et Y du chemin
      x_coords = [pos[0] for pos in path]
      y_coords = [pos[1] for pos in path]
      
      plt.figure(figsize=(10, 10))
      plt.subplot(3, 1, 1)
      # Afficher la bathymétrie
      plt.imshow(bathymetry, cmap='terrain', origin='upper')
      # Tracer le chemin (en rouge)
      plt.gca().invert_yaxis()
      plt.plot(x_coords, y_coords, 'r-o', label='Chemin optimal')
      
      
      # Mettre en évidence départ et arrivée
      plt.scatter(START[0], START[1], c='green', s=100, marker='X', label='Départ')
      plt.scatter(END[0], END[1], c='blue', s=100, marker='X', label='Arrivée')

      plt.title("Chemin A* sur carte de bathymétrie")
      plt.legend()
      plt.colorbar(label="Profondeur (m)")
      plt.show()

      # Deuxième sous-figure : Vitesse du vent
      plt.figure(figsize=(10, 10))
      plt.subplot(3, 1, 2)
      plt.title("Vitesse du vent")
      plt.imshow(wind_speed.T, cmap='cool', origin='upper')
      plt.gca().invert_yaxis()
      plt.plot(x_coords, y_coords, 'r-o', label='Chemin optimal')
      # Marquer le départ et l'arrivée
      plt.scatter(START[1], START[0], c='green', s=100, marker='X', label='Départ')
      plt.scatter(END[1], END[0], c='blue', s=100, marker='X', label='Arrivée')
      plt.colorbar(label="Vent (unité arbitraire)")
      #plt.legend()
      
      # Troisième sous-figure : Courant océaniques 
      """plt.figure(figsize=(10, 10))
      plt.subplot(3, 1, 3)
      plt.title("Courant océaniques")
      plt.imshow(ocean_current.T, cmap='cool', origin='upper')
      plt.gca().invert_yaxis()
      plt.plot(x_coords, y_coords, 'r-o', label='Chemin optimal')
      # Marquer le départ et l'arrivée
      plt.scatter(START[1], START[0], c='green', s=100, marker='X', label='Départ')
      plt.scatter(END[1], END[0], c='blue', s=100, marker='X', label='Arrivée')
      plt.colorbar(label="Courant (unité arbitraire)")
      #plt.legend()"""
      
      
  else:
          print("Aucun chemin n'a pu être trouvé.")
        
def main(start, end, windArray, gridSize):
  """Computes the optimal path for the boat to follow according to winds.

  Args:
      start (int): Tuple of ints representing the starting point.
      end (int): Tuple of ints representing the ending point.
      windArray (float): Array of floats representing the wind speed.
      gridSize (float): Array of floats representing the grid size.

  Returns:
      int: List of tuples representing the optimal path for the boat to follow.
  """
  
  # --- Contraintes et paramètres ---
  MIN_DEPTH = 5
  GRID_SIZE = gridSize
  START = start
  END = end
  bathymetry = 10 * np.ones((GRID_SIZE, GRID_SIZE))
  wind_speed = windArray
  ocean_current = 10 * np.ones((GRID_SIZE, GRID_SIZE))
  
  path = a_star(START, END, gridSize, bathymetry, ocean_current, wind_speed, min_depth=5)
  
  return path


if __name__ == "__main__":
  test()