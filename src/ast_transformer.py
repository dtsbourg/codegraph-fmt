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
        self.prev_line_no = 0
        self.prev_col_offset = 0

    def generic_visit(self, node):
        '''
        Is called upon visit to every node.
        '''
        if isinstance(node, ast.Name):
            if type(node.ctx) is not ast.Load:
                node.varname = node.id

        if not hasattr(node, 'lineno'):
            node.lineno = -1
        self.prev_line_no = node.lineno

        if not hasattr(node, 'col_offset'):
            node.col_offset = -1
        self.prev_col_offset = node.col_offset

        if not hasattr(node, 'visited'):
            self.nodes_stack.append(node)

            token_id = ast_utils.get_token_id(node)
            if token_id == -1:
                print("[WARNING] --- Found unkown token", node)

            self.feature_list.append(token_id)

            node.visited = True

        ast.NodeVisitor.generic_visit(self, node)
