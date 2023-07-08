import logging
import re
from ppctree.tree.ppc_node import PPCNode

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

# bare label can have $ at end, like PRO$
# also allow for _NT at end which gets added on
RE_LABEL_TRACE = re.compile(r'^(?P<bare>[A-Z_]+\$?)(?P<ftags>(-[A-Z]+)+)*(-(?P<trace>[0-9]+))*$')
RE_LABEL_GAP = re.compile(r'^(?P<bare>[A-Z_]+\$?)(?P<ftags>(-[A-Z]+)+)*(=(?P<gap>[0-9]+))*$')

class PPCNodeNt(PPCNode):
    """Tree node that is a nonterminal.

    The nonterminal label is passed in and it is parsed into the bare label,
    function tags, trace index, and gap index.

    #TODO:  The function tag handling could be better

    Attributes
    ==========
    bare_label: string
       label without function tags or indices
    ftags: string
       string of function tags, including hyphens, taken from nonterminal label
    trace_index: int or None
        trace index, taken from nonterminal label
    gap_index: int or None
         gap index, taken from nonterminal label
    children: list of PPCNode
         children, can be any of the subclasses
    """

    def __init__(self, label):
        """Make a new nonterminal node given the label.

        Parameters
        ==========
        label: string
            the nonterminal string - e.g. NP-SBJ-3=2
        """
        PPCNode.__init__(self)
        self.bare_label = None
        self.ftags = None
        self.trace_index = None
        self.gap_index = None
        self.children = []
        self.parse_label(label)

    def set_children(self, kids):
        """ Attaches children to this node.

        Parameters
        ----------
        kids : list of PPCNode
        """
        for (num, kid) in enumerate(kids):
            kid.parent = self
            kid.child_num = num
        self.children = kids

    @staticmethod
    def is_nonterminal():
        return True

    def mystr(self,):
        """Return a one-line string version of the node and its children"""
        lbl = self._assemble_full_label({"show_gaptrace":True})
        lst = ([lbl] +
               [child.mystr() for child in self.children])
        ret = '(' + ' '.join(lst) + ')'
        return ret

    def parse_label(self, label):
        """Parse label into bare_label, ftags, trace/gap"""
        # special case
        if label in ('.', '._NT'):
            logger.debug('period label')
            self.bare_label = label
            self.ftags = ''
            self.trace_index = None
            self.gap_index = None
            return

        mtch = RE_LABEL_TRACE.search(label) or RE_LABEL_GAP.search(label)
        assert mtch is not None, \
            f'unable to parse {label}'
        mdict = mtch.groupdict()

        self.bare_label = mdict['bare']

        self.ftags = mdict['ftags']
        if self.ftags is None:
            self.ftags = ''

        tmp = mdict.get('trace', None)
        self.trace_index = None if tmp is None else int(tmp)

        tmp = mdict.get('gap', None)
        self.gap_index = None if tmp is None else int(tmp)

    def _assemble_full_label(self, options):
        """Put together components of nonterminal label"""
        ret = self.bare_label + self.ftags
        if options.get("show_gaptrace", False):
            if self.gap_index is not None:
                ret += "="+str(self.gap_index)
            if self.trace_index is not None:
                ret += "-"+str(self.trace_index)
        return ret

    def assign_spans(self):
        """Set span for this node and children.

        Assumes that start, end already done for leaves
        """
        for child in self.children:
            if child.is_nonterminal():
                child.assign_spans()
        self.start = self.children[0].start
        self.end = self.children[-1].end

    def recurse_looking_for_leaves(self, nonempty_leaf_nodes, all_leaf_nodes):
        """Go through tree keeping track of leaves

        Parameters
        ==========
        nonempty_leaf_nodes: list of PPCNode
            list that gets appended to
        all_leaf_nodes: list of PPCNode
            list that gets appended to
        """
        for child in self.children:
            if child.is_empty_leaf():
                all_leaf_nodes.append(child)
            elif child.is_nonempty_leaf():
                all_leaf_nodes.append(child)
                nonempty_leaf_nodes.append(child)
            else:
                child.recurse_looking_for_leaves(nonempty_leaf_nodes, all_leaf_nodes)
