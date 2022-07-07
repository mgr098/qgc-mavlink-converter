import sys
import json
from constants import * # TODO: change this, bad practice

# inspired by github user @phrohdoh

def verify_args():
    """Parse and verify input arguments"""
    # TODO:
    # Verify string input type, and arg counts

    return sys.argv[1]


class Converter():
    def __init__(self):
        self.file_location = verify_args()
        self.latest_version = "120" #TODO: change this
        self.lines = []

    def main(self):

        self.convert_to_mavlink()

        self.write_to_disk()

    def verify_plan(self):
        """Verifies plan format and version"""
        #TODO:
        # verify that it is a plan
        # try except
        # try:
        #     with open(self.file_location) as f:
        #         plan = f.readlines()
        # except FileNotFoundError:
        #     raise FileNotFoundError("This file can't be found")
        # except:
        #     print("unhandled error?")

        # version = plan[0] # do some stuff here
        # if not version in ACCEPTED_VERSIONS:
        #     raise ValueError("This version is not accepted")
        pass
    
    def tab_it(self, line):
        char = "\t"
        tabs = char.join(str(v) for v in line)
        return tabs


    def convert_to_mavlink(self):
        """Converts plan to mavlink"""
        qgc_plan = {}
        with open(self.file_location) as f:
            qgc_plan = json.load(f)
            f.close()

        mav = [[], []]
        mav[0].append("QGC WPL" + self.latest_version) # Add meta data

        # Add takeoff first
        counter = 0
        cmd_line = [counter, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0] # TODO, do this with listcomp

        # TODO: Move this to a class
        for i, item in enumerate(qgc_plan["mission"]["items"]):
            params = [i for i in item["params"]]
            #TODO: check for autoconintue
            self.line = [i + 1, 0, item["frame"], item["command"], *params, 1 if item["autoContinue"] else 0] # TODO: do this with listcomp
            self.lines.append(self.line)
            
        #TODO: Move this to a function 
        with open("output.mavlink", "w+") as f:
            f.write(str(*mav[0]))
            f.write("\n")

            cmd_line = self.tab_it(cmd_line)
            f.write(cmd_line)

            for line in self.lines:
                f.write("\n")
                f.write(self.tab_it(line))

    def write_to_disk(self):
        pass

if __name__ == "__main__":
    converter = Converter()
    converter.main()