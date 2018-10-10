"""
`ast_networkx.py`
-------------------

Transforming ASTs into networkx graphs.

@author: Thao Nguyen (@thaonguen19)

License: CC-BY 4.0
"""

import utils
import networkx as nx
import ast
import json

# TODO pass as arguments from main.py
data_path = '../data/code-sample/AST/'
ast_path = data_path + 'AST-bin-dump.ast'

def generate_json(ast_path):
    # TODO: Docstring + logging
    tree = utils.load(ast_path)
    # TODO: use a visitor instead of walk + persistent set
    all_nodes = list(ast.walk(tree)) # BFS traversal
    all_nodes_set = set(all_nodes)

    DG = nx.DiGraph() # No need for directed graph
    id_map_dict = {}
    ast_id_mapping = {}
    curr_id = 0
    for node in all_nodes_set:
        DG.add_node(curr_id)
        ast_id_mapping[node] = curr_id
        id_map_dict[str(curr_id)] = curr_id
        curr_id += 1

    for node in all_nodes_set:
        for child in ast.iter_child_nodes(node):
            #DG.add_node(child)
            DG.add_edge(ast_id_mapping[node], ast_id_mapping[child])

    #n_nodes = len(list(DG.nodes))
    with open(data_path + 'id_map.json', 'w') as fout:
        fout.write(json.dumps(id_map_dict))
    with open(data_path + 'G.json', 'w') as fout:
        fout.write(json.dumps(nx.json_graph.node_link_data(DG)))
