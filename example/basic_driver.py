some_hardware = {}

@goatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount * 2

@goatd.heading
def heading():
    return 2.43

@goatd.wind
def get_wind():
    return 0.42
