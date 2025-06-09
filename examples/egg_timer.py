from picocontroller import *
from picocontroller.gui import *
from time import sleep
from machine import Timer

buzzer = Buzzer()
t = Timer()

time_display = SevenSegDisplay(0, 0, digit_w=20, digit_h=40, num_digits=3) # define a 3 digit display

default_mins = 5 # the timer will be reset to this when you press button D
default_secs = 0

mins = default_mins
secs = default_secs
is_running = False # The state of the timer: running or not

# Set a timer to calle update_time every second
t.init(mode=Timer.PERIODIC, period=1000, callback=lambda t:update_time())

def update_time():
    global mins, secs
    if not is_running:
        return # nothing to do
    if secs == 0:
        if mins == 0:
            stop_running() # secs and mins both 0 so stop the timer and buzz
            buzzer.on()
        else:
            secs = 59 # end of the minute so decrease mins by 1 and start secs at 59 again
            mins -= 1
    else:
        secs -= 1
    update_display()
    
def start_running():
    global is_running
    is_running = True
    
def stop_running():
    global is_running
    is_running = False
    
def update_display():
    time_display.draw(mins * 100 + secs)
    
update_display() # so that something appears when program first runs

while True:
    # button press handling
    if Button_A.was_pressed() and not is_running: # increase mins 
        buzzer.off()
        if mins < 9:
            mins += 1
            update_display()
    if Button_B.was_pressed(): # decrease mins
        buzzer.off()
        if mins > 1:
            mins -= 1
            update_display()
    if Button_C.was_pressed(): # toggle running on and off
        buzzer.off()
        if is_running:
            stop_running()
        else:
            start_running()
    if Button_D.was_pressed(): # restart the timer
        buzzer.off()
        mins = default_mins
        secs = default_secs
        stop_running()
        update_display()
        

