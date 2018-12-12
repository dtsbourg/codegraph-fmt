"""
`ast_processor.py`
-------------------

Processing ASTs. This module can generate networkx compatible graphs from this.

@author: Thao Nguyen (@thaonguyen19), Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

import utils
import networkx as nx
import ast
import json
import os
import numpy as np
import itertools

from ast_transformer import ASTVisitor
from ast_utils import AST_SYMBOL_DICT, should_filter, is_func

def process(ast_paths, save_dir, verbose, test_ratio, val_ratio, prefix, dense):
    '''
    Run the processor from within the module to avoid persistance of ASTProcessor object.
    '''
    processor = ASTProcessor(ast_paths=ast_paths, save_dir=save_dir, verbose=verbose, test_ratio=test_ratio, val_ratio=val_ratio, prefix=prefix, dense=dense)
    processor.process()

class ASTProcessor(object):
    '''
    ASTProcessor class. This is the main abstraction with which passes on the AST are done.
    It also provides an interface to dump the processed AST to networkx-compatible graphs.
    '''
    def __init__(self, ast_paths, save_dir, verbose, test_ratio, val_ratio, prefix, dense):
        '''
        Args:
            ast_paths : List of paths to pre-processed ASTs (.ast/pickle format by default)
            save_dir  : Path to save output of AST processing
            test_ratio: Proportion of nodes reserved for testing in the entire graph
            val_ratio: Proportion of nodes reserved for validation in the entire graph
            verbose   : Verbose flag
            prefix    : Prefix appended to file when saved
            dense     : If true, add edges between children
        '''
        # Config
        self.ast_paths  = ast_paths
        self.verbose    = verbose
        self.test_ratio = test_ratio
        self.val_ratio  = val_ratio
        self.save_dir   = save_dir; utils.create_dir(save_dir)
        self.prefix     = prefix
        self.one_hot_features = True
        self.dense      = dense
        # Global
        self.top_nodes  = []            # List of the root nodes corresponding to each of the ASTs
        self.G          = nx.Graph()
        self.id_map     = {}            # Maps node ids to their index in the feature array
        self.features   = []            # Feature array
        self.classes    = []
        self.source_map = {}            # Graph node id to tuple of (top_node, line number, col offset) for inverse lookup
        self.file_map   = {}            # Mapping root node ids to corresponding files
        self.var_map    = {}            # Mapping node ids to variable names, if applicable
        self.func_map   = {}            # Mapping node ids to function names, if applicable

        self.node_count = 0
        self.ast_count  = len(self.ast_paths)
        self.add_root_node = self.ast_count > 1


    def process(self):
        '''Run the AST processing pipeline as follows:

        For each AST files:
            For each node
                Build the node features
            Build the equivalent networkx graph
        Add a virtual root node
        Output to .json
        '''
        last_full_graph_node_count = 0

        for idx, ast_path in enumerate(self.ast_paths):
            print("\r[AST]  --- Processing AST for file {0}/{1} ...".format(idx+1,len(self.ast_paths)), end='\r')

            ast = utils.load(ast_path)
            visitor = self.process_ast(ast)

            self.features.extend(visitor.feature_list)
            self.classes.extend(visitor.classes_list)

            top_node = self.process_nodes(visitor, last_full_graph_node_count)
            self.process_top_nodes(top_node, ast_path)

            last_full_graph_node_count = self.node_count

        print()

        self.add_virtual_root_node()
        self.generate_json()

    def process_top_nodes(self, node_id, path):
        '''Map the top_level node_ids to files'''

        self.top_nodes.append(node_id)
        self.file_map[node_id] = path


    def process_nodes(self, visitor, last_full_graph_node_count):
        '''Process the visited nodes to build the graph
        Args:
            visitor : populated AST visitor (contains the stack of visited nodes)
            last_full_graph_node_count : node id of the last full AST (corr. to one file) added to the graph
        '''
        top_node = self.node_count
        for i, node in enumerate(visitor.nodes_stack):
            if not should_filter(node):
                # Split train / test / val
                val, train = False, True
                rand = np.random.rand(1)[0]
                if rand < self.test_ratio:
                    train = False
                elif rand > 1-self.val_ratio:
                    val = True

                # Add nodes to networkx graph
                self.G.add_node(self.node_count, attr_dict={'train': train, 'test': not train, 'val': val})
                node.graph_id = self.node_count # This is never used???

                # Populate feature maps
                self.id_map[self.node_count] = self.node_count
                self.source_map[self.node_count] = (top_node, node.lineno, node.col_offset)

                # Retrieve variable names
                if hasattr(node, 'varname'):
                    self.var_map[self.node_count] = node.varname

                # Retrieve function names
                if is_func(node):
                    self.func_map[self.node_count] = node.name

                children = []
                for child in ast.iter_child_nodes(node):
                    if not should_filter(child):
                        child_index = visitor.nodes_stack.index(child)
                        children.append(child_index)
                        self.G.add_edge(self.node_count, last_full_graph_node_count + child_index) # child may be lower down the stack
                if self.dense:
                    for src, tgt in itertools.combinations(children, 2):
                        self.G.add_edge(last_full_graph_node_count+src, last_full_graph_node_count+tgt)

            self.node_count +=  1
        return top_node

    def process_ast(self, ast):
        '''Process an entire AST.
        Args:
            ast : an ast object

        Returns:
            visitor : an ASTVisitor object which contains the stack of visited nodes
        '''
        visitor = ASTVisitor(self.verbose)
        visitor.visit(ast) # <-- This could probably be optimized to loop just once with process_nodes

        return visitor

    def add_virtual_root_node(self):
        '''
        When dealing with multiple files we collate them by adding a virtual root node.
        '''
        if self.add_root_node:
            self.G.add_node(self.node_count, attr_dict={'train': True, 'test': False, 'val': False, 'feature': 0})
            self.id_map[self.node_count] = self.node_count
            self.features.append(0)
            self.classes.append(13)

            for top_node in self.top_nodes:
                self.G.add_edge(self.node_count, top_node)
            self.node_count += 1

    def generate_json(self):
        '''
        Dumps the processed AST to several files containing all the meta information

        1. feats.npy        --> a numpy array cointaining all the node features.
        2. id_map.json      --> a map of node identifiers.
        3. file_map.json    --> a map from root nodes to filenames.
        4. source_map.json  --> a map of AST token identifiers to positions in the source code.
        5. G.json           --> a networkx compatible graph representation of the AST.
        6. class_map.json   --> a map of node_id to class.
        7. var_map.json     --> a map of node_id to variable names (when applicable).
        8. var_map.json     --> a map of node_id to function names (when applicable).
        '''
        # 1. Save features
        if self.one_hot_features:
            features = utils.one_hot_encoder(self.features, self.node_count, min=0,max=max(AST_SYMBOL_DICT.values()))
        else:
            features = np.array(self.features).reshape(-1, 1)

        feature_path = os.path.join(self.save_dir, self.prefix+'-feats.npy')
        np.save(feature_path, features)

        print()
        print("[AST]  --- Saved features to", feature_path)

        # 2. Save node identifiers
        utils.save_json(self.id_map, save_dir=self.save_dir, filename=self.prefix+'-id_map.json')
        # 3. Save File map
        utils.save_json(self.file_map, save_dir=self.save_dir, filename=self.prefix+'-file_map.json')
        # 4. Save Source map
        utils.save_json(self.source_map, save_dir=self.save_dir, filename=self.prefix+'-source_map.json')
        # 5. Save Graph
        graph = nx.json_graph.node_link_data(self.G)
        utils.save_json(graph, save_dir=self.save_dir, filename=self.prefix+'-G.json')
        # 6. Save class
        class_map = {i: c for i,c in enumerate(self.classes)}
        utils.save_json(class_map, save_dir=self.save_dir, filename=self.prefix+'-class_map.json')
        # 7. Save variable names
        utils.save_json(self.var_map, save_dir=self.save_dir, filename=self.prefix+'-var_map.json')
        # 8. Save function names
        utils.save_json(self.func_map, save_dir=self.save_dir, filename=self.prefix+'-func_map.json')
