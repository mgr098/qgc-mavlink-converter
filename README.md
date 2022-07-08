# QGroundControl Plan to MAVlink Converter ♻️
Convert [QGroundControl (QGC)](http://qgroundcontrol.com/) JSON .plan file to [Parrot compatible MAVlink](https://developer.parrot.com/docs/mavlink-flightplan/overview.html) file used for [AirSDK Flight mission](https://developer.parrot.com/docs/airsdk/general/overview.html). 

## Requirements ✔

* [Python 3](https://www.python.org/)

## Setup ⚙️

Clone the project and navigate to the /src folder
```
git clone https://github.com/mgr098/qgc-mavlink-converter.git
cd src
```
## Usage 🖥
In your terminal run
```
python3 main.py /path/to/qgc.plan
```


<details>
<summary> View optional arguments </summary>
<br>

```
python3 main.py --help
```
Output
```
usage: main.py [-h] [--out OUT] [--version VERSION]
               [--takeoff TAKEOFF]
               filepath

Convert QGC .plan to .mavlink format

positional arguments:
  filepath           Usage: python3 main.py </path/to/file/>

optional arguments:
  -h, --help         show this help message and exit
  --out OUT          MAVlink filename
  --version VERSION  MAVlink version
  --takeoff TAKEOFF  Add takeoff at start of mavlink
```
Example usecase of optional arguments

```
python3 main.py qgc.plan --out output.mavlink --version 120 --takeoff True
```
</details>

## Limitations 🚨

Does not support conversion of item type "complexItem" because it does not have a standard .mavlink format.

## About 📝

This project was created in order to upload QGC plans to the ANAFI AI drone. It also contains a script that uploads and starts an AirSDK mission on a Parrot drone using a mavlink file. Read the [documentation](./src/README.md) on how to to run both scripts. 
