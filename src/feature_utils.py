"""
`feature_utils.py`
-------------------

Extract different types of features based on the properties of nodes within the AST or within the graph.

@author: Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import ast_utils

class FeatureExtractor():
    def __init__(self):
        return

    def get_node_type(self, node):
        return ast_utils.get_token_id(node)
