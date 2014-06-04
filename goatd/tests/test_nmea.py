import goatd

def test_hdm():
    assert goatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'
