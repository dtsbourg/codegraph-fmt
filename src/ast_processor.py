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

from ast_transformer import ASTVisitor

def process(ast_paths, save_dir, verbose, test_ratio):
    '''
    Run the processor from within the module to avoid persistance of ASTProcessor object.
    '''
    processor = ASTProcessor(ast_paths=ast_paths, save_dir=save_dir, verbose=verbose, test_ratio=test_ratio)
    processor.process()

class ASTProcessor(object):
    '''
    ASTProcessor class. This is the main abstraction with which passes on the AST are done.
    It also provides an interface to dump the processed AST to networkx-compatible graphs.
    '''
    def __init__(self, ast_paths, save_dir, verbose, test_ratio):
        '''
        Args:
            ast_paths : List of paths to pre-processed ASTs (.ast/pickle format by default)
            save_dir  : Path to save output of AST processing
            test_ratio: Proportion of nodes reserved for testing in the entire graph
            verbose   : Verbose flag
            top_nodes : list of the root nodes corresponding to each of the ASTs
            G         : the output networkx undirected graph
            id_map    : dict used to output id_map.json
            features  : list of features obtained from each node in order during traversal
            source_map: dict mapping graph node id to tuple of (line number, col offset) for inverse lookup
            file_map  : dict mapping root node ids to corresponding files
        '''
        # Config
        self.ast_paths = ast_paths
        self.verbose = verbose
        self.test_ratio = test_ratio
        self.save_dir = save_dir
        # Global
        self.top_nodes = []
        self.G = nx.Graph()
        self.id_map = {}
        self.features = []
        self.source_map = {}
        self.file_map = {}

        self.node_count = 0
        self.ast_count = len(self.ast_paths)
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

            self.process_nodes(visitor, last_full_graph_node_count)
            self.process_top_nodes(self.node_count, ast_path)

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
        for i, node in enumerate(visitor.nodes_stack):
            current_node_count = self.node_count
            if np.random.rand(1)[0] < self.test_ratio:
                train = False
            else:
                train = True
            self.G.add_node(current_node_count, attr_dict={'train': train, 'test': not train, 'val': False, 'feature': visitor.feature_list[i]}) #TODO: convert it to one-hot?
            node.graph_id = current_node_count # This is never used???

            self.id_map[current_node_count] = current_node_count
            self.source_map[current_node_count] = (node.lineno, node.col_offset)

            for child in ast.iter_child_nodes(node):
                child_index = visitor.nodes_stack.index(child)
                self.G.add_edge(current_node_count, last_full_graph_node_count + child_index) # child may be lower down the stack

            self.node_count = current_node_count + 1

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
            self.G.add_node(self.node_count, attr_dict={'train': True, 'test': False, 'val': False, 'feature': -1})
            self.features.append(-1)

            for top_node in self.top_nodes:
                self.G.add_edge(self.node_count, top_node)
            self.node_count += 1

    def generate_json(self):
        '''
        Dumps the processed AST to several files containing all the meta information

        1. feats.npy   --> a numpy array cointaining all the node features.
        2. id_map.json --> a map of node identifiers.
        3. G.json      --> a networkx compatible graph.
        '''
        features_one_hot = utils.one_hot_encoder(self.features, self.node_count)

        feature_path = os.path.join(self.save_dir, 'feats.npy')
        np.save(feature_path, features_one_hot)

        print()
        print("[AST]  --- Saved features to", feature_path)

        with open(os.path.join(self.save_dir, 'id_map.json'), 'w') as fout:
            fout.write(json.dumps(self.id_map))
            print("[AST]  --- Saved identifier map to", fout.name)

        with open(os.path.join(self.save_dir, 'file_map.json'), 'w') as fout:
            fout.write(json.dumps(self.file_map))
            print("[AST]  --- Saved file map to", fout.name)

        with open(os.path.join(self.save_dir, 'source_map.json'), 'w') as fout:
            fout.write(json.dumps(self.source_map))
            print("[AST]  --- Saved source map to", fout.name)
        with open(os.path.join(self.save_dir, 'G.json'), 'w') as fout:
            fout.write(json.dumps(nx.json_graph.node_link_data(self.G)))
            print("[AST]  --- Saved networkx graph to", fout.name)
