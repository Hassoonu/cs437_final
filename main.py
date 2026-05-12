import threading
import time
import subprocess
import RPi.GPIO as GPIO
from pynput import keyboard
import firebase_interface as fbi


stop_event = threading.Event()

INTERVAL = 3 #60 * 60 * 6  # 6 hours (4 readings per day)
DO_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def set_wifi(enabled: bool):
    # turn it off/on
    pass


def set_hdmi(enabled: bool):
    # Turn it off/on
    pass


def low_power_wait(seconds):
    """Disable non-essential hardware during the long wait between readings."""
    #set_hdmi(False)
    #set_wifi(False)

    stop_event.wait(seconds)  # CPU idles here

    #set_wifi(True)
    #set_hdmi(True)


def wait_for_quit():
    def on_press(key):
        try:
            if key.char == 'z':
                stop_event.set()
                return False
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def get_sensor_data():
    needs_water = GPIO.input(DO_PIN)  # 1 = dry, 0 = wet
    return {"needs_water": bool(needs_water)}


def main():
    my_key = "needs_water"

    threading.Thread(target=wait_for_quit, daemon=True).start()

    while not stop_event.is_set():
        data = get_sensor_data()
        print(f"data is: {data}")
        fbi.set_data(my_key, data)
        low_power_wait(INTERVAL)

    GPIO.cleanup()


if __name__ == '__main__':
    main()
