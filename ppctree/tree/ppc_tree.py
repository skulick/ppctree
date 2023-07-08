import re
import sys
from ppctree.tree.ppc_node_nt import PPCNodeNt
from ppctree.tree.ppc_node_t import PPCNodeT
from ppctree.tree.ppc_node_empty_t import PPCNodeEmptyT

class PPCTree():
    """Stores a tree structure.

    The class used to represent each node defaults to PPCNode,
    which is the appropriate one to use for the ppc work.

    Attributes
    ==========
    root: PPCNode
        root of the tree
    all_leaf_nodes: list of PPCNode
        all leaves
    nonempty_leaf_nodes: list of PPCNode
        the leaves that are not empty
    """
    def __init__(self, line, assign_spans=True, term_class=PPCNodeT):
        """Initialize a tree structure from string or existing structure.

        Parameters
        ----------
        line : str
            A string representation of the phrase structure tree. For example,
            when converting from the existing .psd files, the tree string
            with CODE, etc. removed will be passed into here.
        """
        self.root = self.parse_treestr(line, term_class)

        self.nonempty_leaf_nodes = []
        self.all_leaf_nodes = []
        self.root.recurse_looking_for_leaves(self.nonempty_leaf_nodes, self.all_leaf_nodes)
        if assign_spans:
            self._assign_spans()

    @staticmethod
    def parse_treestr(line, term_class):
        """Convert string to a phrase structure tree.

        Parameters
        ----------
        line : str
            tree string to be parsed.
        Returns
        -------
        PPNode
            The root of the tree.
        """
        line = re.sub(r"\(", r" ( ", line)
        line = re.sub(r"\)", " ) ", line)
        line = re.sub(r" +", " ", line)
        line = re.sub(r" $", "", line)
        line = line.strip()
        parts = line.split(" ")

        stack = []
        for token in parts:
            if token != ")":
                # ( or str
                stack.append(token)
            else:
                cons = []
                popped_token = stack.pop()
                while popped_token != "(":
                    cons.append(popped_token)
                    popped_token = stack.pop()
                # each member of cons is a string (not parens) or a PPCNode
                # parent is a string
                parent_str = cons.pop()
                cons.reverse()

                if (len(cons) == 1 and
                    isinstance(cons[0], str)):
                    pos = parent_str
                    text = cons[0]
                    if pos == '-NONE-':
                        parent = PPCNodeEmptyT(pos, text)
                    else:
                        parent = term_class(pos, text)
                else:
                    parent = PPCNodeNt(parent_str)
                    parent.set_children(cons)

                stack.append(parent)
        root = stack.pop()
        return root

    def _assign_spans(self,):
        """Assign spans to all leaves and nontermimals.

        Start from 1 since we want to reserve 0 for a dummy root node later.
        First assign word_nuxsm, start, and end to leaves and then recurse
        down.
        """
        current_word_num = 1
        for one in self.all_leaf_nodes:
            # includes empty leafs and anchor
            if one.is_nonempty_leaf():
                #one.start = one.word_num
                #one.end = one.word_num+1
                #current_word_num = one.word_num+1
                one.start = current_word_num
                one.end = current_word_num + 1
                current_word_num += 1
            elif one.is_empty_leaf():
                one.start = current_word_num
                one.end = current_word_num
            else:
                print("impossible")
                sys.exit(-1)
        self.root.assign_spans()

    def mystr(self,):
        """Return a one-line string version of the node and its children"""
        return self.root.mystr()
