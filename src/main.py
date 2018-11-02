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
parser = argparse.ArgumentParser(description="Configure the AST generation and parsing script.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--verbose", action="store_true", dest="verbose")
parser.add_argument("--preprocess", action="store_true", dest="preprocess", help="If flag is passed, the ASTs will be re-generated. Otherwise, the script will load pre-generated AST")
parser.add_argument("-d", "--datadir",    type=str, default="../data",      dest="datadir",    help="Path to the top level data directory.")
parser.add_argument("-n", "--name",       type=str, default="code-sample",  dest="name",       help="Identifier for the mined directory.")
parser.add_argument("-c", "--codefolder", type=str, default="raw",          dest="codefolder", help="Raw code folder identifier.")
parser.add_argument("-p", "--pregenpath", type=str, default="AST",          dest="pregenpath", help="Pre-generated AST folder identifier.")
cfg = parser.parse_args()

path    = os.path.join(cfg.datadir, cfg.name, cfg.codefolder)
dumpdir = os.path.join(cfg.datadir, cfg.name, 'graph')
astdir  = os.path.join(cfg.datadir, cfg.name, 'AST')
# END CFG

import project_crawler
import utils
import ast_transformer
import ast_processor

if cfg.preprocess:
    paths = project_crawler.crawl(path, verbose=cfg.verbose)
    all_ast_dump = []
    for idx,p in enumerate(paths):
        if cfg.verbose:
            print("[MAIN] Processing path", p)

        parsed_file = str(os.path.basename(p))
        save_file = 'AST-bin-dump-'+parsed_file

        parsed_ast = utils.parse_file(p, verbose=cfg.verbose)
        ast_dump_file = os.path.join(astdir, save_file+'.ast')
        all_ast_dump.append(ast_dump_file)
        utils.save(ast=parsed_ast, filename=ast_dump_file, format='pickle')

        ast_dump = astor.dump_tree(parsed_ast)
        ast_dump_file_txt = os.path.join(astdir, save_file+'.txt')
        utils.save(ast=ast_dump, filename=ast_dump_file_txt, format='txt')

        print("\r[MAIN]  --- Saving parsed AST for file {0}/{1} ...".format(idx+1,len(paths)), end='\r')
    print()
    print("[MAIN]  --- Saved parsed AST for {0} files in {1}.".format(len(paths), dumpdir))
    print()

else:
    all_ast_dump = project_crawler.crawl(astdir, filetype='.ast')

ast_processor.process(ast_paths=all_ast_dump, save_dir=dumpdir, verbose=cfg.verbose)
