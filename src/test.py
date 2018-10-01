"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import astpp
import os
from collections import namedtuple

# CFG
Config = namedtuple('Config', 'datapath name')
cfg = Config(os.path.join('..', 'data'), 'code-sample')

path = os.path.join(cfg.datapath, cfg.name, 'raw')
dumpdir = os.path.join(cfg.datapath, cfg.name, 'AST')
# END CFG


for file in os.listdir(path):
    if file.endswith(".py"):
        f = os.path.join(path, file)
        print("Processing file", f)
        with open(f, 'r') as myfile:
           data=myfile.read()
        astpp.pdp(data, dumpdir=dumpdir)
