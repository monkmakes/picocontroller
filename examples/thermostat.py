from machine import Pin
from picocontroller import *
from time import sleep

import onewire # Prerequisite for the ds18x20 digital thermometer
import ds18x20

ONE_WIRE_PIN = 14 # The pin to be connected to the DS18B20's data pin

ow = onewire.OneWire(Pin(ONE_WIRE_PIN, pull=Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)

relay = Relay_A # You could change this to a different relay

MIN_T = 0  # Minimum set temperature 
MAX_T = 40

thermometer = None
t_set = 20.0
t = 0.0

def refresh_display(output_on):
    text_color = 1
    background_color = 0
    if output_on:
        text_color = 0
        background_color = 1
    display.fill(background_color)
    display.text('Measured', 5, 20, text_color)
    display.text(str(t), 90, 20, text_color)
    display.text('Set', 5, 40, text_color)
    display.text(str(t_set), 90, 40, text_color)
    display.show()
    
def connect_thermometer():
    global thermometer
    try:
        devices = ds.scan()
        thermometer = devices[0] # You can connect multiple DS18B20s to the same pin [0] for the first and only in this example
    except:
        print("Couldn't detect thermometer - check wiring")
        
def read_temp():
    global t
    ds.convert_temp()
    t = ds.read_temp(thermometer)

connect_thermometer()
refresh_display(False)
while True:
    # Check to see if the temperature has falled below the threshold
    read_temp()
    if t < t_set:
        # power on if measured temp too low
        relay.on()
        refresh_display(True)
    else:
        relay.off()
        refresh_display(False)
    # Check for button presses
    if Button_A.was_pressed() and t_set > MIN_T:
        t_set -= 1
        refresh_display(False)
    if Button_B.was_pressed() and t_set < MAX_T:
        t_set += 1
        refresh_display(False)
