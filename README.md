# QGroundControl Plan to MAVlink Converter ♻️

Convert QGroundControl (QGC) JSON .plan file to Parrot compatible MAVlink file used for AirSDK FlightPlans. 

## Requirements ✔

* [python3](https://www.python.org/)

## Usage

Clone the repository and navigate to /src. In your terminal run

```
python3 main.py /path/to/qgc.plan
```

## About

This Python script was created in order to upload QGC plans to the ANAFI AI drone. It also contains a file that uploads and runs a .mavlink file on a Parrot drone. Check out /src/README.md to see information on how to run both scripts with optional arguments. 

## TODO

* verify plan commands are compatible to parrot
* test with multiple plans
* add script that runs this on a simulator

## Contributing 

## Acknowledgments