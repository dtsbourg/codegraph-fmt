"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import joblib
import os
from collections import namedtuple
import astor


# CFG
Config = namedtuple('Config', 'datapath name verbose')
cfg = Config(os.path.join('..', 'data'), 'code-sample', False)

path = os.path.join(cfg.datapath, cfg.name, 'raw')
dumpdir = os.path.join(cfg.datapath, cfg.name, 'AST')
# END CFG

import file_parser
import project_crawler
import ast_transformer
import utils
import ast_networkx

paths = project_crawler.crawl(path, verbose=cfg.verbose)
for idx,p in enumerate(paths):
    if cfg.verbose:
        print("[MAIN] Processing path", p)
    parsed_file = str(os.path.basename(p))
    save_file = 'AST-bin-dump-'+parsed_file

    parsed_ast = file_parser.parse(p, verbose=cfg.verbose)
    ast_dump_file = os.path.join(dumpdir, save_file+'.ast')
    utils.save(ast=parsed_ast, filename=ast_dump_file, format='pickle')

    ast_dump = astor.dump_tree(parsed_ast)
    ast_dump_file_txt = os.path.join(dumpdir, save_file+'.txt')
    utils.save(ast=ast_dump, filename=ast_dump_file_txt, format='txt')

    print("\r[MAIN]  --- Saving parsed AST for file {0}/{1} ...".format(idx+1,len(paths)), end='\r')
print()
print("[MAIN]  --- Saved parsed AST for {0} files in {1}.".format(len(paths), dumpdir))
print()

ast_networkx.generate_json(ast_dump_file, dumpdir)
