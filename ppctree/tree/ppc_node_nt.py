import logging
from ppctree.tree.ppc_node import PPCNode

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

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
        """Parse the label for a nonterminal node."""
        tmp = self._get_trace_or_gap_index(label)
        self.ftags = ""
        hyphen_x = tmp.find("-")
        if hyphen_x > -1:
            self.ftags = tmp[hyphen_x:]
            tmp = tmp[:hyphen_x]
        self.bare_label = tmp

    def _get_trace_or_gap_index(self, label):
        """Checks if label has gap or trace index.

        (1) only trace index
        IP-MAT-1

        (2) only gap index
        IP-MAT=2

        (3) trace and gap
        IP-MAT-1=2

        (4) gap and trace (unexpected)
        IP-MAT=2-1

        Parameters
        ==========
        label: string
            the nonterminal label
        """
        #  quick and sloppy code
        self.gap_index = None
        self.trace_index = None
        highest_hyphen = label.rfind("-")
        highest_equals = label.rfind("=")
        ret = label
        if highest_hyphen != -1 and highest_equals != -1:
            if highest_hyphen > highest_equals:
                # case 4
                print("highest_hyphen > highest_equals %s" % (label,))
                self._set_trace_index(label, highest_hyphen)
                label = label[:highest_hyphen]
                self._set_gap_index(label, highest_equals)
                print("trace_index=%s gap_index=%s" % (self.trace_index, self.gap_index))
                ret = label[:highest_equals]
            else:
                # case 3
                self._set_gap_index(label, highest_equals)
                ret = label[:highest_equals]
        elif highest_hyphen != -1:
            if self._set_trace_index(label, highest_hyphen):
                # case 1
                ret = label[:highest_hyphen]
            else:
                # just function tags, no indices
                ret = label
        elif highest_equals != -1:
            # case 2
            self._set_gap_index(label, highest_equals)
            ret = label[:highest_equals]
        return ret

    def _set_trace_index(self, label, index_hyphen):
        """Check if string after hyphen is int and if so sets trace index.

        Parameters
        ==========
        label: string
            the full nonterminal label
        index_hyphen: int
            index of -

        Returns
        =======
        boolean: True if trace_index was set.
        """
        if self._is_int(label[index_hyphen+1:]):
            self.trace_index = int(label[index_hyphen+1:])
            return True
        return False

    def _set_gap_index(self, label, index_equals):
        """Sets gap index.

        Unlike with what comes after a hyphen, which could be a trace
        index or ftag string, this has to be an integer.

        Parameters
        ==========
        label: string
            the full nonterminal label
        index_equals: int
            index of =
        """
        if self._is_int(label[index_equals+1:]):
            self.gap_index = int(label[index_equals+1:])
        else:
            print("unexpected label2 %s %s " % (label, index_equals))
            #sys.exit(-1)

    @staticmethod
    def _is_int(text):
        """Just checks if text is integer."""
        try:
            _ = int(text)
            return True
        except ValueError:
            return False

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
