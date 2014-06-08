import datetime

import goatd

def test_hdm():
    assert goatd.nmea.hdm(49.6) == '$HDM,49.6,M*19'

def test_degrees_to_nmea():
    assert goatd.nmea.degrees_to_nmea(45.555) == '4533.3'

def test_negative_degrees_to_nmea():
    assert goatd.nmea.degrees_to_nmea(-45.555) == '-4533.3'

def test_gll():
    date = datetime.datetime(2014, 6, 7, 22, 22, 01, 152642)
    assert goatd.nmea.gll(38.063413, -122.240910, date) == \
        '$GLL,383.8,N,12214.5,W,222201.15,A*35'
