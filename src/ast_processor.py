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
    processor = ASTProcessor(ast_paths=ast_paths, save_dir=save_dir, verbose=verbose)
    processor.process()

class ASTProcessor():
    def __init__(self, ast_paths, verbose, save_dir):
        # Config
        self.ast_paths = ast_paths
        self.verbose = verbose
        self.save_dir = save_dir
        # Global
        self.top_nodes = []
        self.G = nx.Graph()
        self.id_map = {}
        self.ast_id_map = {}
        self.features = []

        self.node_count = 0
        self.ast_count = len(self.ast_paths)
        self.add_root_node = self.ast_count > 1


    def process(self):
        last_full_graph_node_count = 0

        for idx, ast_path in enumerate(self.ast_paths):
            print("\r[AST]  --- Processing AST for file {0}/{1} ...".format(idx+1,len(self.ast_paths)), end='\r')

            ast = utils.load(ast_path)
            visitor = self.process_ast(ast)

            self.features.extend(visitor.feature_list)
            self.top_nodes.append(self.node_count)

            self.process_nodes(visitor, last_full_graph_node_count)

            last_full_graph_node_count = self.node_count

        print()

        self.add_virtual_root_node()
        self.generate_json()


    def process_nodes(self, visitor, last_full_graph_node_count):
        for node in visitor.nodes_stack:
            current_node_count = self.node_count

            self.G.add_node(current_node_count)
            node.graph_id = current_node_count
            self.id_map[self.node_count] = current_node_count

            for child in ast.iter_child_nodes(node):
                child_index = visitor.nodes_stack.index(child)
                self.G.add_edge(current_node_count, last_full_graph_node_count + child_index) # child may be lower down the stack

            self.node_count = current_node_count + 1

    def process_ast(self, ast):
        visitor = ASTVisitor(self.verbose)
        visitor.visit(ast)

        return visitor

    def add_virtual_root_node(self):
        if self.add_root_node:
            self.G.add_node(self.node_count)
            self.features.append(-1)

            for top_node in self.top_nodes:
                self.G.add_edge(self.node_count, top_node)
            self.node_count += 1

    def generate_json(self):
        features_one_hot = utils.one_hot_encoder(self.features, self.node_count)

        feature_path = os.path.join(self.save_dir, 'feats.npy')
        np.save(feature_path, features_one_hot)
        print("[AST]  --- Saved features to", feature_path)

        with open(os.path.join(self.save_dir, 'id_map.json'), 'w') as fout:
            fout.write(json.dumps(self.id_map))
            print("[AST]  --- Saved identifier map to", fout.name)

        with open(os.path.join(self.save_dir, 'G.json'), 'w') as fout:
            fout.write(json.dumps(nx.json_graph.node_link_data(self.G)))
            print("[AST]  --- Saved graph to", fout.name)
