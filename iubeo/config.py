import copy
import os
from typing import AnyStr, Callable, Dict, Optional, Tuple, Union

from .exceptions import ConfigError
from .utils import raise_config_error_instead

ConfigFormat = Dict[AnyStr, Union["ConfigFormat", Tuple[AnyStr, Callable]]]


class Config(dict):
    __setattr__ = dict.__setitem__

    def __getattr__(self, item):
        value = dict.__getitem__(self, item)
        if isinstance(value, list):
            var, cast = value
            return raise_config_error_instead(cast)(os.environ.get(var))
        return value

    _START_NODE_NAME = "iubeo_data"

    @classmethod
    def _fix_end_node_name(cls, name, sep):
        # Removes sep+_START_NODE_NAME+sep from the end node name.
        return name.replace(sep + cls._START_NODE_NAME, "").lstrip(sep)

    @classmethod
    def _create(cls, data: dict, prefix: str = "", sep: str = "__"):
        prefix = prefix or ""
        for key, value in data.items():
            mutated = {}
            if isinstance(value, dict):
                mutated = {prefix + sep + key: cls._create(value, prefix + sep + key, sep)}
            elif callable(value):
                data[key] = [cls._fix_end_node_name(prefix + sep + key, sep), value]
            else:
                raise ConfigError("Values either must be callables or other mappings, not {}.".format(value))
        return cls(**mutated, **data)

    @classmethod
    def from_data(cls, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = cls.from_data(value)
        return cls(**data)

    @classmethod
    def create(cls, data: dict, prefix: str = "", sep: str = "__"):
        # We are tweaking the initial data here because we don't want the last node to be inside our final result
        # I actually consider what's above function does as a buggy behaviour, but wrapping it up in this is way easier.
        # TODO fix the _create method and merge it with this method
        data = {cls._START_NODE_NAME: data}
        # We are giving it a single root node, data; then reading it so that there is no leftover `mutated` in
        # the resulting object. This function itself introduces new bugs like having to strip the start node name
        # from the produced end node names, such as prefix__data__N0__N00, where we would want to remove the __data
        # We are currently removing it in yet another function _fix_end_node_name
        data = copy.deepcopy(data)
        # The _create method mutates the mappings it gets, actually it depends on the mutability of the objects
        # Which has, well, a side effect of mutating the object for the end user, hence: deepcopy.
        return cls.from_data(cls._create(data, prefix, sep).get(cls._START_NODE_NAME))

    @classmethod
    def _final_nodes(cls, data: ConfigFormat):
        for key, value in data.items():
            if isinstance(value, list):
                yield value[0]
            elif isinstance(value, dict):
                yield from cls._final_nodes(value)

    @property
    def final_nodes(self):
        return [*self._final_nodes(self)]


def config(data, *, prefix: Optional[str] = None, sep: str = "__"):
    return Config.create(data, prefix, sep)
