# Phrase Structure Tree manipulation

This package consists of code for phrase structrue tree manipulation. It is intended to be used with
[github/skulick/ppcprep](https://github.com/skulick/ppcprep.git).

## Installation

This is not yet on PyPi, but can be installed in the standard way, such as

```git clone https://github.com/skulick/ppctree.git```

and then running `pip install .`

## Usage

An example:
```
from ppctree.tree.ppc_tree import PPCTree
x = "(S (NP (NN john)) (VP (V fell)))"
tree = PPCTree(x)
print(tree.mystr())
```

will output 

```(S (NP (NN john)) (VP (V fell)))```

