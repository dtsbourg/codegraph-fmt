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
import numpy as np
import astor
import json

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
        return all_asts
    except:
        print("[ERROR] Could not load pre-generated ASTs from", path, ".")
        print("[ERROR] Please run again with the --preprocess flag enabled.")

def one_hot_encoder(x, size, max=None, min=None):
    x = np.array(x)
    if max is None:
        max = np.max(x)
    if min is None:
        min = np.min(x)
    n_types =  max + 1 - min
    x_one_hot = np.zeros((size, n_types))
    x_one_hot[np.arange(size), x] = 1
    return x_one_hot

def parse_file(filename, verbose=False):
    return astor.code_to_ast.parse_file(filename)

def save_json(obj, save_dir, filename):
    with open(os.path.join(save_dir, filename), 'w') as fout:
        fout.write(json.dumps(obj))
        print("[AST]  --- Saved", fout.name)

def invert_var_map(var_map):
    inv_var_map = {}
    for node_id, var_name in var_map.items():
        if inv_var_map.get(var_name, None) is None:
            inv_var_map[var_name] = [node_id]
        else:
            inv_var_map[var_name].append(node_id)
    return inv_var_map

def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)
