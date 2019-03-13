# SAGE-fmt

The goal of this repository is to streamline the generation of graphs from Python source code. It parses provided source files to generate annotated ASTs as networkx graphs, along with custom features for nodes and edges when applicable.

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


To add a new piece of source code that should be parsed, you can add it as a submodule:

```
SAGE-fmt/data/example-tree> git submodule add https://github.com/<username>/<cloned-repo>
```

or just clone the desired repository:

```
SAGE-fmt/data/example-tree> git clone https://github.com/<username>/<cloned-repo>
```

### 2. Generating ASTs

The main interface can be configured through a `.yaml` file, which contains the following properties:

```
run:
    preprocess: True         # If flag is passed, the ASTs will be re-generated. Otherwise, the script will load pre-generated AST
    verbose: True
paths:
    datadir: "../data"       # Path to the top level data directory.
    name: "code-example"      # Identifier for the mined directory.
    folder: "raw"            # Raw code folder identifier.
    pregenpath: "AST"        # Pre-generated AST folder identifier.
experiment:
    train_ratio: 0.8         # At a file level, fraction of training samples
    val_ratio: 0.2           # At a file level, fraction of validation samples
    graph_type: "test" # Graph granularity level ("file_graph" for one graph per file, "project_graph" for one large graph)
    train_files: ['']          # Directory of files to build the training graph(s) from
    test_files: ['main']        # Directory of files to build the test graph(s) from
    dense: False
```

Many examples of configuration files are provided in the `src` directory.

The main interface then runs several consecutive actions, none of which should require much
configuration for most usecases:

1. Crawl the desired repository to collect the paths of `.py` source files.
2. Parse the files to generate a valid AST (done with [`astor`](https://astor.readthedocs.io))
3. Save the generated AST in two formats
    1. `.txt`: Pretty-printed string representation
    2. `.ast`: Pickle holding a valid `AST` Python object

### 3. Manipulating the generated ASTs

Run `main.py` that first crawls all the python files in the raw code directory, constructs an AST for each file and pass the list of ASTs to `generate_json()` function in `ast_networkx.py`, which in turn traverses each AST in DFS manner, extracts features (AST node type), converts the AST into a networkx graph and finally merges all the graphs together into one.

The `experiment` fields of the configuration file contains mosst of the possible configuration options, including the specification of particular paths for training and test graphs, the ability to densify the graphs, ...

(Optional) To profile the computation cost of the process, run the script with cProfile flag and save the output into a txt file that can later be parsed with pstats:
```
SAGE-fmt/src> python -m cProfile -o [output txt file] main.py [arguments as mentioned above]
SAGE-fmt/src> python parse_profiling_output.py > [readable output file]
```

#### The output Format

The library will produce the following files:

* `<prefix>-feats.npy` : A numpy array containing, for each node, the set of specified features. 
* `<prefix>-id_map.json` : A map of unique identifiers to nodes identifiers in the generated graph.
* `<prefix>-file_map.json` : A map of root nodes to the source code files they connect.
* `<prefix>-source_map.json` : A map of node identifiers to positions in the original source files (line and column indices).
* `<prefix>-G.json : A networkx compatible graph of the generated AST.
* `<prefix>-var_map.json` : A map of extracted variable name literals to their respective node identifiers.
* `<prefix>-func_map.json` : A map of extracted method name literals to their respective node identifiers.

