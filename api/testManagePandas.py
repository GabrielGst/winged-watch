import xarray as xr
import matplotlib.pyplot as plt
import json
import numpy as np
import pandas as pd


def main(): 
    ds = xr.open_dataset("output.grib", engine="cfgrib", decode_times=False) # To avoid datetime incompatibility use decode_times=False kwarg in xarray.open_dataset
    
    u10 = ds.get("u10")
    df_u = u10.to_dataframe()
    df_u.drop(columns=["number", "time", "heightAboveGround", "valid_time", "surface"], inplace=True)
    
    # print(f"keys : {df_u.keys()}")
    # print(f"head : {df_u.head()}")
    
    v10 = ds.get("v10")
    df_v = v10.to_dataframe()
    df_v.drop(columns=["number", "time", "heightAboveGround", "valid_time", "surface"], inplace=True)
    
    df = pd.merge(df_u, df_v, left_index=True, right_index=True, how='left') # on=["step", "latitude", "longitude"] here we are joining on indexes
    
    df["speed"] = np.sqrt(df["v10"] ** 2 + df["u10"] ** 2)
    df["deg"] = np.arctan(df["v10"] / df["u10"])
    

    print(df.head())
    
    # df.to_json("dataPostProcessing.json")
    
    print(df.keys())
    df["longitude"] = df.index.get_level_values(2)
    df["latitude"] = df.index.get_level_values(1)
    print(df.keys())
    
    df = df[df.index.get_level_values(0) == 0.0]
    df = df.sample(1000)
    lon = df.index.get_level_values(2).tolist()
    lat = df.index.get_level_values(1).tolist()
    
    lon, lat = np.meshgrid(lon, lat)
    
    u = 1 # df["u10"].values.tolist()
    v = -1 # df["v10"].values.tolist()

    plt.quiver(lon, lat, u, v)
    plt.show()


if __name__ == "__main__":
    main()