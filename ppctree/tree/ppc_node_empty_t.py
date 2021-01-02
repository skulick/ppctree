import logging
from ppctree.tree.ppc_node import PPCNode


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

class PPCNodeEmptyT(PPCNode):
    """Tree node that is an empty terminal.

    This is the class for a terminal that has an empty "word" - e.g.
    -NONE- or some other empty category. So end == start
    """
    def __init__(self, pos, word):
        """Make a nonempty terminal from the pos and word"""
        PPCNode.__init__(self)
        self.pos = pos
        self.terminal_string = word

    @staticmethod
    def is_empty_leaf():
        return True

    def mystr(self,):
        """Return a one-line string version of the node."""
        ret = f'({self.pos} {self.terminal_string})'
        return ret
