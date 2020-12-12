"""
Utility functions to cast the string value from environment to python types.
"""

from .utils import raise_config_error_instead


@raise_config_error_instead
def comma_separated_list(value):
    return value.split(",")


@raise_config_error_instead
def boolean(value):
    _truthy = ["true", "True", "1"]
    _false = ["false", "False", "0"]

    if value in _truthy:
        return True
    elif value in _false:
        return False
    else:
        raise ValueError('Value "{}" can not be parsed into a boolean.'.format(value))
