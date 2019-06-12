'''
Main
'''

import os
import sys
import logging as log 

import astor

import config
import project_crawler
import utils

def main(_):
    paths = project_crawler.crawl(cfg.path) 
    for idx,p in enumerate(paths):
        log.debug("[MAIN] Processing path %s" % p)
       
        parsed_ast = utils.parse_file(p, verbose=cfg.verbose)
        if idx == 0:
            for jdx, ast_subset in enumerate(parsed_ast.body):
                ast_dump = astor.dump_tree(ast_subset)
                print(jdx, ast_dump)
                save_file = 'AST-bin-dump-'+"_".join(p.split('/')[2:])+'_'+str(jdx)
                ast_dump_file_txt = os.path.join(cfg.astdir, save_file+'.txt')
                utils.save(ast=ast_dump, filename=ast_dump_file_txt, format='txt')


if __name__ == '__main__':
  env = sys.argv[1] if len(sys.argv) > 2 else 'dev'
  cfg = config.init(env=env) 
  log.basicConfig(level=log.DEBUG)
  main(cfg)
