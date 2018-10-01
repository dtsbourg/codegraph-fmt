# SAGE-fmt

The goal of this repository is to streamline the generation of graphs compatible with the [GraphSAGE](https://github.com/williamleif/GraphSAGE) [1] learning framework, in particular in the case of source code graphs.

## The GraphSAGE Format

> TODO

* `xxx-class_map.json`
* `xxx-feats.npy`
* `xxx-G.json`
* `xxx-id_map.json`

## Usage

### AST Extractor

> Dylan

```
import ast

ast.dump("print("Hello World!"))
```

Some pre-generated ASTs are provided as tests for the pipeline in the `data/AST` repository.

### Graph Generator

> Thao

## References

[1]: _Inductive Representation Learning on Large Graphs_, by William L. Hamilton, Rex Ying, Jure Leskovec [link](https://arxiv.org/abs/1706.02216)
