"""
`project_crawler.py`
-------------------

Module that should process a given project and
build the index of relevant source code files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import os

def crawl(path, verbose=False, filetype='.py'):
    ps = [];
    for root, directories, filenames in os.walk(path):
        if verbose: print("[CRAWL]", os.path.join(root))
        for filename in filenames:
            if filename.endswith(filetype):
                p = os.path.join(root,filename)
                ps.append(p)
        print("[CRAWL]  --- Processed {0} files in {1}".format(len(filenames), root))
    print()
    return ps
