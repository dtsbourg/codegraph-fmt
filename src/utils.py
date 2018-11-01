"""
`utils.py`
----------

Module that should process a given project and
build the index of relevant source code files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import pickle
import os

import project_crawler

def save(ast, filename, format='pickle'):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

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
                return pickle.load(handle)
        except:
            print("[ERROR] Could not open file", filename)

    elif format == 'txt':
        print("[LOAD] Parsing file ...")
    else:
        print("[ERROR] Please specify a valid format.")
        return None

def load_asts(path, verbose=False):
    try:
        asts = project_crawler.crawl(path, filetype='.ast')
        all_asts = []

        for idx, ast in enumerate(asts):
            loaded = load(ast)
            all_asts.append(loaded)
            if verbose:
                print("\r[LOAD]  --- Loading parsed AST {0}/{1} ...".format(idx+1,len(asts)), end='\r')
        print()
        print(all_asts)
        return all_asts
    except:
        print("[ERROR] Could not load pre-generated ASTs from", path, ".")
        print("[ERROR] Please run again with the --preprocess flag enabled.")
