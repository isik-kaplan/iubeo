import copy
import os

from .exceptions import ConfigError


class Config(dict):
    _START_NODE_NAME = "iubeo_data"

    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    @classmethod
    def _fix_end_node_name(cls, name, sep):
        # Removes sep+_START_NODE_NAME+sep from the end node name.
        return name.replace(sep + cls._START_NODE_NAME, "").lstrip(sep)

    @staticmethod
    def _cast_value(data, key, caster, environment_key):
        try:
            data[key] = caster(os.environ[environment_key])
        except KeyError:
            default = getattr(caster, "missing_default", None)
            if default:
                data[key] = default
            else:
                raise ConfigError(
                    f"Environment variable {environment_key} not found."
                    f" Please set it or provide a `missing_default` to your caster."
                )
        except Exception as e:
            default = getattr(caster, "error_default", None)
            if default:
                data[key] = default
            else:
                raise ConfigError(
                    f"Error while parsing {environment_key}='{os.environ[environment_key]}' with '{caster}'."
                    " Please check the value and the caster or provide an `error_default` to your caster."
                ) from e

    @classmethod
    def _create(cls, data: dict, prefix: str = "", sep: str = "__"):
        prefix = prefix or ""
        mutated = {}
        for key, value in data.items():
            mutated = {}
            if isinstance(value, dict):
                mutated = {prefix + sep + key: cls._create(value, prefix + sep + key, sep)}
            elif callable(value):
                cls._cast_value(data, key, value, cls._fix_end_node_name(prefix + sep + key, sep))

            else:
                raise ConfigError(f"Values either must be callables or other mappings, not {type(value)}. Key={key}.")
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


def config(data, *, prefix: str | None = None, sep: str = "__"):
    return Config.create(data, prefix, sep)
