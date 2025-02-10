# https://github.com/ecmwf/ecmwf-opendata
# https://github.com/ecmwf/cfgrib

from ecmwf.opendata import Client
import xarray as xr
import xarray_extras as xrx
import os
import shutil
from datetime import datetime
import numpy as np

def retrieve_forecast(parameters, filename):
    """Checks if retrieve is needed and downloads the forecast file if needed.

    Args:
        parameters (str): List of parameters to download
        filename (str): Filename to save the forecast data

    Returns:
        str: filename of the forecast data
    """
    # Define .grib modifier id
    mod = False
    
    # Create the dataset directory if it doesn't exist
    dataset_dir = "./public/"
    
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    
    # Check if the file exists
    filename = os.path.join(dataset_dir, filename)
    
    if os.path.exists(filename):
        ds = xr.open_dataset(filename, engine="cfgrib", decode_times=False) # To avoid datetime incompatibility use decode_times=False kwarg in xarray.open_dataset
        fileTime = ds["time"].values
        file_time_converted = datetime.fromtimestamp(fileTime)
        file_day = file_time_converted.day
        
        current_time = datetime.now()
        current_day = current_time.day
        
        # print(f"Current time: {current_time}")
        # print(f"File time: {fileTime}")
        # print(f"File time (converted): {file_time_converted}")

        if file_day - current_day < 1:
            print(f"Reponse [{file_day - current_day}]. The weather dataset file time {file_time_converted} and current time {current_time} are on the same day. No download needed.")
            
        else:
            print(f"The weather dataset file time {file_time_converted} and current time {current_time} are on different days. Proceeding with download.")
            
            mod = True
            
            client = Client()
    
            request = {
                # "date":'2022-01-25 12:00:00',
                "source": "ecmwf",  # ecmwf or azure
                "model": "ifs",  # ifs (physic driven) or aifs (data driven)
                "resol": "0p25",  # only resol available
                "preserve_request_order": False,  # faster download
                "infer_stream_keyword": True,  # It is recommended not to set the preserve_request_order flag to True when downloading a large number of fields as this will add extra load on the servers.
                "type": "fc", # forecast (HRES), other types exist within (ENS)
                "stream":"oper", # Atmospheric fields from HRES - 00 UTC and 12 UTC
                "step": 24, # Q: 12 hourly steps
                "levtype":"sfc", # Q: surface level
                "param": parameters,
            }
            
            time = client.latest( # returns the latest forecast date and time
                request=request,
                target=filename,
            )
            
            print(f"Latest forecast available : {time}")
            
            result = client.retrieve(
                request = request,
                target = filename,
            )
            
            print(f"Forecast downloaded : {result}")
            
            # # Move the file to the dataset directory
            # destination = os.path.join(dataset_dir, filename)
            
            # if os.path.exists(filename):
            #     shutil.move(filename, destination)
            #     filename = destination
    
    else:
        print(f"The weather dataset file does not exist yet. Proceding with download.")
        
        mod = True
        
        client = Client()

        request = {
            # "date":'2022-01-25 12:00:00',
            "source": "ecmwf",  # ecmwf or azure
            "model": "ifs",  # ifs (physic driven) or aifs (data driven)
            "resol": "0p25",  # only resol available
            "preserve_request_order": False,  # faster download
            "infer_stream_keyword": True,  # It is recommended not to set the preserve_request_order flag to True when downloading a large number of fields as this will add extra load on the servers.
            "type": "fc", # forecast (HRES), other types exist within (ENS)
            "stream":"oper", # Atmospheric fields from HRES - 00 UTC and 12 UTC
            "step": 24, # Q: 12 hourly steps
            "levtype":"sfc", # Q: surface level
            "param": parameters,
        }
        
        time = client.latest( # returns the latest forecast date and time
            request=request,
            target=filename,
        )
        
        print(f"Latest forecast available : {time}")
        
        result = client.retrieve(
            request = request,
            target = filename,
        )
        
        print(f"Forecast downloaded : {result}")
        
        # # Move the file to the dataset directory
        # destination = os.path.join(dataset_dir, filename)
        
        # if os.path.exists(filename):
        #     shutil.move(filename, destination)
        #     filename = destination
    
    return filename, mod

    
def process_forecast(filename, export=False):
    """Load and process the .grib file to extract the wind data and export it to a .json file.

    Args:
        filename (str): .grib file to process
        export (bool, optional): Boolean to export data to .json. Defaults to False.
    """
    
    print("Proceeding with grib to json export.")
    ds = xr.open_dataset(filename, engine="cfgrib", decode_times=False) # To avoid datetime incompatibility use decode_times=False kwarg in xarray.open_dataset

    u10 = ds["u10"]
    v10 = ds["v10"]
    
    if export:
        udf = u10.to_dataframe()
        vdf = v10.to_dataframe()
        
        udf.drop(["valid_time", "heightAboveGround", "meanSea"], axis=1, inplace=True)
        udf.reset_index(inplace=True)
        
        vdf.drop(["valid_time", "heightAboveGround", "meanSea"], axis=1, inplace=True)
        vdf.reset_index(inplace=True)
        
        df = udf.merge(vdf, on=["latitude", "longitude"])
        df.drop(["time_y", "step_y"], axis=1, inplace=True)
        df.rename(columns={"time_x": "time", "step_x": "step"}, inplace=True)
        
        df["speed"] = (df["u10"]**2 + df["v10"]**2)**0.5
        df["deg"] = (180 + np.rad2deg(np.atan2(df["u10"], df["v10"]))) % 360
        
        with open("./public/wind.json", "w") as f:
            df.to_json(f, orient="index")
        
        dfSamp1000 = df.sample(1000)
        
        with open("./public/wind-sample-1000.json", "w") as f:
            dfSamp1000.to_json(f, orient="index")
            
        dfSamp2 = df.sample(2)
        
        with open("./public/wind-sample-2.json", "w") as f:
            dfSamp2.to_json(f, orient="index")
            
        dfSamp3 = df.sample(5000)
        
        with open("./public/wind-sample-5000.json", "w") as f:
            dfSamp3.to_json(f, orient="index")
        
        print("Wind data exported to ./public/wind.json")
        
    else:
        print("Wind data not exported.")


def main():
    
    parameters = ['msl', '10u', '10v']
    filename = 'medium-wind-10m.grib'
    
    filename, exp = retrieve_forecast(parameters, filename)
    process_forecast(filename, export=True) # set to true for debugging


if __name__ == "__main__":
    main()