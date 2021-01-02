import logging
from ppctree.tree.ppc_node import PPCNode

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

class PPCNodeT(PPCNode):
    """Tree node that is a terminal.

    This is the class for a terminal that has overt material - e.g not
    a trace or some other empty category.  so end == start + 1

    #TODO: could make empty and nonempty leaves into subclass of a leaf class

    Attributes
    ==========
    pos: string
        part-of-speech tag
    word: string
        the word
    """
    def __init__(self, pos, word):
        """Make a nonempty terminal from the pos and word"""
        PPCNode.__init__(self)
        self.pos = pos
        self.terminal_string = word

    @staticmethod
    def is_nonempty_leaf():
        return True

    def mystr(self,):
        """Return a one-line string version of the node."""
        ret = f'({self.pos} {self.terminal_string})'
        return ret
