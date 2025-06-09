from picocontroller.gui import OLEDConsole
from time import sleep

log = OLEDConsole()

x = 0
while True:
    log.print('Counting ' + str(x))
    x += 1
    sleep(1)