#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

pip install influxdb-client
cp solaredge_to_influx.service /lib/systemd/system/solaredge_to_influx.service
systemctl daemon-reload
systemctl enable shellscript.service
systemctl start shellscript.service