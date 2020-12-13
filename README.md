[![Build Status](https://travis-ci.com/isik-kaplan/iubeo.svg?branch=master)](https://travis-ci.com/isik-kaplan/iubeo)
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

CONFIG = config({
    'DATABASE': {
        'USER': str,
        'PASSWORD': str,
        'HOST': str,
        'PORT': str,
    },
    'ALLOWED_HOSTS': list_from_string,
})
```

It creates the environment variable names for you, and reads them from the environment, casting it to the final nodes.

Now your can just chain the attributes, and if it is the last node on the above dictionary, you get the environment
variable casted to given callable.

```.env
DATABASE__USER=isik-kaplan
DATABASE__PASSWORD=isik-kaplan-db-password
DATABASE__HOST=localhost
DATABASE__PORT=5432
ALLOWED__HOSTS=isik-kaplan.com,api.isik-kaplan.com,www.isik-kaplan.com
```

are read from the environment, and are casted when you access the attribute.

```py
CONFIG.DATABASE.USER # "isik-kaplan"
CONFIG.DATABASE.PASSWORD # "isik-kaplan-db-password"
CONFIG.DATABASE.HOST # "localhost"
CONFIG.DATABASE.PORT # "5432"
CONFIG.ALLOWED_HOSTS # ["isik-kaplan.com", "api.isik-kaplan.com", "www.isik-kaplan.com"]
```

Iubeo also comes with couple of pre-configured functions to read common environment variable types:
```py
from iubeo import config, comma_separated_list, boolean

CONFIG = config({
    'DATABASE': {
        'USER': str,
        'PASSWORD': str,
        'HOST': str,
        'PORT: str,
    },
    'ALLOWED_HOSTS': comma_separated_list,
    'DEBUG': boolean,
})
```
