#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 15 - Beacon Exclusion Zone """

from paoc.helper import get_input, print_summary
import re


class Sensor:
    def __init__(self, x, y, b_y, b_x):
        self.x = x
        self.y = y
        self.reach = abs(b_y - y) + abs(b_x - x)
        self.rim = set()

    def define_rim(self):
        x, y, r = self.x, self.y, self.reach  # shorthand for readability
        self.rim.update(set(zip(range(x+r+1, x, -1), range(y, y+r+1))))
        self.rim.update(set(zip(range(x-r-1, x), range(y, y+r+1))))
        self.rim.update(set(zip(range(x+r+1, x, -1), range(y, y-r-1, -1))))
        self.rim.update(set(zip(range(x-r-1, x), range(y, y-r-1, -1))))
        self.rim.update({(x, y+r+1), (x, y-r-1)})
    
    def render_rim(self):
        print(f'sensor at ({self.x}, {self.y}) with reach {self.reach}')
        for y in range(0, 20):
            for x in range(0, 20):
                if (x, y) in self.rim:             print('#', end='')
                elif x == self.x and y == self.y:  print('S', end='')
                else:                              print('.', end='')
            print()
        print('-'*20)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def get_sensors(lines: list[str]) -> list[Sensor]:
    sensors = []
    for line in lines:
        s_x, s_y, n_x, b_y = re.findall(r'(-?\d+)', line)
        sensors.append(Sensor(int(s_x), int(s_y), int(b_y), int(n_x)))
    return sensors

def reachable_in_row(row_num: int, sensor: Sensor) -> set[int]:
    # find distance from sensor to row
    d_row = abs(sensor.y - row_num)
    # find all x-positions in row that are in range of sensor
    span = sensor.reach - d_row
    if span < 0: return set()
    return set(range(sensor.x - span+1, sensor.x + span + 1))

def p1() -> any:
    lines = get_input(15)
    row_num = 2_000_000
    sensors = get_sensors(lines)
    scanned = set()
    for sensor in sensors:
        reachable = reachable_in_row(row_num, sensor)
        scanned.update(reachable)
    return len(scanned)

def p2() -> any:
    lines = get_input(15)
    max_rc = 4000000
    sensors = get_sensors(lines)

    for sensor in sensors:
        sensor.define_rim()
        for x, y in sensor.rim:
            if x < 0 or x > max_rc or y < 0 or y > max_rc: continue
            for other_sensor in sensors:
                if other_sensor == sensor: continue
                if abs(x - other_sensor.x) + abs(y - other_sensor.y) <= other_sensor.reach:
                    break
            else:
                return x * 4_000_000 + y
    return 'not found'


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
