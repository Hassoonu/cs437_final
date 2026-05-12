import time
import random
import threading
import RPi.GPIO as GPIO
from pynput import keyboard

OUTPUT_PIN      = 27
UPDATE_INTERVAL = 3
DRY_THRESHOLD   = 0.4

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

watered = threading.Event()


def listen_for_water():
    def on_press(key):
        try:
            if key.char == 'w':
                watered.set()
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


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
        GPIO.output(OUTPUT_PIN, GPIO.HIGH if is_dry else GPIO.LOW)

        status = "DRY" if is_dry else "WET"
        print(f"{status} | Moisture: {moisture:.2f} | Bounds: ({bound_low:.1f} - {bound_high:.1f})")

        time.sleep(UPDATE_INTERVAL)

        if bound_low > 0.0:
            bound_low  = round(bound_low  - 0.1, 1)
            bound_high = round(bound_high - 0.1, 1)

        moisture = random.uniform(bound_low, bound_high)


threading.Thread(target=listen_for_water, daemon=True).start()

try:
    simulate_moisture()
finally:
    GPIO.cleanup()