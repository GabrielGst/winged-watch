# https://github.com/ecmwf/ecmwf-opendata
# https://github.com/ecmwf/cfgrib

from ecmwf.opendata import Client
import xarray as xr
import xarray_extras as xrx

def retrieve_forecast(parameters, filename):
    
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
    
def process_forecast(filename):
    ds = xr.open_dataset(filename, engine="cfgrib", decode_times=False) # To avoid datetime incompatibility use decode_times=False kwarg in xarray.open_dataset
    u10 = ds["u10"]
    v10 = ds["v10"]
    
    udf = u10.to_dataframe()
    vdf = v10.to_dataframe()
    
    udf.to_json("u10.json")
    vdf.to_json("v10.json")
    
    udf.head(10)
    

    
    
def main():
    
    parameters = ['msl', '10u', '10v']
    filename = 'medium-wind-10m.grib'
    
    # retrieve_forecast(parameters, filename)
    
    process_forecast(filename)


if __name__ == "__main__":
    main()