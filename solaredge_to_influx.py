import os
import requests
import configparser
import json
from argparse import ArgumentParser
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

parser = ArgumentParser()
parser.add_argument("-s", "--since", dest="since", default=datetime.today().strftime('%Y-%m-%d'), help="Since date YYYY-MM-DD")
parser.add_argument("-u", "--until", dest="until", default=datetime.today().strftime('%Y-%m-%d'), help="Until date YYYY-MM-DD")
args = parser.parse_args()

config = configparser.ConfigParser()
config_path = os.path.dirname(__file__) + '/config.ini'
config.read(config_path)

api_key = config["solaredge"]["api_key"]
installation_id = config["solaredge"]["installation_id"]

r = requests.get("https://monitoringapi.solaredge.com/site/{}/energy?timeUnit=QUARTER_OF_AN_HOUR&endDate={}&startDate={}&api_key={}".format(installation_id, args.until, args.since, api_key))
energy = json.loads(r.text)

client = influxdb_client.InfluxDBClient(url=config["influx"]["url"], token=config["influx"]["token"], org=config["influx"]["org"])
write_api = client.write_api(write_options=SYNCHRONOUS)

for reading in energy["energy"]["values"]:
    p = influxdb_client.Point("energy_produced_15_min").tag("location", "Sosnowiec").time(reading["date"]).field("energy", reading["value"])
    write_api.write(bucket=config["influx"]["bucket"], org=config["influx"]["org"], record=p)
