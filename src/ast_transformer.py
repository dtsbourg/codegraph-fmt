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
from ast_utils import AST_SYMBOL_DICT
import feature_utils
import utils
import numpy as np

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
    def __init__(self, verbose, slot):
        super().__init__()
        self.verbose         = verbose
        self.nodes_stack     = []
        self.feature_list    = []
        self.classes_list    = []
        self.prev_line_no    = 0
        self.prev_col_offset = 0
        self.slot            = slot

    def collect_metadata(self,node):
        if ast_utils.is_func_def(node):
            node.func_name = ast_utils.get_func_name(node)

        if ast_utils.is_variable(node):
            node.var_name = ast_utils.get_varname(node)

        if not hasattr(node, 'lineno'):
            node.lineno = -1
        self.prev_line_no = node.lineno

        if not hasattr(node, 'col_offset'):
            node.col_offset = -1
        self.prev_col_offset = node.col_offset

    def generic_visit(self, node):
        '''
        Is called upon visit to every node.
        '''
        if not hasattr(node, 'visited'):
            if not ast_utils.should_filter(node):
                self.collect_metadata(node)
                self.nodes_stack.append(node)

                token_id = ast_utils.get_token_id(node)
                if token_id == -1:
                    print("[WARNING] --- Found unkown token", node)

                ft = feature_utils.token2vec(node, slot=self.slot)
                one_hot_token_type = utils.one_hot_encoder(token_id, 1, min=0, max=max(AST_SYMBOL_DICT.values()))

                if np.count_nonzero(np.isnan(ft)) > 0:
                    print("[WARNING] Found nan feature for node", node)
                    ft = np.zeros(64)
                self.feature_list.append(np.concatenate([ft, one_hot_token_type[0]]))
                self.classes_list.append(ast_utils.get_token_class_id(node))
                node.visited = True

        ast.NodeVisitor.generic_visit(self, node)
