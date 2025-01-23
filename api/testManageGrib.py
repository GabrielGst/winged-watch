import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset("output.grib", engine="cfgrib")

for v in ds:
    print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

# plt.figure()
# plt.imshow(ds.u10[0] + ds.v10[0])
# plt.show()

print(ds.u10.shape)