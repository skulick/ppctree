import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

class PPCNode(ABC):
    """Abstract class for tree node

    One of the three functions is_nonterminal, is_empty_leaf, is_nonempty_leaf
    needs to be overridden to return True. Of course this could also be done
    with a node type Enum, or by checking the class of the object.

    Attributes
    ==========
    parent: PPCNodeNt or None
        The root node has a parent == None
    child_num: int or None
        which child this is of the parent's children
    start: int
        start span of the node
    end: int
        end span of this node.
        If node is empty leaf, (start, end) == (x, x)
        If node is nonempty leaf, (start, end) == (x, x+1)
        and nonterminals build on that.  This won't wort with two
        consecutive empty leaves.
    """

    def __init__(self):
        self.parent = None
        self.child_num = None
        self.start = None
        self.end = None

    @staticmethod
    def is_nonterminal():
        """Return true iff this node is a nonterminal"""
        return False

    @staticmethod
    def is_nonempty_leaf():
        """Return true iff this node is a nonempty leaf"""
        return False

    @staticmethod
    def is_empty_leaf():
        """Return true iff this node is an empty leaf"""
        return False

    def is_empty(self):
        """Return true iff this node has no overt material"""
        return self.start == self.end

    @abstractmethod
    def mystr(self):
        """Return a one-line string version of the node and its children"""
        raise NotImplementedError
