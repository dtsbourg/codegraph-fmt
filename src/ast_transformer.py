"""
`ast_transformer.py`
-------------------

Used to manipulated parsed ASTs.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import astor
import networkx as nx


class SAGEWalker(astor.TreeWalk):
    '''
    Example subclass of an astor TreeWalker.
    '''
    def node_class_index(self, node):
        '''
        Adds the node to the indexed list.
        '''
        raise NotImplementedError

    def process_class_index(self, node):
        '''
        Adds the node's class to the indexed list.
        '''
        raise NotImplementedError

    def to_sage(self):
        '''
        Dump the indexed AST to the appropriate files.
        '''
        raise NotImplementedError
