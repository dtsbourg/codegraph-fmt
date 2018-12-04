"""
`project_crawler.py`
-------------------

Module that should process a given project and
build the index of relevant source code files.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import os

blacklist = [
    '__init__.py',
    'setup.py',
    'autogen.py',
    'conf.py',
    'config.py'
]

def crawl(path, verbose=False, filetype='.py'):
    ps = []; ignore_count = 0;
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(filetype):
                if not filename in blacklist:
                    p = os.path.join(root,filename)
                    ps.append(p)
                else:
                    ignore_count += 1
        if verbose:
            print("[CRAWL]  --- Processed {0} files in {1}".format(len(filenames), root))

    print("[CRAWL]  --- Ignored {0} blacklisted files in {1}".format(ignore_count, path))
    print()
    return ps
