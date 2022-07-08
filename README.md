# QGroundControl Plan to MAVlink Converter ♻️
Convert [QGroundControl (QGC)](http://qgroundcontrol.com/) JSON .plan file to [Parrot compatible MAVlink](https://developer.parrot.com/docs/mavlink-flightplan/overview.html) file used for [AirSDK Flight mission](https://developer.parrot.com/docs/airsdk/general/overview.html). 

## Requirements ✔

* [Python 3](https://www.python.org/)

## Usage ⚙️

Clone the repository and navigate to /src. In your terminal run

```
python3 main.py /path/to/qgc.plan
```

## About 📝

This Python script was created in order to upload QGC plans to the ANAFI AI drone. It also contains a script that uploads and starts an AirSDK mission on a Parrot drone using a mavlink file. Read the [documentation](./src/README.md) to run both scripts with optional arguments. 

## TODO

* verify plan commands are compatible to parrot
* test with multiple plans
* add script that runs this on a simulator

## Contributing ✍️
## Acknowledgments
## Related
[Parrot Guide](https://github.com/mgr098/parrot-guide) - An unofficial guide to the Parrot Ecosystem
[Simulated Drone Flight](https://github.com/mgr098/simulated-drone-flight) - A Python script that remotely controls a simulated ANAFI AI drone in the Parrot Sphinx simulator