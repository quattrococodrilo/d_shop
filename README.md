# Fly: Django taking flight

This project encapsulates my experience with Django. I have found working with
Docker to be incredibly beneficial, and to streamline its usage, I have created
a tool that allows for easy management of services. This tool is ./fly.py. In
addition to this utility, I have included factories, a debugging class, mixins,
and applications that I find useful.

## Install

`fly.py` is the command line tool for the project.

To install Clone this repo and:

`./fly.py build`
`./fly.py up`

## Fly Manager

Fly is inspired in Laravel Sail, so, with this app manager you can:

- `install`: Install app.
- `build`: Build services.
- `up`: Up services.
- `down`: Down services.
- `d`: Execute docker compose commands.
- `pip`: Execute pip commands.
- `manage`: Execute Django Manager.
- `npm`: Execute npm.
- `mysql`: Execute MySql.
- `psql`: Execute PostgreSQL.
- `runserve-alone`: Run Django server alone.
- `-h, --help`: show this help message and exit.

## Django commands

### Create New App

When create a new a app with `./fly.py manage startapp {app_name}`, the app will be created in apps directory.

### Seeder

To create a seeder, execute:

```bash

./fly manage make_seeder {app_name}


```

With this command you can seed your database.

```bash

./fly manage seed --seeder={app_name}.{seeder_function_name}


```

Example Factory:

```python

import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = "core.User"

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


```

Example Seeder:

```python

from .factories.user_factory import UserFactory


def user_seeder():
    UserFactory.create_batch(10)

```

Execute seeder:

```bash

./fly manage seed --seeder=core.user_seeder


```

## Fly Mixins

These mixins are part of the `core.models.mixins` module.

### DateTimeTrackMixin

Mixin to automatically track the creation and last modification times of an object.

```python
from core.models.mixins import DateTimeTrackMixin

class MyModel(models.Model, DateTimeTrackMixin):
    # Your fields here
```

#### Fields

- `created_at`: Creation date and time (automatically set on creation).
- `updated_at`: Last modification date and time (automatically updated on each save).

### SoftDeleteMixin

Mixin to provide soft delete functionality. Soft deleted objects are not removed
from the database but are flagged as deleted.

```python
from core.models.mixins import SoftDeleteMixin

class MyModel(models.Model, SoftDeleteMixin):
    # Your fields here
```

#### Fields

- `deleted_at`: Soft deletion date and time (null if the object is not deleted).

#### Managers

- `objects`: Manager to retrieve objects that have not been soft deleted.
- `deleted_objects`: Manager to retrieve objects that have been soft deleted.
- `all_objects`: Default Django manager.

#### Methods

- `delete(force=False)`: Soft delete the object by setting the `deleted_at`
  field to the current time. If `force=True`, the object will be permanently
  removed from the database.

  Example:

  ```python
  my_object.delete()  # Soft delete
  my_object.delete(force=True)  # Permanent delete
  ```

- `restore()`: Restore a soft deleted object by setting the `deleted_at` field
  to None.

  Example:

  ```python
  my_object.restore()  # Restore soft deleted object
  ```

### Additional Managers

- `DeletedManager`: Manager to retrieve objects that have been soft deleted.
- `ActiveManager`: Manager to retrieve objects that have not been soft deleted.

This documentation describes the classes and methods and provides examples of
how to use them in your Django models. You can copy and paste this content into
your `README.md` file or your project's documentation.

## Custom Configuration and Global Debugging Functions

### Configuration Directory Structure

Unlike a standard Django project, this implementation places all base configuration
files, which would normally be in the directory named after the project, into the
`config` directory.

### Debugging Configuration (`config.settings.py`)

When `DEBUG` is set to `True`, the following code snippet can be used to set up
global debugging functions and configure Django Debug Toolbar for Docker:

```python
if DEBUG:
    from core.utils.globals import SET_GLOBALS
    import socket

    SET_GLOBALS()

    # django-debug-toolbar docker
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
```

### Global Debugging Functions (`core.utils.globals.py`)

This module contains global functions that can be injected into Python's
builtins, allowing them to be used globally without needing to import them.

#### `SET_GLOBALS()`

Injects custom functions into Python's builtins.

```python
from core.utils.globals import SET_GLOBALS

SET_GLOBALS()
```

#### `FlyDebugGlobals` Class

Contains static methods for global debugging.

- `pdb()`: A global function to quickly enter Python's debugger (pdb).

  Example:

  ```python
  FLY.pdb().set_trace()
  ```

- `printer(*args, title="DEBUG")`: A global print function that prints a debug
header and footer around the arguments.

  Example:

  ```python
  FLY.printer("Value1", "Value2", title="My Debug Info")
  ```

  This will print the values with a header and footer, and an optional title for
  the debug section. The default color for the header and footer is cyan, but it
  can be customized.

### Note

Make sure to install the `colorama` package if you want to use colored output in
the `printer` function.

## TODO

1. [ ] Better documentation for **fly** manager.
2. [ ] Add project structure.
3. [ ] Add exec command.
