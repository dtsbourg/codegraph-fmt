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

def generate_json(all_ast_paths, save_dir, verbose): #all_ast_path is a list of asts constructed from each file crawled
    print("[AST_NX] Converting ast to json files...")
    
    # Initialise tree and maps
    all_top_nodes = []
    node_count = 0
    last_full_graph_node_count = 0
    G = nx.Graph()
    id_map_dict = {}
    ast_id_mapping = {}
    
    features_array = []
    for ast_path in all_ast_paths:
        tree = utils.load(ast_path)

        visitor = ASTVisitor(verbose)
        visitor.visit(tree)
        print("[AST_NX] Visited ", ast_path, " found ", len(visitor.nodes_stack), " nodes")
        features_array.extend(visitor.feature_list)

        all_top_nodes.append(node_count)
        for node in visitor.nodes_stack:
            G.add_node(node_count)
            node.graph_id = node_count
            id_map_dict[node_count] = node_count
            for child in ast.iter_child_nodes(node):
                G.add_edge(node_count, last_full_graph_node_count + visitor.nodes_stack.index(child)) # child may be lower down the stack
            node_count += 1
        last_full_graph_node_count = node_count
 
    if len(all_ast_paths) > 1: # add virtual root node
        G.add(node_count)
        features_array.append(-1)
        for top_node in all_top_nodes:
            G.add_edge(node_count, top_node)
        node_count += 1

    print("[AST_NX] Found ", node_count, " nodes in total")
    
    features_array = np.array(features_array)
    # one hot conversion
    n_types = np.max(features_array) + 1 - np.min(features_array)
    n_nodes = node_count
    features_one_hot = np.zeros((n_nodes, n_types))
    features_one_hot[np.arange(n_nodes), features_array] = 1
    #if len(all_ast_paths) > 1: # update feature vector for last node (virtual root) to be all 0's
    #    features_one_hot[-1, -1] = 0

    # write to files
    np.save(os.path.join(save_dir, 'feats.npy'), features_one_hot)
    with open(os.path.join(save_dir, 'id_map.json'), 'w') as fout:
        fout.write(json.dumps(id_map_dict))
    with open(os.path.join(save_dir, 'G.json'), 'w') as fout:
        fout.write(json.dumps(nx.json_graph.node_link_data(G)))

if __name__ == '__main__': #test
    generate_json('../data/code-sample/AST/AST-bin-dump.ast', '../data/code-sample/AST/')
