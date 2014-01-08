some_hardware = {}

@goatd.do_something
def do_hardware(amount):
    some_hardware['something'] = amount
    return amount

print(do_hardware(4))
