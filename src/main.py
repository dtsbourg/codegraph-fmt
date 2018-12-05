"""
Utility to dump an AST from a set of files.

@author: Dylan Bourgeois (@dtsbourg), Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import os
from collections import namedtuple
import astor
import argparse
import yaml
from utils import create_dir

# CFG
with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

path    = os.path.join(cfg['paths']['datadir'], cfg['paths']['name'], cfg['paths']['folder'])
dumpdir = os.path.join(cfg['paths']['datadir'], cfg['paths']['name'], 'graph'); create_dir(dumpdir)
astdir  = os.path.join(cfg['paths']['datadir'], cfg['paths']['name'], 'AST');   create_dir(astdir)
traindir = os.path.join(dumpdir, 'train');              create_dir(traindir)
testdir  = os.path.join(dumpdir, 'test');               create_dir(testdir)
valdir   = os.path.join(dumpdir, 'val');                create_dir(valdir)
# END CFG

import project_crawler
import utils
import ast_transformer
import ast_processor

if cfg['run']['preprocess']:
    paths = project_crawler.crawl(path, verbose=cfg['run']['verbose'])
    all_ast_dump = []; parse_map = {}
    for idx,p in enumerate(paths):
        if cfg['run']['verbose']:
            print("[MAIN] Processing path", p)

        save_file = 'AST-bin-dump-'+"_".join(p.split('/')[2:])

        parsed_ast = utils.parse_file(p, verbose=cfg['run']['verbose'])
        ast_dump_file = os.path.join(astdir, save_file+'.ast')
        all_ast_dump.append(ast_dump_file)
        utils.save(ast=parsed_ast, filename=ast_dump_file, format='pickle')

        parse_map[ast_dump_file] = p

        ast_dump = astor.dump_tree(parsed_ast)
        ast_dump_file_txt = os.path.join(astdir, save_file+'.txt')
        utils.save(ast=ast_dump, filename=ast_dump_file_txt, format='txt')

        print("\r[MAIN]  --- Saving parsed AST for file {0}/{1} ...".format(idx+1,len(paths)), end='\r')
    print()
    if len(paths) == 0:
        print("[ERROR] --- Found no files to process in {}".format(path))
        quit()
    print("[MAIN]  --- Saved parsed AST for {0} files in {1}.".format(len(paths), dumpdir))
    print()

    utils.save_json(parse_map, save_dir=dumpdir, filename=cfg['paths']['folder']+'-parse_map.json')

else:
    all_ast_dump = project_crawler.crawl(astdir, filetype='.ast')

ast_processor.process(ast_paths=all_ast_dump,
                      save_dir=dumpdir,
                      verbose=cfg['run']['verbose'],
                      test_ratio=1.0-cfg['experiment']['train_ratio'],
                      val_ratio=cfg['experiment']['val_ratio'],
                      prefix=cfg['paths']['folder'])
