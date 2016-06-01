import serial
import time

from goatd import BasePlugin
import goatd.coreplugins.mavlink_common as mv


class MavlinkPlugin(BasePlugin):

    def send_heartbeat(self):
        self.ml.heartbeat_send(
            mv.MAV_TYPE_SURFACE_GOAT,
            mv.MAV_AUTOPILOT_GENERIC,
            mv.MAV_MODE_FLAG_GUIDED_ENABLED,
            0,
            mv.MAV_STATE_ACTIVE,
            3
        )

    def send_position(self, lat, lon):
        self.ml.global_position_int_send(
            int(time.time()),
            int(lat * 1e7),
            int(lon * 1e7),
            25000,
            25000,
            1,1,1,180*100)

        self.ml.gps_raw_int_send(
            int(time.time()*100),
            3,
            int(lat * 1e7),
            int(lon * 1e7),
            25000,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            0xFFFF,
            5
        )

    def send_heading(self, heading):
        heading = heading % 360
        if heading > 180:
            heading = heading - 360

        self.ml.vfr_hud_send(
            0,  # airspeed
            10,  # groundspeed
            heading,  # heading
            100,  # throttle
            0,  # alt
            0  # climb
        )

    def send_param(self, name, value, index):
        self.ml.param_value_send(
            name,
            value,
            mv.MAV_PARAM_TYPE_REAL32,
            len(self.params),
            index
        )

    def send_params(self):
        for param in self.params:
            name, value = param
            self.send_param(name, value, 0)

    def get_next_waypoint(self):
        if self.waypoint_count > 0:
            self.ml.mission_request_send(0, 0, self.last_sent_waypoint)
            self.last_sent_waypoint += 1

    def send_ack(self):
        self.ml.mission_ack_send(0, 0, mv.MAV_MISSION_ACCEPTED)

    def send_mission_list(self):
        self.ml.mission_count_send(0, 0, len(self.waypoints))

    def send_mission_item(self, seq):
        x, y = self.waypoints[seq-1]
        self.ml.mission_item_send(
            0,
            0,
            seq,
            mv.MAV_FRAME_GLOBAL,
            mv.MAV_CMD_NAV_WAYPOINT,
            1,  # is current waypoint
            True,
            0, 0, 0, 0,  # params
            x,
            y,
            0
        )

    def main(self):
        device = self.config.get('device', '/dev/ttyUSB0')
        baud = self.config.get('baud', 115200)

        self.ser = serial.Serial(device, baud, timeout=0.1)
        self.ml = mv.MAVLink(self.ser)

        self.waypoint_count = 0
        self.waypoints = []
        self.last_sent_waypoint = 0

        self.params = [(b'RUDDER', 0.5)]

        while self.running:
            lat, lon = self.goatd.goat.position()
            heading = self.goatd.goat.heading()

            self.send_heartbeat()
            self.send_position(lat, lon)
            self.send_heading(int(heading))

            buf = self.ser.read(32)
            messages = self.ml.parse_buffer(buf)
            if messages:
                for message in messages:
                    name = message.get_type()
                    if name == 'PARAM_REQUEST_LIST':
                        self.send_params()

                    if name == 'MISSION_COUNT':
                        self.waypoint_count = message.count
                        self.waypoints = [None for i in
                                          range(self.waypoint_count)]
                        self.last_sent_waypoint = 0
                        self.get_next_waypoint()

                    if name == 'MISSION_ITEM':
                        self.waypoints[message.seq-1] = (message.x, message.y)
                        if message.seq >= self.waypoint_count-1:
                            self.send_ack()
                        else:
                            self.get_next_waypoint()

                    if name == 'MISSION_REQUEST':
                        self.send_mission_item(message.seq)

                    if name == 'MISSION_REQUEST_LIST':
                        self.send_mission_list()


plugin = MavlinkPlugin
