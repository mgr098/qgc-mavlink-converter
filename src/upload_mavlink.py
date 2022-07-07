import olympe
from olympe.messages.common.Mavlink import Start
from olympe.messages.common.MavlinkState import (
    MavlinkFilePlayingStateChanged,
    MissionItemExecuted,
)

import requests
import os

drone_ip = "10.202.0.1"

headers = {
    "Accept": "application/json, text/javascript, text/plain */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Content-type": "application/json; charset=UTF-8; application/gzip",
}

drone = olympe.Drone(drone_ip)
drone.connect()

# Upload mavlink file
with open("mavtest.mavlink", "rb") as data:
    resp = requests.put(
        url=os.path.join("http://", drone_ip, "api/v1/upload", "flightplan"),
        headers=headers,
        data=data,
    )

# Start flightplan
expectation = drone(
    Start(resp.json(), type="flightPlan")
    >> MissionItemExecuted(idx=0.0)
    >> MissionItemExecuted(idx=1.0)
    >> MissionItemExecuted(idx=2.0)
    >> MissionItemExecuted(idx=3.0)
    >> MissionItemExecuted(idx=4.0)
    >> MissionItemExecuted(idx=5.0)
    >> MissionItemExecuted(idx=6.0) 
    >> MissionItemExecuted(idx=7.0) 
    >> MavlinkFilePlayingStateChanged(state="stopped")
).wait(_timeout=200)

assert expectation
