#!/usr/bin/env python
# coding=utf-8
import datetime
import logging
import os 
import requests
import time
import traceback
from prometheus_client import start_http_server, Summary, Gauge

URL = "https://opendata.reseaux-energies.fr/api/records/1.0/search/"
# Env Variables
EXPORTER_PORT = int(os.environ.get('EXPORTER_PORT', 9143))
RUN_INTERVAL = int(os.environ.get('RUN_INTERVAL', 180))

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
CO2 = Gauge('rte_taux_co2', 'Co2 emitted per kWh')


def update_metrics():
    # HTTP Calls
    now = datetime.datetime.utcnow()
    params={
        "dataset": "eco2mix-national-tr",
        "q": "date_heure:[2021-11-03T{}:00:00Z TO 2021-11-03T{}:00:00Z]".format(now.hour - 1, now.hour + 2),
        "sort": "-date_heure",
        "facet": ["nature", "date_heure"],
        "timezone": "Europe/Paris",
        "rows": 100
    }
    res = requests.get(URL, params=params).json()
    last_record = {}
    for record in res["records"]:
        if record["fields"].get("taux_co2", None) != None:
            last_record = record
    # Variable set
    CO2.set(last_record["fields"]["taux_co2"])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_http_server(EXPORTER_PORT)

    while True:
        try:
            update_metrics()
        except Exception as e:
            print(traceback.format_exc())
        time.sleep(RUN_INTERVAL)