from functools import wraps

from .exceptions import ConfigError


def raise_config_error_instead(f):
    if hasattr(f, "_raises_config_error") and f._raises_config_error:
        # This means that we already have decorated previously, so shortcut and don't re-decorate it.
        # Avoiding nested ConfigErrors
        return f

    @wraps(f)
    def wrapper(value):
        try:
            return f(value)
        except Exception as e:
            raise ConfigError("Error while parsing value with {}".format(f.__name__)) from e

    wrapper._raises_config_error = True
    return wrapper
