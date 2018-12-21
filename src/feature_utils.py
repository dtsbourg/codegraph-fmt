"""
`feature_utils.py`
-------------------

Extract different types of features based on the properties of nodes within the AST or within the graph.

@author: Thao Nguyen (@thaonguyen19)

License: CC-BY 4.0
"""

import numpy as np
import ast_utils
import gensim
import re

class FeatureExtractor():
    def __init__(self):
        return

    def get_node_type(self, node):
        return ast_utils.get_token_id(node)

def load_model(model_path):
    return gensim.models.Word2Vec.load(model_path)

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]

def token2vec(token):
    MODEL_PATH = "../token2vec.model"
    model = load_model(MODEL_PATH)

    flatten = lambda l: [y for x in l for y in x]

    strtok = type(token).__name__
    if ast_utils.is_variable(token):
        strtok = ast_utils.get_varname(token)
    subtoks = flatten([camel_case_split(v) for v in strtok.split('_')])

    return np.mean([model[sk] for sk in subtoks], axis=0)
