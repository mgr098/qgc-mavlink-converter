# Convert and Upload MAVlink ⚡️

This folder contains Python scripts that can convert QGC JSON .plan file to .mavlink file and upload it to an ANAFI AI drone.

## Folder Structure 🗃️
```
└── Src
    ├── constants.py            Constants used by main.py
    ├── main.py                 Converts JSON .plan to .mavlink
    ├── README.md               This README
    └── upload_mavlink.py       Uploads .mavlink to drone and starts it    
```

## Setup ⚙️

Clone the project and navigate to the /src folder
```
git clone https://github.com/mgr098/qgc-mavlink-converter.git
cd src
```

## Convert .plan to .malink ♻️

In your terminal run
```
python3 main.py /path/to/qgc.plan
```

<details>
<summary> To view arguments</summary>
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
python3 main.py qgc.plan --out mission.mavlink --version 120 --takeoff True
```
</details>

## Upload .mavlink to ANAFI AI drone ✈️

### Prerequisites ✔

* [Parrot Sphinx](https://developer.parrot.com/docs/sphinx/)

### Usage 🖥

To upload the .mavlink file to the drone and start the mission, run this in your terminal
```
python3 upload_mavlink.py mission.mavlink
```



