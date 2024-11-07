import xarray as xr

# Load the .grib2 file as an xarray dataset
ds = xr.open_dataset(".bdd/arome", engine="cfgrib")

# Print the dataset structure and contents
print(ds)

# Access a specific variable in the dataset (e.g., temperature)
temperature = ds['t']  # replace 't' with the actual variable name in your file

# Work with the data
print(temperature.mean(dim=["latitude", "longitude"]))

# Close the dataset when done (xarray handles this automatically when out of scope)
ds.close()
