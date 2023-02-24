# Personnal
from run_state import RunState

# Std
import re

# Third party
import numpy as np


f_instance = './instances/'


class KServerInstance:

    # Grid dimensions, not used
    grid_width  = 100
    grid_height = 100
    # pattern to split quickly over fields
    field = "# [A-Z, a-z]*\n"

    def __init__(self):
        self.k = None  # number of technicians
        self.opt = None  # opt value

        # list of tuple coordinates. The indice i can be interpreted as a customer
        self.sites = None

        # The list of requests from the customers.
        # The j-th request is the one at coordinates sites[request[j]]
        self.requests = None

    def parse(self, f_name: str) -> None:
        rm_stuff = (lambda stuff, word: word.replace(stuff, ""))
        to_pairs = (lambda words: list([(w.split(" ")[0], w.split(" ")[1]) for w in words]))
        with open(f_instance + f_name) as f:
            data = f.read()
            lines = re.split(self.field, data)
            self.opt = int(rm_stuff("\n", lines[1]))
            self.k = int(rm_stuff("\n", lines[2]))
            coords_str = to_pairs(rm_stuff("\n\n", lines[3]).split("\n"))
            self.sites = [(int(x), int(y)) for x, y in coords_str]
            requests_str = rm_stuff("\n", lines[4]).split(" ")[:-1]
            self.requests = list([int(w) for w in requests_str])

            # print(self.opt)
            # print(self.k)
            # print(self.sites)
            # print(self.requests)


if __name__ == "__main__":
    kinstance = KServerInstance()
    kinstance.parse("instance_N200_OPT347.inst")

