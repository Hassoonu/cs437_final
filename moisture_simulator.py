#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import tty
import termios
import time
import random
import threading
import gpiod
from gpiod.line import Direction, Value

OUTPUT_PIN      = 27
UPDATE_INTERVAL = 3
DRY_THRESHOLD   = 0.4

request = gpiod.request_lines(
    '/dev/gpiochip0',
    consumer="MOISTURE",
    config={OUTPUT_PIN: gpiod.LineSettings(direction=Direction.OUTPUT)}
)

watered = threading.Event()

def listen_for_water():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == 'w':
                watered.set()
            elif ch in ('\x03', '\x04'):
                raise KeyboardInterrupt
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def simulate_moisture():
    bound_low  = 0.9
    bound_high = 1.0
    moisture   = random.uniform(bound_low, bound_high)
    while True:
        if watered.is_set():
            bound_low  = 0.9
            bound_high = 1.0
            moisture   = random.uniform(bound_low, bound_high)
            watered.clear()
            print("Plant watered -- bounds reset")

        is_dry = moisture < DRY_THRESHOLD
        request.set_value(OUTPUT_PIN, Value.ACTIVE if is_dry else Value.INACTIVE)

        status = "DRY" if is_dry else "WET"
        print(f"{status} | Moisture: {moisture:.2f} | Bounds: ({bound_low:.1f} - {bound_high:.1f})")
        time.sleep(UPDATE_INTERVAL)

        if bound_low > 0.0:
            bound_low  = round(bound_low  - 0.1, 1)
            bound_high = round(bound_high - 0.1, 1)
        moisture = random.uniform(bound_low, bound_high)

threading.Thread(target=listen_for_water, daemon=True).start()
print("Running... press 'w' to water, Ctrl+C to quit")
try:
    simulate_moisture()
finally:
    request.release()
