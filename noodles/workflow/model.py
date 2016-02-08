from collections import namedtuple
from ..utility import unwrap
from .arguments import (bind_arguments, get_arguments, ref_argument,
                        serialize_arguments, Empty)


NodeData = namedtuple(
    'NodeData',
    ['function', 'arguments', 'hints'])


class FunctionNode:
    """Captures a function call as a combination of function and arguments.
    Some of these arguments may be set to :py:obj:`Empty`, these need to be
    filled in by the workflow before the function can be applied.

    .. py:attribute:: foo

    The function (or object) that is being called.

    .. py:attribute:: bound_args

    A :py:class:`BoundArguments` object storing the arguments to
    the function.
    """
    @staticmethod
    def from_node_data(data):
        foo = unwrap(data.function)
        bound_args = bind_arguments(foo, data.arguments)
        return FunctionNode(foo, bound_args, data.hints)

    def __init__(self, foo, bound_args, hints):
        self.foo = foo
        self.bound_args = bound_args
        self.hints = hints

    @property
    def data(self):
        """Convert to a :py:class:`NodeData` for subsequent serial."""
        return NodeData(self.foo, get_arguments(self.bound_args), self.hints)


class Workflow:
    """
    The workflow data container.

    .. py:attribute:: root

        A reference to the root node in the graph.

    .. py:attribute:: nodes

        A `dict` listing the nodes in the graph. We use a `dict` only to have
        a persistent object reference.

    .. py:attribute:: links

        A `dict` giving a `set` of links from each node.
    """
    def __init__(self, root, nodes, links):
        self.root = root
        self.nodes = nodes
        self.links = links

    def __iter__(self):
        return iter((self.root, self.nodes, self.links))

    @property
    def root_node(self):
        return self.nodes[self.root]


def is_workflow(x):
    return isinstance(x, Workflow) or ('_workflow' in dir(x))


def get_workflow(x):
    if isinstance(x, Workflow):
        return x

    if '_workflow' in dir(x):
        return x._workflow

    return None


def is_node_ready(node):
    """Returns True if none of the argument holders contain any `Empty` object.
    """
    return all(ref_argument(node.bound_args, a) is not Empty
               for a in serialize_arguments(node.bound_args))
