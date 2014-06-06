import goatd

def test_hdm():
    assert goatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'

def test_degrees_to_nmea():
    assert goatd.nmea.degrees_to_nmea(45.555) == '4533.3'

def test_negative_degrees_to_nmea():
    assert goatd.nmea.degrees_to_nmea(-45.555) == '-4533.3'

'''def test_gll():
    print goatd.nmea.gll(38.063413, 122.240910, None)
    assert False'''
