import time

for i in range(5):
    goat.heading()
    goat.get_wind()
    goat.position()
    goat.rudder(0)
    goat.rudder(-1)
    goat.rudder(3)

    goat.sail(0)
