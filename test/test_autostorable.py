from noodles import (schedule, run_process, Storable, gather,
                     base_registry, Registry)
from noodles.serialisation.registry import Serialiser
import sys


class A(object):
    def __init__(self, a):
        self.a = a

    @classmethod
    def from_dict(cls, a):
        return cls(a)

    def as_dict(self):
        return {'a': self.a}


class B(Storable):
    def __init__(self):
        super(B, self).__init__()


@schedule
def g(a):
    return A(a)


@schedule
def f(a):
    b = B()
    b.b = A(a.a * 5)
    return b


@schedule
def h(b):
    return b.b.a + 7


def test_autostorable():
    a = g(7)
    b = f(a)
    c = h(b)
    d = gather(c, a)

    result = run_process(d, n_processes=1)
    assert result[0] == 42
    assert result[1].a == 7


