
import board
import time
import digitalio
import neopixel


# Use Pull.UP for external buttons wired to ground
button = digitalio.DigitalInOut(board.GP0)  # Wired to pin GP15
button.switch_to_input(pull=digitalio.Pull.UP)

strip = neopixel.NeoPixel(board.GP15, 30)

while True:
    if button.value == False:  # Button is pressed when False
        print("BUTTON IS PRESSED! button.value = False")
        strip.fill((0, 255, 0))
    else:  # Button is not pressed
        print("Button is NOT pressed. button.value = True")
        strip.fill((0, 0, 0))
    time.sleep(0.2)
