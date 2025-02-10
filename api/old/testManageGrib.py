import xarray as xr
import matplotlib.pyplot as plt
import json
import numpy as np

def create_dict(d, l = ["longitude", "latitude", "time", "step", "tp", "u10", "v10"]):
    data = dict(zip(l, [dict() for _ in range(len(l))]))
    print(data)
    c = ""
    
    for item in data.keys():
        if item in ["longitude", "latitude", "time", "step"]:
            c = "coords"
        elif item in ["tp", "u10", "v10"]:
            c = "data_vars"
        
        # if item == "wind":
        #     print(d[c]["v10"]["data"])
        #     data[item] = {
        #             "deg": [np.atan(a / b) for a, b in zip(d[c]["v10"]["data"], d[c]["u10"]["data"])],
        #             "speed": [np.sqrt(a **2 + b **2 for a, b in zip(d[c]["v10"]["data"],d[c]["u10"]["data"]))]
        #         }
            
        # else:
            # data[item]["data"] = d[c][item]["data"]
        data[item] = {
            "data": d[c][item]["data"],
            "shape": d[c][item]["encoding"]["original_shape"]
        }
        
    return data

def plot_dict(d):
    for s, step in enumerate(d.step["data"]):
        n = d.longitude["shape"][0] * d.latitude["shape"][0]
        data = dict(zip([i for i in range(n)], [dict() for _ in range(n)]))
        
        for i in range(n):
            data[i] = {
                "longitude": d.longitude["data"][i],
                "latitude": d.latitude["data"][i],
                "time": d.time["data"],
                "tp": d.tp["data"][count],
                "u10": d.u10["data"][s] ,
                "v10": d.v10["data"][count],
                "wind": {
                    "deg": np.atan(d.v10["data"][count] / d.u10["data"][count]),
                    "speed": np.sqrt(d.v10["data"][count] ** 2 + d.u10["data"][count] ** 2)
                }
            }
            
        with open(f"dataPlotStep_{s}.json", 'w') as file:
            json.dump(data, file)
    
def main():
    # for v in ds:
    #     print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

    # plt.figure()
    # plt.imshow(ds.u10[0] + ds.v10[0])
    # plt.show()

    # print(ds.u10.shape)
    # print(temp.keys())
    # print(temp["data_vars"].keys())
    # print(temp["data_vars"]["u10"].keys())
    # print(temp["data_vars"]["u10"]["encoding"])
    # print(temp["coords"]["longitude"]["data"])
    
    ds = xr.open_dataset("output.grib", engine="cfgrib", decode_times=False) # To avoid datetime incompatibility use decode_times=False kwarg in xarray.open_dataset
    temp = ds.to_dict('list', encoding=True)
    
    dataPostProcessing = create_dict(temp, ["longitude", "latitude", "time", "step", "tp", "u10", "v10"])
    test = dataPostProcessing["wind"]
    
    print(f"test : output dictionnary for the latitude key : {test}")

    with open("dataPostProcessing.json", 'w') as file:
        json.dump(dataPostProcessing, file)
    
    plot_dict(dataPostProcessing)
    
        


if __name__ == "__main__":
    main()