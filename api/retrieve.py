# https://apps.ecmwf.int/datasets/data/s2s-reforecasts-instantaneous-accum-ecmf/levtype=sfc/type=cf/?realtime_date=2025-01-23&model_date=2025-02-11&hindcast_date=2024-02-11&step=0,6,12,18,24,30,36,42,48&param=165,166,172,151,228228,228205

from ecmwfapi import ECMWFDataServer
from dotenv import load_dotenv
import os

def retrieve():
    load_dotenv()
    # print(os.getenv("ECMWF_API_RC_FILE")) # Debug

    server = ECMWFDataServer()

    # server.retrieve({
    #     "class": "s2",
    #     "dataset": "s2s",
    #     "date": "2025-02-11",
    #     "expver": "prod",
    #     "hdate": "2024-02-11",
    #     "levtype": "sfc",
    #     "model": "glob",
    #     "origin": "ecmf",
    #     "param": "151/172/228205",
    #     "step": "0/24/48",
    #     "stream": "enfh",
    #     "time": "00:00:00",
    #     "type": "cf",
    #     "target": "output.grib2"
    # })

    server.retrieve({
        "class": "s2",
        "dataset": "s2s",
        "date": "2025-02-11",
        "expver": "prod",
        "hdate": "2024-02-11",
        "levtype": "sfc",
        "model": "glob",
        "origin": "ecmf",
        "param": "165/166/228228",
        "step": "0/6/12/18/24/30/36/42/48",
        "stream": "enfh",
        "time": "00:00:00",
        "type": "cf",
        "target": "output.grib"
    })

    size = os.path.getsize("output.grib")
    print(f"File output.grib is of size: {size}")

if __name__ == "__main__":
    retrieve()