goatd - sailing goat daemon
===========================

Experimental robotic sailing goat daemon.

Terminology
-----------

  - `Behaviour` - performs a set of actions to make the goat do a particular task
  - `Driver` - causes hardware to do interesting things based on actions

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

    $ sudo apt-get install python-yaml


Todo
----

  - Behaviour loading
  - Driver loading
  - Core goatd function decorators
  - Logging
  - Event system
  - API
  - Halisim driver
  - Other language support
  - init system integration
  - Remote behaviour loading
