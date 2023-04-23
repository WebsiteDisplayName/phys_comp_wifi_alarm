# Bluetooth to Bluetooth SENDER Code (requires a BLE device running RECEIVER Code)
# Also assumes RECEIVER has a folder named drumSounds containing .wav files as listed in RECEIVER
# Also note sender & receiver must also send / look for the same receiver_name,
# which you'll find in the line below named.
# Be sure to change to something unique & <11 chars in BOTH the sender & receiver code.py files.
# receiver_name = "profg-r"

import board
import time
import touchio
import digitalio
import neopixel
import touchio
from adafruit_debouncer import Button
from adafruit_led_animation.animation.blink import Blink
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket

receiver_name = "receiver"

ble = BLERadio()
uart_connection = None


def send_packet(uart_connection_name, packet):
    """Returns False if no longer connected."""
    try:
        uart_connection_name[UARTService].write(packet.to_bytes())
    except:  # pylint: disable=bare-except
        try:
            uart_connection[UARTService].write(packet)
        except:  # pylint: disable=bare-except
            try:
                uart_connection_name.disconnect()
            except:  # pylint: disable=bare-except
                pass
            print("No longer connected")
            return False
    return True


# Audio
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True
audio = AudioOut(board.SPEAKER)

# Sound file path
path = ""


def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass


# SET UP COLORS & A COLORS LIST
RED = (255, 0, 0)
MAGENTA = (255, 0, 20)
ORANGE = (255, 40, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
JADE = (0, 255, 40)
BLUE = (0, 0, 255)
INDIGO = (63, 0, 255)
VIOLET = (127, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# CREATE AN ARRAY OF THESE COLORS
colors = [RED, MAGENTA, ORANGE, YELLOW, GREEN, JADE,
          BLUE, INDIGO, VIOLET, PURPLE, WHITE, BLACK]

# SET UP THE 10 NEOPIXELS ON THE CPB. NAME THEM PIXELS
pixels_length = 10
pixels = neopixel.NeoPixel(
    board.NEOPIXEL, pixels_length, auto_write=True, brightness=0.5)
blink1 = Blink(pixels, speed=0.1, color=GREEN)

# signal touchpad =
button_A1_input = digitalio.DigitalInOut(board.A1)
# Note: Pull.UP for external buttons
button_A1_input.switch_to_input(digitalio.Pull.UP)
# NOTE: value_when_pressed = default False for external buttons
button_A1 = Button(button_A1_input, value_when_pressed=True)


# These are the ButtonPacket codes that are the same as the 8 buttons on the Bluefruit App
bluefruit_button = ButtonPacket.BUTTON_1


while True:
    if not uart_connection or not uart_connection.connected:  # If not connected...
        print("Scanning...")
        # Scan...
        blink1.animate()

        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=1):
            if UARTService in adv.services:  # If UARTService found...
                if adv.complete_name == receiver_name:
                    # Create a UART connection...
                    uart_connection = ble.connect(adv)
                    print(f"I've found and connected to {receiver_name}!")
                    # MUST include this here or code will never continue after connection.
                    break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()  # And stop scanning.

    while uart_connection and uart_connection.connected:  # If connected...
        pixels.fill(BLACK)
        pixels[0] = GREEN
        button_A1.update()  # gets Debounced state
        if button_A1.pressed:  # if a pad is touched
            # then send the button corresponding to bluefruit_buttons for the pad pressed
            # Note: This means we'll never send the 8th button, BUTTON.RIGHT,
            # since there are only 7 touchpads on the CPB. RIGHT is sent by button_A, below
            if not send_packet(uart_connection,
                               ButtonPacket(bluefruit_button, pressed=True)):
                uart_connection = None
                continue
            print(f"Button 1 pressed!")
    pixels.fill(BLACK)
