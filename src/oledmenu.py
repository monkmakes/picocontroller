from machine import I2C
from picocontroller import *
from ssd1306 import SSD1306_I2C

class Menu:
    """A Class for Menus using the OLED and buttons on the MonkMakes Pico Controller board"""
    
    _MENU_SEP = 0
    
    _menu_data = None
    _i2c = None
    _oled = None
    _selection = None
    _selection_index = 0

    def __init__(self, menu_data, menu_sep=10):
        self._menu_data = menu_data
        self._selection = menu_data[0]
        self._MENU_SEP = menu_sep
        
    def oled(self):
        return self._oled
        
    def draw_menu(self):
        menu_data = self._menu_data
        display.fill(0)
        y = 0
        n = len(menu_data)
        for menu_item in menu_data:
            if self._selection == menu_item:
                display.fill_rect(0, y, W-3, self._MENU_SEP, 1)
                display.text(menu_item['label'], 3, y+2, 0)
            else:
                display.text(menu_item['label'], 3, y+2, 1)
            y += self._MENU_SEP
        display.text('ok', 75, 55, 1)
        if self._selection_index > 0:
             display.text('^', 10, 58, 1)
        if self._selection_index < n-1:
             display.text('v', 45, 58, 1)

        display.show()
        
    def check_keys(self):
        menu_data = self._menu_data
        n = len(menu_data)
        if Button_A.was_pressed() and self._selection_index > 0:
            self._selection_index -= 1
            self._selection = menu_data[self._selection_index]
            self.draw_menu()
        if Button_B.was_pressed() and self._selection_index < n-1:
            self._selection_index += 1
            self._selection = menu_data[self._selection_index]
            self.draw_menu()
        if Button_C.was_pressed():
            return self._selection['id']
        return None
            
