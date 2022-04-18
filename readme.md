# InfluxDB
`mkdir influxdb`

`docker run -d -p 8086:8086 --restart=always -v influxdb2:/var/lib/influxdb2 --name=influx influxdb:2.0`

On running container:

`docker exec influxdb2 influx setup --username $USERNAME --password $PASSWORD --org home --bucket solaredge`

Generate access token:

`influx auth create --org home -u $USERNAME --write-bucket $BUCKET_ID --read-bucket $BUCKET_ID`

# Scrapper
Edit `config.ini` and fill all required data
Run `setup.sh` as root

# Grafana
`docker run -d --restart=always --name=grafana -p 3000:3000 grafana/grafana`

1. Setup Influx DataSource
2. Add graphs:
```
from(bucket: "solaredge")
  |> range(start: v.timeRangeStart, stop:v.timeRangeStop)
  |> filter(fn: (r) =>
    r._measurement == "energy_produced_15_min" and
    r._field == "energy"
  )
  |> aggregateWindow(every: 1h, fn: sum)
```

