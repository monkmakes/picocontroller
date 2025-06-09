from machine import PWM
from picocontroller import Relay_A

pwm_Relay_A = PWM(Relay_A._pin)

while True:
    f = int(input('f (Hz):'))
    d = int(input('duty (0..65535):'))
    pwm_Relay_A.freq(f)
    pwm_Relay_A.duty_u16(d)