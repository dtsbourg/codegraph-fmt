"""
`ast_networkx.py`
-------------------

Transforming ASTs into networkx graphs.

@author: Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import utils
import networkx as nx
import ast
import json
import os
import numpy as np
from ast_transformer import ASTVisitor
from feature_utils import FeatureExtractor

def generate_json(all_ast_paths, save_dir): #all_ast_path is a list of asts constructed from each file crawled
    print("[AST_NETWORKX] Converting ast to json files...")
    all_top_nodes = []
    node_count = 0
    G = nx.Graph()
    id_map_dict = {}
    ast_id_mapping = {}
    extractor = FeatureExtractor()
    features_array = []
    for ast_path in all_ast_paths:
        tree = utils.load(ast_path)

        visitor = ASTVisitor()
        visitor.visit(tree)
        print(ast_path, len(visitor.nodes_stack))

        all_top_nodes.append(node_count)
        for node in visitor.nodes_stack:
            G.add_node(node_count)
            node.graph_id = node_count
            features_array.append(extractor.get_node_type(node))
            id_map_dict[node_count] = node_count
            for child in ast.iter_child_nodes(node):
                G.add_edge(i, visitor.nodes_stack.index(child))###TODO
            node_count += 1
    '''
    features_array = np.vstack(features_array)
    # one hot conversion
    n_types = np.max(features_array) + 1
    n_nodes = len(visitor.nodes_stack)
    features_one_hot = np.zeros((n_nodes, n_types))
    features_one_hot[np.arange(n_nodes), features_array.squeeze()] = 1
    np.save(os.path.join(save_dir, 'feats.npy'), features_one_hot)
    '''
    with open(os.path.join(save_dir, 'id_map.json'), 'w') as fout:
        fout.write(json.dumps(id_map_dict))
    with open(os.path.join(save_dir, 'G.json'), 'w') as fout:
        fout.write(json.dumps(nx.json_graph.node_link_data(G)))

if __name__ == '__main__': #test
    generate_json('../data/code-sample/AST/AST-bin-dump.ast', '../data/code-sample/AST/')
