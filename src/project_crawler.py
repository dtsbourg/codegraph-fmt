"""
`project_crawler.py`
-------------------

Module that should process a given project and
build the index of relevant source code files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import os
import logging as log


blacklist = [
    '__init__.py',
    'setup.py',
    'autogen.py',
    'conf.py',
    'config.py',
    'process.py'
]

def crawl(path, filetype='.py'):
    ps = []; ignore_count = 0; total_count = 0
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(filetype):
                if not filename in blacklist:
                    p = os.path.join(root,filename)
                    ps.append(p)
                    total_count += 1
                else:
                    ignore_count += 1
        log.debug("[CRAWL]  --- Processed {0} files in {1}".format(len(filenames), root))
    log.debug("")
    log.debug("[CRAWL]  --- Done crawling ...")
    log.debug("[CRAWL]  --- Ignored {0} blacklisted files in {1}".format(ignore_count, path))
    log.debug("[CRAWL]  --- Found {0} valid files in {1}".format(total_count, path))
    log.debug("")
    return ps
