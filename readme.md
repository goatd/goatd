goatd - sailing goat daemon
===========================

Experimental robotic sailing goat daemon.

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

Dependencies
------------

With pip:

    $ pip install -r requirements.txt

Debian based systems:

    $ apt-get install python-yaml


Todo
----

  - ~~Behaviour loading~~
  - Driver loading
  - Core goatd function decorators
  - Logging
  - Event system
  - API
  - Halisim driver
  - Other language support
  - init system integration
  - Remote behaviour loading
