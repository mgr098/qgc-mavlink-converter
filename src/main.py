from fileinput import filename
import string
import sys
import json
import logging
import argparse

from numpy import require
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

        mav = MAVlink(LATEST_VERSION)

        """Converts plan to mavlink"""
        mav = [[], []]
        mav[0].append("QGC WPL" + LATEST_VERSION) # Add meta data

        # Add takeoff first
        counter = 0
        cmd_line = [counter, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0] # TODO, do this with listcomp

        # TODO: Move this to a class
        for i, item in enumerate(self.qgc_plan["mission"]["items"]):
            params = [i for i in item["params"]]
            #TODO: check for autoconintue
            self.line = [i + 1, 0, item["frame"], item["command"], *params, 1 if item["autoContinue"] else 0] # TODO: do this with listcomp
            self.lines.append(self.line)
        
        self.write_to_disk(mav, cmd_line)

    def write_to_disk(self, mav, cmd_line):
        #TODO: Move this to a function 
        with open("output.mavlink", "w+") as f:
            f.write(str(*mav[0]))
            f.write("\n")

            cmd_line = self.tab_it(cmd_line)
            f.write(cmd_line)

            for line in self.lines:
                f.write("\n")
                f.write(self.tab_it(line))
            
            f.close()

"""MAVlink object"""
class MAVlink():
    def __init__(self, version) -> None:
        self.header = "QGC WPL {}".format(version)

    def main(self):
        print(self.header)

if __name__ == "__main__":
    args = parse_args()

    converter = Converter(args.filename, args.out)
    converter.main()
