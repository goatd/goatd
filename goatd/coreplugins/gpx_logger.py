from goatd import BasePlugin

import datetime
import time

gpx_trkpt_format = (
             '\t\t\t<trkpt '
             'lat="{lat}" '
             'lon="{long}">'
             
             '<time>{datetime}</time>'
             
             '<cmt>Rudder:{rudder} Sail:{sail} Wind:{wind_direction} Heading:{heading}</cmt>'
             
             '</trkpt>'
             '\n'
             )
             
gpx_wpt_format = (
             '\t\t<wpt '
             'lat="{lat}" '
             'lon="{long}">'
             '</wpt>'
             '\n'
             )

class GPXLoggerPlugin(BasePlugin):
    def main(self):
        self.period = self.config.period
        self.filename = self.config.filename + time.strftime("_%d-%m-%yT%H,%M,%SZ.gpx")
        
        self.startfile()
        
        self.trackpoints()
        
        self.waypoints()
            
        self.endfile()
            
    def startfile(self):
        
        with open(self.filename, 'a') as f:
                f.write('<?xml version="1.0"?> \n'
    '<gpx creator="goatd" xmlns="http://www.topografix.com/GPX/1/1"'
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation='
    '"http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
                f.write("\t<name>Goatd Output Track</name>\n")
                
    def trackpoints(self):
        with open(self.filename, 'a') as f:
            f.write("\t<trk>\n\t\t<trkseg> \n")
        
            while self.running:
                goat_heading = self.goatd.goat.heading()
                goat_wind_direction = self.goatd.goat.wind_absolute()
                goat_lat, goat_lon = self.goatd.goat.position()
                goat_sail = self.goatd.goat.get_sail()
                goat_rudder = self.goatd.goat.get_rudder()
                goat_datetime = datetime.datetime.now().isoformat()

                log_line = gpx_trkpt_format.format(
                        lat=goat_lat,
                        long=goat_lon,
                        datetime=goat_datetime,
                        rudder=goat_rudder,
                        sail=goat_sail,
                        wind_direction=goat_wind_direction,
                        heading=goat_heading,
                )

                f.write(log_line)

                time.sleep(self.period)
            
            f.write("\t\t</trkseg>\n\t</trk>\n")
            
    def waypoints(self):
        with open(self.filename, 'a') as f:
            for mark in self.goatd.waypoint_manager.waypoints:
                mark_lat, mark_long = mark
            
                point_line = gpx_wpt_format.format(
                    lat=mark_lat,
                    long=mark_long,
                )
            
                f.write(point_line)
    
    def endfile(self):
        with open(self.filename, 'a') as f:
                f.write("</gpx>")

plugin = GPXLoggerPlugin
