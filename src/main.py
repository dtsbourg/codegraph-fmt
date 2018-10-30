"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg), Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import os
from collections import namedtuple
import astor
import argparse


# CFG
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", default=False, type=bool,  dest="verbose")
parser.add_argument("--datapath", type=str,  dest="datapath", help='path to data folder')
parser.add_argument("--name", type=str, dest="name", help='name of codebase')
cfg = parser.parse_args()

path = os.path.join(cfg.datapath, cfg.name, 'raw')
dumpdir = os.path.join(cfg.datapath, cfg.name, 'AST')
#print(path, dumpdir)
# END CFG

import file_parser
import project_crawler
import ast_transformer
import utils
import ast_networkx

paths = project_crawler.crawl(path, verbose=cfg.verbose)
all_ast_dump = []
for idx,p in enumerate(paths):
    if cfg.verbose:
        print("[MAIN] Processing path", p)
    parsed_file = str(os.path.basename(p))
    save_file = 'AST-bin-dump-'+parsed_file

    parsed_ast = file_parser.parse(p, verbose=cfg.verbose)
    ast_dump_file = os.path.join(dumpdir, save_file+'.ast')
    all_ast_dump.append(ast_dump_file)
    utils.save(ast=parsed_ast, filename=ast_dump_file, format='pickle')

    ast_dump = astor.dump_tree(parsed_ast)
    ast_dump_file_txt = os.path.join(dumpdir, save_file+'.txt')
    utils.save(ast=ast_dump, filename=ast_dump_file_txt, format='txt')

    print("\r[MAIN]  --- Saving parsed AST for file {0}/{1} ...".format(idx+1,len(paths)), end='\r')
print()
print("[MAIN]  --- Saved parsed AST for {0} files in {1}.".format(len(paths), dumpdir))
print()

ast_networkx.generate_json(all_ast_dump, dumpdir)
