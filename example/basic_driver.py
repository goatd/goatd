some_hardware = {}

@goatd.heading
def heading():
    return 2.43

@goatd.wind
def get_wind():
    return 8.42

@goatd.position
def position():
    return (2.343443, None)

@goatd.rudder
def rudder(theta):
    return theta

@goatd.sail
def sail(theta):
    return theta
