# import xarray as xr

# ds = xr.open_dataset("./bdd/arome__001__HP1__00H__2024-11-07T09_00_00Z.grib2", engine="cfgrib")

# for v in ds:
#     print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))
    
import cfgrib
import pandas

# Load all layers, separated into individual datasets
datasets = cfgrib.open_datasets("./bdd/arome__0025__SP1__00H06H__2024-11-07T21_00_00Z.grib2")

# Print information about each dataset
# for i, ds in enumerate(datasets):
#     print(f"Dataset {i}:")
#     print("\n")
#     print(ds)
#     print("\n")
#     print("Next:\n")


wind_speed = datasets[1].si10
wind_direction = datasets[1].wdir10

# print(wind_speed)
# print(wind_direction)

df = wind_direction.to_dataframe()
df2 = wind_speed.to_dataframe()

df.head(10).style


# import plotly.express as px

# fig = px.scatter_geo(
#     df, locations="iso_alpha",
#     size="pop", # size of markers, "pop" is one of the columns of gapminder
# )

# fig.show()

# df.to_csv("wind_direction.csv", index=False)

# df2.to_csv("wind_speed.csv", index=False)