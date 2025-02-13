import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import json
import pandas as pd
import os
import sys

# Adjust the path to include the root directory of your project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..modOptim import createGrid, closest_index, main

class TestCreateGrid(unittest.TestCase):
  def setUp(self):
    self.dummy_json_path = os.path.join(os.path.dirname(__file__), 'dummy.json')
    with open(self.dummy_json_path, 'w') as f:
      json.dump({
        "0": {"latitude": 10, "longitude": 20, "deg": 30, "speed": 40},
        "1": {"latitude": 15, "longitude": 25, "deg": 35, "speed": 45}
      }, f)

  def tearDown(self):
    os.remove(self.dummy_json_path)

  @patch('modOptim.pd.DataFrame')
  def test_create_grid(self, mock_dataframe):
    mock_df = MagicMock()
    mock_df.transpose.return_value = mock_df
    mock_df.itertuples.return_value = [
      MagicMock(latitude=10, longitude=20, deg=30, speed=40),
      MagicMock(latitude=15, longitude=25, deg=35, speed=45)
    ]
    mock_dataframe.return_value = mock_df

    degArray, speedArray, lat, lon = createGrid(self.dummy_json_path)

    self.assertEqual(degArray.shape, (2, 2))
    self.assertEqual(speedArray.shape, (2, 2))
    self.assertIn(30, degArray)
    self.assertIn(35, degArray)
    self.assertIn(40, speedArray)
    self.assertIn(45, speedArray)

class TestClosestIndex(unittest.TestCase):
    def test_closest_index(self):
        lst = [10, 20, 30, 40]
        target = 25
        index = closest_index(lst, target)
        self.assertEqual(index, 1)

class TestMain(unittest.TestCase):
    @patch('modOptim.createGrid')
    @patch('modOptim.computeCourse')
    @patch('modOptim.json.dump')
    def test_main(self, mock_json_dump, mock_computeCourse, mock_createGrid):
        mock_createGrid.return_value = (
            np.array([[0, 1], [2, 3]]),
            np.array([[4, 5], [6, 7]]),
            [10, 20],
            [30, 40]
        )
        mock_computeCourse.return_value = [(0, 0), (1, 1)]

        start = (30, 10)
        end = (40, 20)
        main(start, end)

        self.assertTrue(mock_json_dump.called)

if __name__ == '__main__':
    unittest.main()
