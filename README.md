goatd - sailing goat daemon 
===========================

Experimental robotic sailing goat daemon.

[![BuildStatus](https://travis-ci.org/goatd/goatd.png?branch=master)](https://travis-ci.org/goatd/goatd)
[![CoverageStatus](https://coveralls.io/repos/goatd/goatd/badge.png?branch=master)](https://coveralls.io/r/goatd/goatd?branch=master)

General architecture
-----------

Goatd is designed to be the manager for a goat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using goatd:

  - the __driver__ interfaces with the particular set of hardware in the goat.

  - the __behaviour__ performs a set of actions to make the goat do a
    particular task. The API available for these scripts is supposed to be
    declarative, with the idea that for any goat with a driver written, any
    behavour script will work.

```
           goatd
             |
        -----------
       |           |
     driver     behaviour
       |
  goat hardware
```

Installing dependencies
-----------------------

Goatd is tested on Python 2.7, 3.2 and 3.3.

### Locally with virtualenv

Install virtualenv and pip

```bash
$ sudo easy_install virtualenv pip
```

Now setup the virtual environment and install the dependencies

```bash
$ mkdir env
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### System-wide on Debian

On any Debian based distribution:

```bash
$ apt-get install python-yaml
```


Testing
-------

To run tests, install nose

```bash
$ pip install nose
```

and run `nosetests`. If all the tests pass, the output should be similar to:

```bash
$ nosetests 
..........
----------------------------------------------------------------------
Ran 30 tests in 0.118s

OK
```

The current test results from the head of the `master` branch can be found
[here](https://travis-ci.org/goatd/goatd).

Drivers
-------

### Driver basics

Goatd drivers are implemented as a simple python module. When a behaviour
script requires information about the current state of the goat or needs to
send a command to some hardware, goatd runs one of the functions in the driver.

Drivers should implement the following basic functions:

  - `heading()` - Return the heading of the goat in degrees, relative to the
    world.
  - `wind()` - Return the direction the wind is blowing, relative to the world.
  - `position()` - Return a tuple containing the current latitude and longitude
    of the goat, in that order.
  - `rudder(angle)` - Set the goat's rudder to `angle`  degrees relative to the
    goat.
  - `sail(angle)` - Similarly to `rudder`, set the sail to `angle` degrees
    relative to the goat.

These functions can have any name, but are marked for use and registered with
goatd using decorators.

Example, only implementing `heading`:

```python
import goatd
driver = goatd.Driver()

@driver.heading
def get_heading():
    return some_compass.bearing()
```

### Custom handlers

If the behaviour script needs to run some other function in the driver, a
handler can be registered using `driver.handler(name)`

For example:

```python
@driver.handler('pony')
def example_handler():
    return something
```

This can then be used as any other function in a behaviour client.
