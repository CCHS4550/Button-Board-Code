#import board support libraries, including HID.
import board
import digitalio
import analogio
import usb_hid


from time import sleep


#library for communicating as a gamepad
from hid_gamepad import Gamepad


from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

mediacontrol = ConsumerControl(usb_hid.devices)

gp = Gamepad(usb_hid.devices)

#Create a collection of GPIO pins that represent the buttons
#This includes the digital pins for the Directional Pad.
#They can be used as regular buttons if using the analog inputs instead
#1 3 5 7 9 11
#2 4 6 8 10 12
button_pins = (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,
               board.GP12)

gamepad_buttons = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]

led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
led.value = True

#Initialize The Buttons
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    
# Setup for Analog Joystick as X and Y
# ax = analogio.AnalogIn(board.GP26)
# ay = analogio.AnalogIn(board.GP27)


# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
  
  
def debounce():
    sleep(0.2)

while True:
    led.value = True
    # Go through all the button definitions, and
    # press or release as appropriate
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
        else:
            gp.press_buttons(gamepad_button_num)
    