from picocontroller import *
from picocontroller.gui import *
from time import sleep

relay_b_submenu_data =  [
    {'id' : 'relay_B_on', 'label' : 'On'},
    {'id' : 'relay_B_off', 'label' : 'Off'},
    {'id' : 'back', 'label' : 'Back'}
    ]       

menu_data = [
    {'id' : 'relay_A_on', 'label' : 'Relay A on'},
    {'id' : 'relay_A_off', 'label' : 'Relay A off'},
    {'id' : 'relay_B_submenu', 'label' : 'Relay B >'}
    ]

main_menu = Menu(menu_data)
relay_b_submenu = Menu(relay_b_submenu_data)

menu = main_menu
menu.draw_menu()

while True:
    selection = menu.check_keys()
    if selection:
        print(selection)
        if selection == 'relay_B_submenu':
            menu = relay_b_submenu
            menu.draw_menu()
        if selection == 'back':
            menu = main_menu
            menu.draw_menu()
        if selection == 'relay_A_on':
            Relay_A.on()
        if selection == 'relay_A_off':
            Relay_A.off()
        if selection == 'relay_B_on':
            Relay_B.on()
        if selection == 'relay_B_off':
            Relay_B.off()
    sleep(0.1)