goatd - sailing goat daemon 
===========================

Experimental robotic sailing goat daemon.

[![BuildStatus](https://travis-ci.org/goatd/goatd.png?branch=master)](https://travis-ci.org/goatd/goatd)
[![CoverageStatus](https://coveralls.io/repos/goatd/goatd/badge.png?branch=master)](https://coveralls.io/r/goatd/goatd?branch=master)

General architecture
-----------

Goatd is designed to be the manager for a goat control system, granting
graceful startup, telemetry, logging and a built in simulator.

There are two main components of a system written using `goatd`:

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

    $ sudo easy_install virtualenv pip

Now setup the virtual environment and install the dependencies

    $ mkdir env
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

### System-wide on Debian

On any Debian based distribution:

    $ apt-get install python-yaml


Testing
-------

To run tests, install nose

    $ pip install nose

and run `nosetests`. If all the tests pass, the output should be similar to:

    $ nosetests 
    ..........
    ----------------------------------------------------------------------
    Ran 30 tests in 0.118s

    OK

Drivers
-------

Drivers should implement the following functions:

  * `heading`
  * `wind`
  * `position`
  * `rudder`
  * `sail`
