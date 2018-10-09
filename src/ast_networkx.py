import utils
import networkx as nx
import ast
import json

data_path = '/lfs/hyperion3/0/thaonguyen/SAGE-fmt/data/code-sample/AST/'
tree = utils.load(data_path + 'AST-bin-dump.ast')
all_nodes = list(ast.walk(tree)) # BFS traversal
all_nodes_set = set(all_nodes)

DG = nx.DiGraph()
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
