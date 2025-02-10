""""
Projet PAI Sailing Course
Created on Sun Jan 9 12:00:00 2025

Import data functions and computing functions
"""


import numpy as np
import heapq
import json
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

def createGrid(filename: str):
  """Creates the wind speed and wind degree arrays for course computation from jsonifyed data

  Args:
      filename (str): Filename of the json data

  Returns:
      float: Tuple of two arrays of floats, (deg, speed)
  """
  
  with open(filename) as f:
    data = json.load(f)
    df = pd.DataFrame(data)
    df = df.transpose()
    
    # print(f"Simple import of data:")
    # print(df.head())
    
  lat = [row.latitude for row in df.itertuples(index=False)]
  lon = [row.longitude for row in df.itertuples(index=False)]    
  lat.sort()    
  lon.sort()
  # print(lat)
  # print(lon)
  
  degArray = np.ones((len(lat), len(lon))) /1e6
  speedArray = np.ones((len(lat), len(lon))) /1e6
  
  for row in tqdm(df.itertuples(index=False), total=len(df)):
    i = lat.index(row.latitude)
    j = lon.index(row.longitude)
    degArray[i][j] = row.deg
    speedArray[i][j] = row.speed
    
    # if row.speed == 0:
    #   print(f"row: {row}")
    
  # print(f"degArray: {degArray}")
  
  plt.figure()
  plt.imshow(speedArray, cmap='hot', interpolation='nearest')
  plt.title('Wind speed')
  plt.show()
  
  return degArray, speedArray, lat, lon

# from boatCourseHamza import distance, get_neighbors, cost_function, a_star
from boatCourseHamza import main as computeCourse

def test():

  # START, END = getStartEnd()
  degArray, speedArray, latList, lonList = createGrid("./public/wind-sample-5000.json")
  print(speedArray.shape[0])
  
  path = computeCourse((0,0), (200,200), speedArray, speedArray.shape[0])
  # print(f"path: {path}")
  
  plt.figure()
  plt.imshow(speedArray, cmap='hot', interpolation='nearest')
  plt.title('Wind speed and optimized path')
  for item in path:
    plt.scatter(item[1], item[0], c='r')
  plt.show()
  
import json
  
def main(start, end):
  degArray, speedArray, latList, lonList = createGrid("./public/wind-sample-1000.json")
  path = computeCourse(start, end, speedArray, speedArray.shape[0])
  
  result_dict = {i: {'latitude': latList[x], 'longitude': lonList[y]} for i, (x, y) in enumerate(path)}
  
  json_string = json.dumps(result_dict, indent=4)
  print(json_string)
  
  with open("./public/course.json", "w") as json_file:
    json.dump(result_dict, json_file, indent=4)
  
  
if __name__ == "__main__":
  main((0,0), (200,200))