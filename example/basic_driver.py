some_hardware = {}

@goatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount * 2
