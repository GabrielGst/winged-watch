# import xarray as xr

# ds = xr.open_dataset("./bdd/arome__001__HP1__00H__2024-11-07T09_00_00Z.grib2", engine="cfgrib")

# for v in ds:
#     print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))
    
import cfgrib

# Load all layers, separated into individual datasets
datasets = cfgrib.open_datasets("./bdd/arome__0025__SP1__00H06H__2024-11-07T21_00_00Z.grib2")

# Print information about each dataset
for i, ds in enumerate(datasets):
    print(f"Dataset {i}:")
    print("\n")
    print(ds)
    print("\n")
    print("Next:\n")
