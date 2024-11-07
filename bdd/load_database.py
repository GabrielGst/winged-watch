import pygrib

# Open the .grib2 file
# filename = "./bdd/arome__001__HP1__00H__2024-11-07T09_00_00Z.grib2"
filename = "./bdd/constant-arome-eurw1s40-2024.grib2"
grib_file = pygrib.open(filename)

# Inspect the first message (one layer of the data)
grib_message = grib_file.message(1)
print(grib_message)

# Access the data as a numpy array
data, lats, lons = grib_message.data()

# Close the file after reading
grib_file.close()
