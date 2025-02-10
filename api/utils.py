"""
Projet PAI Sailing Course
Created on Sun Jan 9 12:00:00 2025

Utility functions
"""
from datetime import datetime

def log(message, filename="./api/python-logs.txt"):
  """Logs a message to the console with a timestamp.

  Args:
      message (str): Message to log
  """
  
  # Open a file in write mode ('w'), or append mode ('a')
  with open(filename, "a") as file:
    file.write(f"[{datetime.now()}] {message}\n")  # Write the string to the file
    
  print(f"[{datetime.now()}] {message}")
