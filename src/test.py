"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import joblib
import astpp
import os
from collections import namedtuple

# CFG
Config = namedtuple('Config', 'datapath name')
cfg = Config(os.path.join('..', 'data'), 'code-sample')

path = os.path.join(cfg.datapath, cfg.name, 'raw')
dumpdir = os.path.join(cfg.datapath, cfg.name, 'AST')
# END CFG

#####################################
# Astor example
####################################

import astor

for file in os.listdir(path):
    if file.endswith(".py"):
        f = os.path.join(path, file)
        print("Processing file", f)
        parsed_ast = astor.code_to_ast.parse_file(f)
        ast_dump = astpp.dump(parsed_ast)
        with open(os.path.join(dumpdir, 'AST-str-dump.txt'), 'w') as f:
            f.write(ast_dump)
        joblib.dump(parsed_ast, os.path.join(dumpdir, 'AST-bin-dump.ast'))
        print(ast_dump)
        print()
