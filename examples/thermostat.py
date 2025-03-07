from machine import Pin
from picocontroller import *
from time import sleep

import onewire
import ds18x20

ONE_WIRE_PIN = 14

ow = onewire.OneWire(Pin(ONE_WIRE_PIN, pull=Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)

relay = Relay_A

MIN_T = 0
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
        thermometer = devices[0]
    except:
        print("Couldn't detect thermometer - check wiring")
        
def read_temp():
    global t
    ds.convert_temp()
    t = ds.read_temp(thermometer)

connect_thermometer()
refresh_display(False)
while True:
    read_temp()
    if t < t_set:
        # power on if measured temp too low
        relay.on()
        refresh_display(True)
    else:
        relay.off()
        refresh_display(False)
    if Button_A.was_pressed() and t_set > MIN_T:
        t_set -= 1
        refresh_display(False)
    if Button_B.was_pressed() and t_set < MAX_T:
        t_set += 1
        refresh_display(False)
