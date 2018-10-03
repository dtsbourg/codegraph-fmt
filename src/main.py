"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import joblib
import astpp
import os
from collections import namedtuple
import astor


# CFG
Config = namedtuple('Config', 'datapath name verbose')
cfg = Config(os.path.join('..', 'data'), 'keras-example', False)

path = os.path.join(cfg.datapath, cfg.name, 'keras')
dumpdir = os.path.join(cfg.datapath, cfg.name, 'AST')
# END CFG

import file_parser
import project_crawler
import ast_transformer
import utils

paths = project_crawler.crawl(path, verbose=cfg.verbose)
for p in paths:
    parsed_ast = file_parser.parse(p, verbose=cfg.verbose)
    ast_dump_file = os.path.join(dumpdir, 'AST-bin-dump-'+str(os.path.basename(p))+'.ast')
    utils.save(ast=parsed_ast, filename=ast_dump_file, format='pickle')

    ast_dump = astpp.dump(parsed_ast)
    ast_dump_file = os.path.join(dumpdir, 'AST-bin-dump-'+str(os.path.basename(p))+'.txt')
    utils.save(ast=ast_dump, filename=ast_dump_file, format='txt')
