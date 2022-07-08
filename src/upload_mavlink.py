import sys
import olympe
from olympe.messages.common.Mavlink import Start
from olympe.messages.common.MavlinkState import (
    MavlinkFilePlayingStateChanged,
    MissionItemExecuted,
)

import requests
import os

#TODO: Add arg parser
olympe.log.update_config({"loggers": {"olympe": {"level": "ERROR"}}})

drone_ip = "10.202.0.1"

headers = {
    "Accept": "application/json, text/javascript, text/plain */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Content-type": "application/json; charset=UTF-8; application/gzip",
}

drone = olympe.Drone(drone_ip)
drone.connect()

filepath = sys.argv[1]

# Upload mavlink file
with open(filepath, "rb") as data:
    resp = requests.put(
        url=os.path.join("http://", drone_ip, "api/v1/upload", "flightplan"),
        headers=headers,
        data=data,
    )

# Start flightplan
expectation = drone(
    Start(resp.json(), type="flightPlan")
).wait(_timeout=200)

assert expectation
