import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Adjust the path to include the root directory of your project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ..modRetrieve import retrieve_forecast, process_forecast


class TestRetrieveForecast(unittest.TestCase):

  def setUp(self):
    self.test_filename = 'medium-wind-10m.grib'
    self.test_filepath = os.path.join(os.path.dirname(__file__), self.test_filename)
    # Copy the .grib file to the test directory
    with open(self.test_filename, 'rb') as src, open(self.test_filepath, 'wb') as dst:
      dst.write(src.read())

  def tearDown(self):
    # Remove the copied .grib file after tests
    if os.path.exists(self.test_filepath):
      os.remove(self.test_filepath)

  @patch('modRetrieve.Client')
  @patch('modRetrieve.xr.open_dataset')
  @patch('modRetrieve.os.path.exists')
  @patch('modRetrieve.datetime')
  def test_retrieve_forecast_no_download_needed(self, mock_datetime, mock_exists, mock_open_dataset, mock_client):
    mock_exists.return_value = True
    mock_ds = MagicMock()
    mock_ds["time"].values = 1625097600  # Mocked timestamp
    mock_open_dataset.return_value = mock_ds
    mock_datetime.now.return_value = datetime(2021, 7, 1)
    mock_datetime.fromtimestamp.return_value = datetime(2021, 7, 1)

    parameters = ['msl', '10u', '10v']
    result_filename, mod = retrieve_forecast(parameters, self.test_filename)

    self.assertFalse(mod)
    self.assertEqual(result_filename, './public/medium-wind-10m.grib')

  @patch('modRetrieve.Client')
  @patch('modRetrieve.xr.open_dataset')
  @patch('modRetrieve.os.path.exists')
  @patch('modRetrieve.datetime')
  def test_retrieve_forecast_download_needed(self, mock_datetime, mock_exists, mock_open_dataset, mock_client):
    mock_exists.return_value = True
    mock_ds = MagicMock()
    mock_ds["time"].values = 1625011200  # Mocked timestamp
    mock_open_dataset.return_value = mock_ds
    mock_datetime.now.return_value = datetime(2021, 7, 2)
    mock_datetime.fromtimestamp.return_value = datetime(2021, 7, 1)

    parameters = ['msl', '10u', '10v']
    result_filename, mod = retrieve_forecast(parameters, self.test_filename)

    self.assertTrue(mod)
    self.assertEqual(result_filename, './public/medium-wind-10m.grib')

  @patch('modRetrieve.Client')
  @patch('modRetrieve.os.path.exists')
  def test_retrieve_forecast_file_not_exists(self, mock_exists, mock_client):
    mock_exists.return_value = False

    parameters = ['msl', '10u', '10v']
    result_filename, mod = retrieve_forecast(parameters, self.test_filename)

    self.assertTrue(mod)
    self.assertEqual(result_filename, './public/medium-wind-10m.grib')

class TestProcessForecast(unittest.TestCase):
    @patch('modRetrieve.xr.open_dataset')
    @patch('modRetrieve.pd.DataFrame.to_json')
    def test_process_forecast_export(self, mock_to_json, mock_open_dataset):
        mock_ds = MagicMock()
        mock_ds["u10"] = MagicMock()
        mock_ds["v10"] = MagicMock()
        mock_open_dataset.return_value = mock_ds

        filename = 'medium-wind-10m.grib'
        process_forecast(filename, export=True)

        self.assertTrue(mock_to_json.called)

    @patch('modRetrieve.xr.open_dataset')
    def test_process_forecast_no_export(self, mock_open_dataset):
        mock_ds = MagicMock()
        mock_ds["u10"] = MagicMock()
        mock_ds["v10"] = MagicMock()
        mock_open_dataset.return_value = mock_ds

        filename = 'medium-wind-10m.grib'
        process_forecast(filename, export=False)

        self.assertFalse(mock_ds["u10"].to_dataframe.called)
        self.assertFalse(mock_ds["v10"].to_dataframe.called)

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    unittest.main()