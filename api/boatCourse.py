"""
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
import json

from boatCourseHamza import main as computeCourse
from utils import log

def createGrid(filename: str):
  """Creates the wind speed and wind degree arrays for course computation from jsonifyed data

  Args:
      filename (str): Filename of the json data

  Returns:
      float: Tuple of two arrays of floats, (deg, speed)
  """
  
  log(f"Creating grid from {filename}")
  
  with open(filename) as f:
    data = json.load(f)
    df = pd.DataFrame(data)
    df = df.transpose()
    
  lat = [row.latitude for row in df.itertuples(index=False)]
  lon = [row.longitude for row in df.itertuples(index=False)]    
  lat.sort()    
  lon.sort()
  
  degArray = np.ones((len(lat), len(lon))) /1e6
  speedArray = np.ones((len(lat), len(lon))) /1e6
  
  for row in tqdm(df.itertuples(index=False), total=len(df)):
    i = lat.index(row.latitude)
    j = lon.index(row.longitude)
    degArray[i][j] = row.deg
    speedArray[i][j] = row.speed
    
  # plt.figure()
  # plt.imshow(speedArray, cmap='hot', interpolation='nearest')
  # plt.title('Wind speed')
  # plt.show()
  
  return degArray, speedArray, lat, lon


def test():
  """Testing function for the module
  """
  log("Testing boatCourse")
  
  # START, END = getStartEnd()
  degArray, speedArray, latList, lonList = createGrid("./public/wind-sample-5000.json")
  print(speedArray.shape[0])
  
  path = computeCourse((0,0), (200,200), speedArray, speedArray.shape[0])
  print(f"path: {path}")
  
  plt.figure()
  plt.imshow(speedArray, cmap='hot', interpolation='nearest')
  plt.title('Wind speed and optimized path')
  
  for item in path:
    plt.scatter(item[1], item[0], c='r')
    
  plt.show()
  
  result_dict = {i: {'latitude': latList[x], 'longitude': lonList[y]} for i, (x, y) in enumerate(path)}
  
  json_string = json.dumps(result_dict, indent=4)
  print(json_string)
  
  with open("./public/course.json", "w") as json_file:
    json.dump(result_dict, json_file, indent=4)
    
    
def closest_index(lst, target):
  return min(range(len(lst)), key=lambda i: abs(lst[i] - target))
  
def main(start, end):
  """Generates the course from start to end and saves it to a json file

  Args:
      start (float): Tuple of indices for the start point
      end (float): Tuple of indices for the end point
  """
  log("Generating course")
  
  degArray, speedArray, latList, lonList = createGrid("./public/wind-sample-1000.json")
  start = (closest_index(latList, start[1]), closest_index(lonList, start[0]))
  end = (closest_index(latList, end[1]), closest_index(lonList, end[0]))
  
  path = computeCourse(start, end, speedArray, speedArray.shape[0])
  
  result_dict = {i: {'latitude': latList[x], 'longitude': lonList[y]} for i, (x, y) in enumerate(path)}
  
  json_string = json.dumps(result_dict, indent=4)
  
  with open("./public/course.json", "w") as json_file:
    json.dump(result_dict, json_file, indent=4)

  
  
if __name__ == "__main__":
  test((0,0), (200,200))