import goatd

some_hardware = object()

@goatd.do_hardware
def do_hardware(amount):
    some_hardware.something = amount
    return amount
