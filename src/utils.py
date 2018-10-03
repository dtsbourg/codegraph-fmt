"""
`utils.py`
----------

Module that should process a given project and
build the index of relevant source code files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import pickle


def save(ast, filename, format='pickle'):
    if format=='pickle':
        with open(filename, 'wb') as handle:
            pickle.dump(ast, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif format=='txt':
        with open(filename, 'w') as handle:
            handle.write(ast)

def load(filename, format='pickle'):
    if format == 'pickle':
        try:
            with open(filename, 'rb') as handle:
                print("[LOAD] Loading file", filename, "...")
                return pickle.load(handle)
        except:
            print("[ERROR] Could not open file", filename)

    elif format == 'txt':
        print("[LOAD] Parsing file ...")
    else:
        print("[ERROR] Please specify a valid format.")
        return None
