# Generates and sends gcode to control the physical machine

import pandas as pd
from serial import Serial
from threading import Thread
from queue import Queue
from util import solve_affine
from pprint import pprint


class MeatPnP:
    def __init__(self, parts_filename, port_name=None):
        if port_name is not None:
            self.port = Serial(port_name, 115200)
            self.comms_thread = Thread(target=self.comms_handler, daemon=True)
            self.comms_thread.start()

        self.part_data = pd.read_csv(parts_filename)

        # parts_by_value = {}
        # for part in self.get_part_info():
        #     if not part['Val'] in parts_by_value:
        #         parts_by_value[part['Val']] = []
        #
        #     parts_by_value[part['Val']].append(part)
        #
        # values_by_count = list(parts_by_value.values())
        # values_by_count.sort(reverse=True, key=lambda arr: len(arr))
        # pprint(values_by_count)

        self.code_queue = Queue()

        self.position_x = 0
        self.position_y = 0

        hole_to_hole = 54.09  # mm
        left = -27.046834
        top = 27.173834
        self.jig_upper_left_position = (left, top, 0)
        self.jig_upper_right_position = (-left, top, 0)
        self.jig_lower_left_position = (left, -top, 0)
        self.jig_lower_right_position = (-left, -top, 0)
        # self.jig_upper_right_position = (left + 75 * 2 + hole_to_hole, top, 0)
        # self.jig_lower_left_position = (left, top + 75 + hole_to_hole, 0)
        # self.jig_lower_right_position = (left + 75 * 2 + hole_to_hole, top + 75 + hole_to_hole, 0)

        self.upper_left_position = None
        self.upper_right_position = None
        self.lower_left_position = None
        self.lower_right_position = None

    def comms_handler(self):
        lf = '\n'.encode('utf8')

        # Wait for the welcome message
        # Grbl 1.1f ['$' for help]
        # [MSG:'$H'|'$X' to unlock]
        while True:
            init_msg = self.port.read_until(lf).decode('utf8').rstrip()
            print('RX:', init_msg)

            if init_msg == "[MSG:'$H'|'$X' to unlock]":
                self.send_cmd('$X')
                break
            elif init_msg == "[MSG:Caution: Unlocked]":
                break

        self.send_cmd('G92 X0 Y0 Z0')
        print('Machine connected and initialized')

        while True:
            command = self.code_queue.get()
            self.send_cmd(command)

            reply = self.port.read_until(lf).decode('utf8').rstrip()
            if reply != 'ok' and reply != '[MSG:Caution: Unlocked]':
                raise Exception('Unexpected reply from machine: "{}"'.format(reply))

    def send_cmd(self, cmd):
        print('TX:', cmd)
        self.port.write((cmd + '\n').encode('utf8'))

    def run_gcode(self, gcode):
        self.code_queue.put(gcode)

    def corrected_position(self, x, y):
        have_correction = not (self.upper_left_position is None or self.upper_right_position is None or self.lower_left_position is None or self.lower_right_position is None)

        if not have_correction:
            return x, y

        correct_pos = solve_affine(
            self.jig_upper_left_position,
            self.jig_upper_right_position,
            self.jig_lower_left_position,
            self.jig_lower_right_position,
            self.upper_left_position,
            self.upper_right_position,
            self.lower_left_position,
            self.lower_right_position,
        )

        x, y, z = correct_pos((x, y, 0))
        return x, y

    def position(self):
        corrected_x, corrected_y = self.corrected_position(self.position_x, self.position_y)
        return corrected_x, corrected_y

    def home(self):
        self.run_gcode('$H')
        self.position_x = 0
        self.position_y = 0

    def move_relative(self, x, y):
        self.run_gcode('G91 X{} Y{}'.format(x, y))
        self.position_x += x
        self.position_y += y

    def move_to(self, x, y):
        corrected_x, corrected_y = self.corrected_position(x, y)

        self.move_relative(corrected_x - self.position_x, corrected_y - self.position_y)
        self.position_x = corrected_x
        self.position_y = corrected_y

    def move_to_part(self, part_name):
        part_info = self.part_data.loc[self.part_data['Ref'] == part_name]

        if part_info.empty:
            raise ValueError('Part not known')

        x = float(part_info['PosX'].iloc[0])
        y = float(part_info['PosY'].iloc[0])

        self.move_to(x, y)

    def get_part_info(self):
        info = []

        for index, row in self.part_data.iterrows():
            info.append(row.to_dict())

        return info

    def get_part_names(self):
        part_names = self.part_data['Ref'].to_numpy().tolist()
        return part_names

    def set_upper_left_position(self):
        self.upper_left_position = (self.position_x, self.position_y, 0)
        print('Set upper left position to', self.upper_left_position)

    def set_upper_right_position(self):
        self.upper_right_position = (self.position_x, self.position_y, 0)
        print('Set upper right position to', self.upper_right_position)

    def set_lower_left_position(self):
        self.lower_left_position = (self.position_x, self.position_y, 0)
        print('Set lower left position to', self.lower_left_position)

    def set_lower_right_position(self):
        self.lower_right_position = (self.position_x, self.position_y, 0)
        print('Set lower right position to', self.lower_right_position)
