"""
`ast_utils.py`
-------------------

Utility for AST processing in Python.

@author: Dylan Bourgeois (@dtsbourg)

License: CC-BY 4.0
"""

# Build a list of possible AST nodes for Python 3.7
from _ast import *
import sys

MOD_SYMBOLS = [Module, Interactive, Expression, Suite]
STMT_SYMBOLS = [FunctionDef, AsyncFunctionDef, ClassDef, Return, Delete, \
                Assign, AugAssign, For, AsyncFor, While, If, With, AsyncWith, \
                Raise, Try, Assert, Import, ImportFrom, Global, Nonlocal, \
                Expr, Pass, Break, Continue]
EXPR_SYMBOLS = [BoolOp, BinOp, UnaryOp, Lambda, IfExp, Dict, Set, ListComp, \
                SetComp, DictComp, GeneratorExp, Await, Yield, YieldFrom, \
                Compare, Call, Num, Str, FormattedValue, JoinedStr, Bytes, \
                NameConstant, Ellipsis, Constant, Attribute, Subscript, \
                Starred, Name, List, Tuple]
EXPR_CONTENT_SYMBOLS = [Load, Store, Del, AugLoad, AugStore, Param]
SLICE_SYMBOLS = [Slice, ExtSlice, Index]
BOOLOP_SYMBOLS = [And, Or]
OPERATOR_SYMBOLS = [Add, Sub, Mult, MatMult, Div, Mod, Pow, LShift, RShift, \
                    BitOr, BitXor, BitAnd, FloorDiv]
UNARYOP_SYMBOLS = [Invert, Not, UAdd, USub]
CMPOP_SYMBOLS = [Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn]
COMPREHENSION_SYMBOLS = [comprehension]
EXCEPT_SYMBOLS = [excepthandler, ExceptHandler]
ARG_SYMBOLS = [arguments, arg, keyword]
IMPORT_SYMBOLS = [alias, withitem]
PYTHON_SYMBOLS = MOD_SYMBOLS + STMT_SYMBOLS + EXPR_SYMBOLS \
               + EXPR_CONTENT_SYMBOLS + SLICE_SYMBOLS \
               + BOOLOP_SYMBOLS + OPERATOR_SYMBOLS \
               + UNARYOP_SYMBOLS + CMPOP_SYMBOLS \
               + EXCEPT_SYMBOLS + ARG_SYMBOLS + IMPORT_SYMBOLS \
               + COMPREHENSION_SYMBOLS
AST_SYMBOL_DICT = dict((v, k) for (k, v) in enumerate(PYTHON_SYMBOLS))

# End token list
# It's pretty ugly, feel free to edit for more elegance ...

def get_token_class_id(node):
    assert(sys.version_info >= (3,7))
    t = type(node)
    if t in MOD_SYMBOLS: return 0
    if t in STMT_SYMBOLS: return 1
    if t in EXPR_SYMBOLS: return 2
    if t in EXPR_CONTENT_SYMBOLS: return 3
    if t in SLICE_SYMBOLS: return 4
    if t in BOOLOP_SYMBOLS: return 5
    if t in OPERATOR_SYMBOLS: return 6
    if t in UNARYOP_SYMBOLS: return 7
    if t in CMPOP_SYMBOLS: return 8
    if t in ARG_SYMBOLS: return 9
    if t in EXCEPT_SYMBOLS: return 10
    if t in COMPREHENSION_SYMBOLS: return 11
    if t in IMPORT_SYMBOLS: return 12
    else: return 13

def get_token_id(node):
    t = type(node)
    return AST_SYMBOL_DICT.get(t, -1)

def should_filter(node):
    t = type(node)
    return t in EXPR_CONTENT_SYMBOLS
