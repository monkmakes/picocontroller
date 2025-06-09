from picocontroller import Relay_A
from time import sleep

#Relay_A.on_for(10000)
Relay_A.oscillate(200)

while True:
    print('doing stuff')
    sleep(1)