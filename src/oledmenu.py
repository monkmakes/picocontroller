from machine import I2C
from picocontroller import *
from ssd1306 import SSD1306_I2C

class Menu:
    """A Class for Menus using the OLED and buttons on the MonkMakes Pico Controller board"""
    
    _W = 0
    _H = 0
    _MENU_SEP = 0
    
    _menu_data = None
    _i2c = None
    _oled = None
    _selection = None
    _selection_index = 0

    def __init__(self, menu_data, width=128, height=64, menu_sep=10):
        self._menu_data = menu_data
        self._selection = menu_data[0]
        self._W = width
        self._H = height
        self._MENU_SEP = menu_sep
        
        self._i2c = I2C(0, sda=Pin(4, pull=Pin.PULL_UP), scl=Pin(5, pull=Pin.PULL_UP))
        self._oled = SSD1306_I2C(self._W, self._H, self._i2c, addr=0x3C)
        
    def draw_menu(self):
        menu_data = self._menu_data
        self._oled.fill(0)
        y = 0
        n = len(menu_data)
        for menu_item in menu_data:
            if self._selection == menu_item:
                self._oled.fill_rect(0, y, self._W-3, self._MENU_SEP, 1)
                self._oled.text(menu_item['label'], 3, y+2, 0)
            else:
                self._oled.text(menu_item['label'], 3, y+2, 1)
            y += self._MENU_SEP
        self._oled.text('ok', 75, 55, 1)
        if self._selection_index > 0:
             self._oled.text('^', 10, 58, 1)
        if self._selection_index < n-1:
             self._oled.text('v', 45, 58, 1)

        self._oled.show()
        
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
            
