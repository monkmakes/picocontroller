from picocontroller import *
from time import sleep
from random import random, randint

padelW = 4
padelH = 15
balld = 4 # ball diameter
p1x = 0 # player 1
p1y = int(H/2)
p2x = W-padelW-1
p2y = int(H/2)
netx = int(W/2) # net position
x = W/2
y = H/2
dx = 0.8
dy = 0.9
goals1 = 0
goals2 = 0
win = 5 # goals required for a win
padelStep = 2 # pixels to move at a time

buzzer = Buzzer()

def draw_net():
    display.vline(netx, 0, H-1, 1)
    
def draw_padel(x, y):
    display.rect(x, y, padelW, padelH, 1)
    
def draw_scores():
    display.text(str(goals1), netx-30, 0, 1)
    display.text(str(goals2), W-netx+20, 0, 1)
    
def refresh_display():
    display.fill(0)    
    draw_net()
    draw_scores()
    draw_padel(p1x, p1y)
    draw_padel(p2x, p2y)
    display.rect(int(x), int(y), balld, balld, 1)
    display.show()
    
def update_ball():
    global x, y
    x += dx
    y += dy

def check_keys():
    global p1y, p2y
    if Button_A.is_pressed() and p1y > 0:
        p1y -= padelStep
    if Button_B.is_pressed() and p1y < H-padelH:
        p1y += padelStep
    if Button_C.is_pressed() and p2y > 0:
        p2y -= padelStep
    if Button_D.is_pressed() and p2y < H-padelH:
        p2y += padelStep

def restart():
    global x, y, dx, dy
    x, y, dx, dy = W/2, H/2, 1+random()/3, 1+random()/3
    
def play_celebration():
    notes = 		[261, 293, 329, 349, 392, 440, 493, 523]
    durations = [0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.6]
    for i in range(0, len(notes)):
        buzzer.on(notes[i])
        sleep(durations[i])
    buzzer.off()
    
def gameover(message):
    global goals1, goals2
    display.fill(0)
    display.text(message, 0, 0, 1)
    display.text('Press Button A', 0, 30, 1)
    display.text('to Play Again', 0, 50, 1)
    display.show()
    play_celebration()
    while not Button_A.was_pressed():
        pass
    goals1, goals2 = 0, 0
    restart()
    
def check_collisions():
    global dx, dy, goals1, goals2
    buzzer.off()
    if x <= p1x + padelW and y >= p1y and y <= p1y + padelH:
        # p1 hits it
        dx = -dx
        dy = 1+random()/3
        buzzer.on()
    if x >= p2x and y >= p2y and y <= p2y + padelH:
        # p1 hits it
        dx = -dx
        dy = -(1+random()/3)
        buzzer.on()
    if y <= 0 or y >= H-balld:
        # hit wall
        dy = -dy
    if x <= 0:
        goals2 += 1
        if goals2 >= win:
            gameover('Player 2 wins')
        restart()
    if x >= W:
        goals1 += 1
        if goals1 >= win:
            gameover('Player 1 wins')
        restart()
        
while True:
    check_keys()
    update_ball()
    check_collisions()
    refresh_display()
