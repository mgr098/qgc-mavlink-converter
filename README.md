# QGroundControl Plan to MAVlink Converter

Convert QGroundControl JSON .plan file to Parrot compatible MAVlink file used for AirSDK FlightPlans. 

## Requirements
* python3

## Usage

clone the repo

```
python3 convert.py /path-to-qgc-plan/ /location/
```

## About

The scripts adds a takeoff before anything else, because the drone wont really do anything befor you do so. Unsure how mavlink and qgc works? check out the docs, or check out my guide.

## TODO

* convert the file to .mavlink
    * verify input arguments
    * verify file and file format
    * verify compatible to parrot
* add script that runs this on a simulator

## Contributing