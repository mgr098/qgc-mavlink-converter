import json
import logging
import argparse
from constants import LATEST_VERSION, TAKEOFF, DEFAULT_FILE_NAME

logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

def parse_args():
    parser = argparse.ArgumentParser(description="Convert QGC .plan to .mavlink format")

    parser.add_argument(
        "filepath", type=str, help="Usage: python3 main.py </path/to/file/>")
    parser.add_argument(
        "--out", type=str, help="MAVlink filename", default=DEFAULT_FILE_NAME)
    parser.add_argument(
        "--version", type=str, help="MAVlink version", default=LATEST_VERSION)
    parser.add_argument(
        "--takeoff", type=str, help="Add takeoff at start of mavlink", default=False)

    return parser.parse_args()


"""
This class manages the .plan conversion by 
loading the .plan, initializing the mav object
and writing the formated mav object to a new file
"""
class Converter():
    def __init__(self, filepath, out, takeoff, version):
        self.filepath = filepath 
        self.out = out
        self.takeoff = takeoff
        self.version = version
        self.plan = {}

    def main(self):
        self.verify_format()
        mav = Mav(self.plan, self.version, self.takeoff)
        self.write_to_disk(mav.file)

        print("Successfully converted {} to {}".format(self.filepath, self.out))

    def verify_format(self):
        """Verifies plan format"""
        #TODO: check if its a .plan, and that its not empty
        try:
            with open(self.filepath) as f:
                self.plan = json.load(f)
                f.close()
        except FileNotFoundError:
            logging.error("Can't open specified file")
        except:
            logging.error("Unexpected error")

    def write_to_disk(self, mav):
        """Write mavlink object to file"""
        try:
            with open(self.out, "w+") as f:
                for line in mav:
                    f.write(str(line))
                f.close()
        except:
            logging.exception("Unexpected error, could not append MAVlink object to file")

"""
This class converts a JSON .plan file to a 
formated mavlink file
"""
class Mav():
    def __init__(self, plan, version, takeoff):
        self.plan = plan
        self.header = "QGC WPL {}".format(version)
        self.takeoff = takeoff
        
        self.mission_items = self.convert()
        self.file = self.format_items()
    
    def format_items(self):
        mav_file = []
        mav_file.append(self.header)

        # Not sure if this is needed.
        # However, parrot drones need to takeoff
        # before other drone functions are activated
        if self.takeoff: 
            self.takeoff = [0, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0]
            mav_file.append("\n")
            mav_file.append(self.insert_tabs(self.takeoff))

        for line in self.mission_items:
            mav_file.append("\n")
            mav_file.append(self.insert_tabs(line))

        return mav_file

    def convert(self):
        """Convert plan according to MAVlink"""
        mission_items = []

        for i, item in enumerate(self.plan["mission"]["items"]):
            if item["type"] == "SimpleItem":
                params = [i for i in item["params"]] 
                mission_item = [i + 1, 0, item["frame"], item["command"], *params, 
                                1 if item ["autoContinue"] else 0]

                mission_items.append(mission_item)
            else:
                logging.warning("Cannot convert type: complexItem")
        
        return mission_items

    def insert_tabs(self, target):
        """Insert tab between every item in target"""
        return "\t".join(str(t) for t in target)


if __name__ == "__main__":
    args = parse_args()

    converter = Converter(args.filepath, args.out, args.takeoff, args.version)
    converter.main()
