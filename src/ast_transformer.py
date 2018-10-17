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
    def __init__(self):
        super().__init__()
        self.nodes_stack = []

    def generic_visit(self, node):
        '''
        Is called upon visit to every node.
        '''
        if not node.visited:
            self.nodes_stack.append(node)
            node.visited = True
            print(type(node), ast_utils.get_token_id(node), ast_utils.get_token_class_id(node))
        ast.NodeVisitor.generic_visit(self, node)
