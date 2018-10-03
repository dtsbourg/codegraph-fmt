"""
`file_parser.py`
----------------

Module that will fetch and read a file, then pass it
to be processed by the AST parser.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import os
import astor

def parse(filename, verbose=False):
    if verbose:
        print("[READER] Processing file", filename)
    return astor.code_to_ast.parse_file(filename)
