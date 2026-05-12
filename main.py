import threading
import time
import subprocess
import RPi.GPIO as GPIO
from pynput import keyboard
import firebase_interface as fbi


stop_event = threading.Event()

INTERVAL = 60 * 60 * 6  # 6 hours (4 readings per day)
DO_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN)


def set_wifi(enabled: bool):
    state = "off" if not enabled else "on"
    subprocess.run(["sudo", "ifconfig", "wlan0", state])
    if enabled:
        time.sleep(5)  # Give WiFi time to reconnect


def set_hdmi(enabled: bool):
    if enabled:
        subprocess.run(["sudo", "tvservice", "-p"])       # Power on
    else:
        subprocess.run(["sudo", "tvservice", "-o"])       # Power off


def low_power_wait(seconds):
    """Disable non-essential hardware during the long wait between readings."""
    set_hdmi(False)
    set_wifi(False)

    stop_event.wait(seconds)  # CPU idles here

    set_wifi(True)
    set_hdmi(True)


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
    fbi.connect_to_db()

    my_key = "money_tree"

    threading.Thread(target=wait_for_quit, daemon=True).start()

    while not stop_event.is_set():
        data = get_sensor_data()
        fbi.set_data(my_key, data)
        low_power_wait(INTERVAL)

    GPIO.cleanup()


if __name__ == '__main__':
    main()