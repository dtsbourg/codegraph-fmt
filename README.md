# SAGE-fmt

The goal of this repository is to streamline the generation of graphs compatible with the [GraphSAGE](https://github.com/williamleif/GraphSAGE) [1] learning framework, in particular in the case of source code graphs.

## Usage

The interface should be run through `main.py`.

### 1. Choosing a project to run on

The data to be processed is being stored in the the aptly named `data` path.

#### Running existing examples

Existing code samples are saved as [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
As such, they only exist as links when the repository is cloned, but can be pulled by running:

```
SAGE-fmt> git submodule init
SAGE-fmt> git submodule update
```

#### Adding new code

The default structure of a new example is as follows:

```
.
└── example-tree
    ├── AST
    ├── cloned-repo
    └── graph
```

where:

* `example-tree` is the root of your new example (should be in the `data` folder).
    * `AST`: where the generated ASTs will live.
    * `cloned-repo`: where the raw code will live (see below for how to get the code).
    * `graph`: where the generated GraphSAGE-compatible files will live.   

> The library is actually more flexible than it seems (all of this is configurable but
shared structure will help the iteration speed :))

To add a new piece of source code that should be parsed, you can use the following method:

```
SAGE-fmt/data/example-tree> git submodule add https://github.com/<username>/<cloned-repo>
```

> Don't forget to update the configuration in `main.py` to run on this new path!

### 2. Generating ASTs

The main interface can be configured through the `cfg` object. One can set the
following properties:

* `cfg.datapath`: The path to the data folder - the default value should work.
* `cfg.name`: The name of the repository to work on (the example repo is [`keras`](https://github.com/keras-team/keras))
* `cfg.verbose`: How much logging should be displayed.

The main interface then runs several consecutive actions, none of which should require much
action for now:

1. Crawl the desired repository to collect the paths of `.py` source files.
2. Parse the files to generate a valid AST (done with [`astor`](https://astor.readthedocs.io))
3. Save the generated AST in two formats
    1. `.txt`: Pretty-printed string representation
    2. `.ast`: Pickle holding a valid `AST` Python object

### 3. Manipulating the generated ASTs

> TODO: This will be done in the `ast_transformer.py` module.
>       `astor` should provide the required methods for traversing the AST.
>       This module should just do some bookkeeping on top of this.
>       The output should be GraphSAGE compatible `.json` representations
>       of the source code graph.

#### The GraphSAGE Format

> TODO: Document the format more thoroughly.

* `xxx-class_map.json`
* `xxx-feats.npy`
* `xxx-G.json`
* `xxx-id_map.json`

## References

[1]: _Inductive Representation Learning on Large Graphs_, by William L. Hamilton, Rex Ying, Jure Leskovec [link](https://arxiv.org/abs/1706.02216)
