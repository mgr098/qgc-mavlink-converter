from fileinput import filename
import string
import sys
import json
import logging
import argparse

from numpy import append, require
from constants import * # TODO: change this, bad practice

# inspired by github user @phrohdoh

def parse_args():
    #TODO: create better names

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

        self.lines = []
        self.qgc_plan = {}

    def main(self):

        self.verify_plan()
        self.convert_to_mavlink()

        return

    def verify_plan(self):
        """Verifies plan format"""
        try:
            with open(self.filename) as f:
                self.qgc_plan = json.load(f)
                f.close()
        except FileNotFoundError:
            logging.error("Can't open specified file")

        #TODO: check if its a plan, and that its not empty?
    
    def tab_it(self, line):
        char = "\t"
        tabs = char.join(str(v) for v in line)
        return tabs

    def convert_to_mavlink(self):
        """Converts plan to mavlink"""

        mav = MAVlink(self.qgc_plan, LATEST_VERSION, takeoff=True)
        mav.main()
        self.write_to_disk(mav.f_mavlink)
        return 

        # mav = []
        # mav.append("QGC WPL" + LATEST_VERSION) # Add meta data

        # # Add takeoff first
        # counter = 0
        # cmd_line = [counter, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0] # TODO, do this with listcomp

        # # TODO: Move this to a class
        # for i, item in enumerate(self.qgc_plan["mission"]["items"]):
        #     params = [i for i in item["params"]]
        #     self.line = [i + 1, 0, item["frame"], item["command"], *params, 1 if item["autoContinue"] else 0] # TODO: do this with listcomp
        #     self.lines.append(self.line)
        
        # self.write_to_disk(mav, cmd_line)

    def write_to_disk(self, mav):
        #TODO: Move this to a function 



        # for i in self.lines:
        #     i.append("\n")
        
        
        # print(self.lines)
        # skr = []
        # for i in self.lines:
        #     tabbed = self.tab_it(i)
        #     for j in tabbed:
        #         skr.append(j)
        # o = [*mav, self.tab_it(cmd_line)]
                
        # for i in self.lines:
        #     tabbed = self.tab_it(i)
        #     o.append(tabbed)

        # print(o)

        with open("output.mavlink", "w+") as f:
            # f.write(str(mav))
            # f.write("\n")

            # cmd_line = self.tab_it(cmd_line)
            # f.write(cmd_line)

            # for line in self.lines:
            #     f.write("\n")
            #     f.write(self.tab_it(line))
            for i in mav:
                f.write(str(i))
                # f.write("\n")
            f.close()

class MAVlink():
    def __init__(self, plan, version, takeoff):
        self.plan = plan

        self.header = "QGC WPL {}".format(version)
        self.takeoff = [0, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0] if takeoff == True else None # TODO, do this with listcomp
        self.mission_items = self.populate()

        self.mavlink = [self.header, *self.takeoff, *self.mission_items] 
        self.f_mavlink = self.format_mavlink()

    def main(self):
        print(self.f_mavlink)
    
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
