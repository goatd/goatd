# This uses goatd_client, a python library for interacting with goatd. For more
# information, see https://github.com/goatd/python-goatd
# Run with $ python basic_behaviour.py, after goatd is running

from goatd_client import Goat

goat = Goat()

for i in range(5):
    goat.heading
    goat.wind
    goat.position
    goat.rudder(0)
    goat.rudder(-1)
    goat.rudder(3)

    goat.sail(0)
