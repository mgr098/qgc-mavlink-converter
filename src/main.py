from fileinput import filename
import string
import sys
import json
import logging
import argparse

from numpy import append, require
from constants import * # TODO: change this, bad practice

# inspired by github user @phrohdoh
# TODO: try without takeoff, try many different plans to test

def parse_args():
    #TODO: create better names
    # Add takeoff off option
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Convert QGC .plan to .mavlink format")
    parser.add_argument("filename", type=str, help="Usage: python3 main.py </path/to/file/>")
    parser.add_argument("--out", type=str, help=".mavlink filename", default=DEFAULT_FILE_NAME)
    args = parser.parse_args()

    return args

class Converter():
    def __init__(self, filename, out):
        self.filename = filename 
        self.out = out
        self.qgc_plan = {}

    def main(self):
        self.verify_plan()
        self.convert_to_mavlink()

    def verify_plan(self):
        """Verifies plan format"""
        try:
            with open(self.filename) as f:
                self.qgc_plan = json.load(f)
                f.close()
        except FileNotFoundError:
            logging.error("Can't open specified file")

        #TODO: check if its a plan, and that its not empty?

    def convert_to_mavlink(self):
        """Converts plan to mavlink"""

        mav = MAVlink(self.qgc_plan, LATEST_VERSION, takeoff=True)
        self.write_to_disk(mav.f_mavlink)

    def write_to_disk(self, mavlink):
        """Writes object down to disk"""
        #TODO: add try/except
        with open(self.out, "w+") as f:
            for line in mavlink:
                f.write(str(line))
            f.close()

class MAVlink():
    def __init__(self, plan, version, takeoff):
        self.plan = plan
        self.header = "QGC WPL {}".format(version)
        self.takeoff = [0, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0] if takeoff == True else None # TODO, do this with listcomp
        self.mission_items = self.populate()
        self.f_mavlink = self.format_mavlink()
    
    def format_mavlink(self):
        f_mavlink = []

        f_mavlink.append(self.header)
        f_mavlink.append("\n")
        f_mavlink.append(self.tab_it(self.takeoff))

        for line in self.mission_items:
            tabbed_line = self.tab_it(line)
            f_mavlink.append("\n")
            f_mavlink.append(tabbed_line)

        return f_mavlink

    def populate(self):
        #TODO: better names? maybe restructure, hard to read?
        """Populates MAVlink object according to plan"""
        
        mission_items = []
        for i, item in enumerate(self.plan["mission"]["items"]):
            params = [i for i in item["params"]] 
            mission_item = [i + 1, 0, item["frame"], item["command"], *params, 1 if item ["autoContinue"] else 0]
            mission_items.append(mission_item)
        
        return mission_items

    def tab_it(self, target):
        """Insert tab between every item in target"""
        return "\t".join(str(t) for t in target)


if __name__ == "__main__":
    args = parse_args()

    converter = Converter(args.filename, args.out)
    converter.main()
