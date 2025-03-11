from machine import Pin, Timer, I2C
from time import sleep
from ssd1306 import SSD1306_I2C

RELAY_A_PIN = Pin(21, Pin.OUT)
RELAY_B_PIN = Pin(20, Pin.OUT)
RELAY_C_PIN = Pin(19, Pin.OUT)
RELAY_D_PIN = Pin(18, Pin.OUT)
    
BUZZER_A_PIN = Pin(3, Pin.OUT)
BUZZER_B_PIN = Pin(22, Pin.OUT)

SW_A_PIN = Pin(6, Pin.IN, pull=Pin.PULL_UP)
SW_B_PIN = Pin(7, Pin.IN, pull=Pin.PULL_UP)
SW_C_PIN = Pin(8, Pin.IN, pull=Pin.PULL_UP)
SW_D_PIN = Pin(9, Pin.IN, pull=Pin.PULL_UP)

W = 128
H = 64

i2c = I2C(0, sda=Pin(4, pull=Pin.PULL_UP), scl=Pin(5, pull=Pin.PULL_UP))
display = SSD1306_I2C(W, H, i2c, addr=0x3C)

class Relay:
    """A Class for Solid State Relays on the MonkMakes Pico Controller board"""

    _pin = None
    _timer = None

    def __init__(self, pin):
        self._pin = pin

    def on(self):
        self._pin.on()
        
    def off(self):
        self._pin.off()
        
    def value(self, value):
        self._pin.value(value)    

    def on_for(self, duration):
        self._pin.on()
        self._timer = Timer(mode=Timer.ONE_SHOT, period=duration, callback=lambda t:self.cancel_timer(0))

    def off_for(self, duration):
        self._pin.off()
        self._timer = Timer(mode=Timer.ONE_SHOT, period=duration, callback=lambda t:self.cancel_timer(1))

    def oscillate(self, duration):
        self._timer = Timer(mode=Timer.PERIODIC, period=duration, callback=lambda t:self._pin.toggle())
        
    def cancel_timer(self, value=0):
        self._pin.value(value)
        self._timer.deinit()
        
class Buzzer:
    """A Class for the push-pull Piezo Buzzer on the MonkMakes Pico Controller board"""
    
    _timer = None
        
    def _toggle(self):
        BUZZER_A_PIN.toggle()  
        BUZZER_B_PIN.toggle()
        
    def on(self, f = 1500): # resonant f is actually 4kHz, but 1.5kHz local maximum and better for the old
        if f < 1: # timer f of 0 causes Pico hang-up
            return
        self.off() # stop any timer that's running - no polyphony
        BUZZER_A_PIN.on() # push-pull - start out of phase
        BUZZER_B_PIN.off()
        self._timer = Timer(mode=Timer.PERIODIC, freq=f, callback=lambda t:self._toggle())
        
    def off(self):
        if (self._timer):
            self._timer.deinit()
        BUZZER_A_PIN.off()  # Piezo 0 current
        BUZZER_B_PIN.off()
        
class Button:
    """A Class for the navigation buttons on the MonkMakes Pico Controller board"""
    
    _pin = None

    def __init__(self, pin):
        self._pin = pin
    
    def is_pressed(self):
        return (self._pin.value() == 0)
    
    def was_pressed(self):
        if self._pin.value() == 0:
            # debounce and wait for key release
            sleep(0.1)
            while self._pin.value() == 0:
                pass
            return True
        return False
        
Relay_A = Relay(RELAY_A_PIN)
Relay_B = Relay(RELAY_B_PIN)
Relay_C = Relay(RELAY_C_PIN)
Relay_D = Relay(RELAY_D_PIN)
        
Button_A = Button(SW_A_PIN)
Button_B = Button(SW_B_PIN)
Button_C = Button(SW_C_PIN)
Button_D = Button(SW_D_PIN)


