"""
A base class for making objects serializable to JSON.
"""

from copy import deepcopy
from noodles.interface.decorator import PromisedObject, schedule


def storable(obj):
    return isinstance(obj, Storable)


def copy_if_normal(obj, memo):
    if isinstance(obj, PromisedObject):
        return obj
    else:
        return deepcopy(obj, memo)


def from_dict(cls, **kwargs):
    obj = cls.from_dict(**kwargs)
    return obj


class StorableTraits:
    def __init__(self, ref, files):
        self.ref = ref
        self.files = files if files else []


class Storable:
    def __init__(self, ref=False, files=None):
        """Storable constructor

        :param ref:
            if this is True, the Storable is loaded as a
            :py:class:`StorableRef`, only to be restored when the data is
            really needed. This should be set to True for any object that
            carries a lot of data; the default is False.
        :type ref: bool

        :param files:
            the list of filenames that this object uses for
            storage. The property Storable.files is used by Noodles to copy
            relevant data if this object is needed on another host.
        :type files: [str]
        """
        self._storable = StorableTraits(ref, files)

    @property
    def files(self):
        """List of files that this object saves to."""
        return self._storable.files

    def as_dict(self):
        """Converts the object to a `dict` containing the members
        of the object by name.

        The default implementation is just
        ::

            def as_dict(self):
                return self.__dict__

        In most cases, this method is overloaded to provide a more
        advanced method of serializing data, possibly saving data to
        an external file. In this case the corresponding filename needs
        to be appended to `self.files`.
        """
        d = dict(self.__dict__)
        return d

    @classmethod
    def from_dict(cls, **kwargs):
        """Gets a dictionary by `**kwargs`, and restores the original
        object. For any object `obj` of type `cls` that is derived from
        `Storable`, the following should  be true:
        ::

            cls.from_dict(**obj.as_dict()) == obj

        """
        obj = cls.__new__(cls)
        obj.__dict__ = kwargs
        return obj

    def __deepcopy__(self, memo):
        cls = self.__class__
        tmp = {k: copy_if_normal(v, memo) for k, v in self.as_dict().items()}

        if any(isinstance(x, PromisedObject) for x in tmp.values()):
            return schedule(from_dict)(cls, **tmp)
        else:
            return cls.from_dict(**tmp)

