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
from ast_transformer import ASTVisitor

def generate_json(ast_path, save_dir):
    print("[AST_NETWORKX] Converting ast to json files...")
    tree = utils.load(ast_path)
    for node in ast.walk(tree):
        node.visited = False

    G = nx.Graph() 
    id_map_dict = {}
    ast_id_mapping = {}

    visitor = ASTVisitor()
    visitor.visit(tree)
    print(len(visitor.nodes_stack))
    for i, node in enumerate(visitor.nodes_stack):
        G.add_node(i)
        id_map_dict[i] = i
        for child in ast.iter_child_nodes(node):
            G.add_edge(i, visitor.nodes_stack.index(child))
    print(id_map_dict)
    with open(os.path.join(save_dir, 'id_map.json'), 'w') as fout:
        fout.write(json.dumps(id_map_dict))
    with open(os.path.join(save_dir, 'G.json'), 'w') as fout:
        fout.write(json.dumps(nx.json_graph.node_link_data(G)))

if __name__ == '__main__': #test
    generate_json('../data/code-sample/AST/AST-bin-dump.ast', '../data/code-sample/AST/')
