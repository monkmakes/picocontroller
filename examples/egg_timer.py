from picocontroller import *
from picocontrollergui import *
from time import sleep


buzzer = Buzzer()
t = Timer()

time_display = SevenSegDisplay(0, 0, digit_w=20, digit_h=40, num_digits=3)

default_mins = 5
default_secs = 0

mins = default_mins
secs = default_secs
is_running = False

def update_time():
    global mins, secs
    if secs == 0:
        if mins == 0:
            t.deinit()
            buzzer.on()
        else:
            secs = 59
            mins -= 1
    else:
        secs -= 1
    update_display()
    
def start_running():
    global is_running
    is_running = True
    t.init(mode=Timer.PERIODIC, period=1000, callback=lambda t:update_time())
    
def stop_running():
    global is_running
    is_running = False
    t.deinit()
    
def update_display():
    time_display.draw(mins * 100 + secs)
    
update_display()    
while True:
    if Button_A.was_pressed() and not is_running:
        buzzer.off()
        if mins < 9:
            mins += 1
            update_display()
    if Button_B.was_pressed():
        buzzer.off()
        if mins > 1:
            mins -= 1
            update_display()
    if Button_C.was_pressed():
        buzzer.off()
        if is_running:
            stop_running()
        else:
            start_running()
    if Button_D.was_pressed():
        buzzer.off()
        mins = default_mins
        secs = default_secs
        stop_running()
        update_display()
        

