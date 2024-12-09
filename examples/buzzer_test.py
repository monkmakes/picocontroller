from picocontroller import *
from time import sleep

"""
Press Button A for tone 1.5kHz
B to turn off
C for tone 4kHz
D for a quick beep
"""

buzzer = Buzzer()

while True:
    if Button_A.was_pressed():
        buzzer.on()
    if Button_B.was_pressed():
        buzzer.off()
    if Button_C.was_pressed():
        buzzer.on(4000)
    if Button_D.was_pressed():
        buzzer.on()
        sleep(0.3)
        buzzer.off()