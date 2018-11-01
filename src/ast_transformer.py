"""
`ast_transformer.py`
-------------------

Used to manipulated parsed ASTs.

@author: Dylan Bourgeois (@dtsbourg), Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import astor
import networkx as nx
import ast
import ast_utils

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


class ASTVisitor(ast.NodeVisitor):
    '''
    Example subclass of a visitor.
    '''
    def __init__(self, verbose):
        super().__init__()
        self.verbose = verbose
        self.nodes_stack = []
        self.feature_list = []

    def generic_visit(self, node):
        '''
        Is called upon visit to every node.
        '''
        if not hasattr(node, 'visited'):
            self.nodes_stack.append(node)
            self.feature_list.append(ast_utils.get_token_id(node))
            node.visited = True
        ast.NodeVisitor.generic_visit(self, node)
