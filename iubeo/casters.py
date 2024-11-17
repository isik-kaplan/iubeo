"""
Utility functions to cast the string value from environment to python types.
"""

from functools import wraps


def caster(f):
    sentinel = object()

    def wrapper(missing_default=sentinel, error_default=sentinel):
        @wraps(f)
        def function_clone(value):
            return f(value)

        if missing_default is not sentinel:
            function_clone.missing_default = missing_default
        if error_default is not sentinel:
            function_clone.error_default = error_default
        return function_clone

    return wrapper


@caster
def comma_separated_list(value):
    return value.split(",")


@caster
def comma_separated_int_list(value):
    return [int(i) for i in value.split(",")]


@caster
def comma_separated_float_list(value):
    return [float(i) for i in value.split(",")]


@caster
def boolean(value):
    _truthy = ["true", "True", "1"]
    _false = ["false", "False", "0"]

    if value in _truthy:
        return True
    elif value in _false:
        return False
    else:
        raise ValueError('Value "{}" can not be parsed into a boolean.'.format(value))


string = caster(str)
integer = caster(int)
