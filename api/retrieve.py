# https://apps.ecmwf.int/datasets/data/s2s-reforecasts-instantaneous-accum-ecmf/levtype=sfc/type=cf/?realtime_date=2025-01-23&model_date=2025-02-11&hindcast_date=2024-02-11&step=0,6,12,18,24,30,36,42,48&param=165,166,172,151,228228,228205

from ecmwfapi import ECMWFDataServer

server = ECMWFDataServer()

server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2025-02-11",
    "expver": "prod",
    "hdate": "2024-02-11",
    "levtype": "sfc",
    "model": "glob",
    "origin": "ecmf",
    "param": "151/172/228205",
    "step": "0/24/48",
    "stream": "enfh",
    "time": "00:00:00",
    "type": "cf",
    "target": "output"
})

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
    "target": "output"
})