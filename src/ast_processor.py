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

def process(ast_paths, save_dir, verbose):
    '''
    Run the processor from within the module to avoid persistance of ASTProcessor object.
    '''
    processor = ASTProcessor(ast_paths=ast_paths, save_dir=save_dir, verbose=verbose)
    processor.process()

class ASTProcessor(object):
    '''
    ASTProcessor class. This is the main abstraction with which passes on the AST are done.
    It also provides an interface to dump the processed AST to networkx-compatible graphs.
    '''
    def __init__(self, ast_paths, save_dir, verbose):
        '''
        Args:
            ast_paths : List of paths to pre-processed ASTs (.ast/pickle format by default)
            save_dir  : Path to save output of AST processing.
            verbose   : Verbose flag.
        '''
        # Config
        self.ast_paths = ast_paths
        self.verbose = verbose
        self.save_dir = save_dir
        # Global ## TODO: Document these variables @Thao
        self.top_nodes = []
        self.G = nx.Graph()
        self.id_map = {}
        self.ast_id_map = {}
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
            last_full_graph_node_count : @Thao TODO document
        '''
        top_node = self.node_count
        for node in visitor.nodes_stack:
            self.G.add_node(self.node_count)
            # TODO add train / test features
            node.graph_id = self.node_count # This is never used???

            self.id_map[self.node_count] = self.node_count
            self.source_map[self.node_count] = (top_node, node.lineno, node.col_offset)

            for child in ast.iter_child_nodes(node):
                child_index = visitor.nodes_stack.index(child)
                self.G.add_edge(self.node_count, last_full_graph_node_count + child_index) # child may be lower down the stack

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
            self.G.add_node(self.node_count)
            self.features.append(-1)

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
        '''
        # 1. Save features
        features_one_hot = utils.one_hot_encoder(self.features, self.node_count)

        feature_path = os.path.join(self.save_dir, 'feats.npy')
        np.save(feature_path, features_one_hot)

        print()
        print("[AST]  --- Saved features to", feature_path)

        # 2. Save node identifiers
        utils.save_json(self.id_map, save_dir=self.save_dir, filename='id_map.json')
        # 3. Save File map
        utils.save_json(self.file_map, save_dir=self.save_dir, filename='file_map.json')
        # 4. Save Source map
        utils.save_json(self.source_map, save_dir=self.save_dir, filename='source_map.json')
        # 5. Save Graph
        graph = nx.json_graph.node_link_data(self.G)
        utils.save_json(graph, save_dir=self.save_dir, filename='G.json')
