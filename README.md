[![Build Status](https://github.com/isik-kaplan/iubeo/actions/workflows/tests.yml/badge.svg)](https://github.com/isik-kaplan/iubeo/actions/workflows/tests.yml/badge.svg)
[![PyPI - License](https://img.shields.io/pypi/l/iubeo.svg)](https://pypi.org/project/iubeo/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/iubeo.svg)](https://pypi.org/project/iubeo/)


## What is *iubeo*?

Friendlier way to write your config.

## What is it good for?

You write how you want to read your config.

```py
from iubeo import config

def list_from_string(val):
    return val.split(',')

CONFIG = config(
    {
        'DATABASE': {
            'USER': str,
            'PASSWORD': str,
            'HOST': str,
            'PORT': str,
        },
        'ALLOWED_HOSTS': list_from_string,
    },
    # prefix = '',  # default
    # sep = '__',  # default
)
```

with the above config, environment variables like

```.env
DATABASE__USER=example
DATABASE__PASSWORD=example-password
DATABASE__HOST=localhost
DATABASE__PORT=5432
ALLOWED_HOSTS=example.com,api.example.com,www.example.com
```

are read from the environment.

```py
CONFIG.DATABASE.USER # "example-user"
CONFIG.DATABASE.PASSWORD # "example-password"
CONFIG.DATABASE.HOST # "localhost"
CONFIG.DATABASE.PORT # "5432"
CONFIG.ALLOWED_HOSTS # ["example.com", "api.example.com", "www.example.com"]
```

You can also change the separator and add a prefix to manage your environment variables better

```py
CONFIG = config({
    'SECRETS': {
        'API_KEY': str,
    },
}, prefix='APP1', sep='-')
```
which would be read from
```.env
APP1-SECRETS-API_KEY=isik_kaplan_api_key
```

Iubeo also comes with a couple of pre-configured functions to read common environment variable types:
```py
from iubeo import config, comma_separated_list, boolean

CONFIG = config({
    'DATABASE': {
        'USER': str,
        'PASSWORD': str,
        'HOST': str,
        'PORT': str,
    },
    'ALLOWED_HOSTS': comma_separated_list,
    'DEBUG': boolean,
})
```
