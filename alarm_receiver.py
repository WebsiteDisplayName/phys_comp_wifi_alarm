
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut
import board
import neopixel
import digitalio
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.rainbow import Rainbow

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket
from adafruit_bluefruit_connect.raw_text_packet import RawTextPacket


ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# This MUST be the same name - same spelling & capitalization
# as the name in the "receiver_name = " line in the SENDER's code.py file.
# VERY IMPORTANT - the name must also be <= 11 characters!
advertisement.complete_name = "receiver"
ble.name = advertisement.complete_name

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
    board.NEOPIXEL, pixels_length, brightness=0.5)
blink1 = Blink(pixels, speed=1, color=GREEN)
rainbow1 = Rainbow(pixels, speed=0.5, period=5, step=1)

while True:
    ble.start_advertising(advertisement)  # Start advertising.

    # Name prints once each time the board isn't connected
    print(f"Advertising as: {advertisement.complete_name}")
    was_connected = False

    while not was_connected or ble.connected:
        blink1.animate()
        if ble.connected:  # If BLE is connected...
            was_connected = True
            pixels.fill(BLACK)
            pixels[0] = GREEN

            if uart.in_waiting:  # Check to see if any new data has been sent from the SENDER.
                try:
                    # Create the packet object.
                    packet = Packet.from_stream(uart)
                except ValueError:
                    continue
                # Note: I could have sennt ColorPackets that would have had colors, but I wanted
                # to show ButtonPackets because you could do non-color things here, too. For example,
                # if Button_1, then move a servo, if Button_2, then play a certain sound, etc.
                # If the packet is a button packet...
                if isinstance(packet, ButtonPacket):
                    if packet.button.pressed:  # If the buttons on the Remote Control are pressed...
                        rainbow1.animate()
                        rainbow1.show()
    pixels.fill(BLACK)

    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
