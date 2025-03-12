from machine import I2C
from picocontroller import *
from ssd1306 import SSD1306_I2C

class SevenSegDigit:
    
    
    SEG_MAP = ['ABCDEF', 'BC', 'ABGED', 'ABCDG', 'FGBC', 'AFGCD', 'AFGCDE', 'ABC', 'ABCDEFG', 'ABCDFG']
    
    def __init__(self, x, y, digit_w=25, digit_h=40):
        seg_short = int(digit_w * 0.2)
        seg_long = int(digit_w * 0.8)
        self.SEG_COORDS = {}
                          # x y w h
        self.SEG_COORDS['A'] = (x + seg_short, y, seg_long, seg_short)
        self.SEG_COORDS['B'] = (x + seg_long + seg_short, y + seg_short, seg_short, seg_long)
        self.SEG_COORDS['C'] = (x + seg_long + seg_short, y + seg_long + seg_short * 2, seg_short, seg_long)
        self.SEG_COORDS['D'] = (x + seg_short, y + seg_long * 2 + seg_short * 2, seg_long, seg_short)
        self.SEG_COORDS['E'] = (x, y + seg_long + seg_short * 2, seg_short, seg_long)
        self.SEG_COORDS['F'] = (x, y + seg_short, seg_short, seg_long)
        self.SEG_COORDS['G'] = (x + seg_short, y + seg_long + seg_short, seg_long, seg_short)
        dp_radius = int(seg_short / 1.5)
        self.SEG_COORDS['p'] = (x + digit_w + seg_short * 2, y + digit_h + seg_short * 2, dp_radius, dp_radius)
      
    def draw_segments(self, segments):
        # A
        #F B
        # G
        #E C
        # D   p
        self._undraw_segments()
        for seg in segments:
            if seg == 'p':
                x, y, rx, ry = self.SEG_COORDS['p']
                display.ellipse(x, y, rx, ry, 1, True)
            else:    
                x, y, w, h = self.SEG_COORDS[seg]
                display.rect(x, y, w, h, 1, True)
        display.show()  
      
    def _undraw_segments(self):
        for seg in 'ABCDEFGp':
            if seg == 'p':
                x, y, rx, ry = self.SEG_COORDS['p']
                display.ellipse(x, y, rx, ry, 0, True)
            else:    
                x, y, w, h = self.SEG_COORDS[seg]
                display.rect(x, y, w, h, 0, True)
        
    def draw(self, value, dp=False):
        segs = self.SEG_MAP[value]
        if dp:
            segs += 'p'
        self.draw_segments(segs)
        
class SevenSegDisplay:
    
    _num_digits = 0
    
    def __init__(self, x, y, digit_w=20, digit_h=40, num_digits=4):
        self.DIGITS = []
        self._num_digits = num_digits
        digit_spacing = int(digit_w * 1.4)
        for d in range(0, num_digits):
            self.DIGITS.append(SevenSegDigit(d * digit_spacing, y, digit_w=digit_w, digit_h=digit_h))
        
    def draw(self, value):
        digit_values = []
        x = value
        for d in range(0, self._num_digits):
            self.DIGITS[self._num_digits-d-1].draw(x % 10)
            x = int(x / 10)


class OLEDConsole:
    
    _line_spacing = 0
    _current_line = 0
    _num_lines = 0
    
    def __init__(self, line_spacing=10):
        self._line_spacing = line_spacing
        self._num_lines = int(H / line_spacing)
    
    def print(self, text):
        y = self._current_line * self._line_spacing
        if self._current_line == self._num_lines:
            display.scroll(0, -self._line_spacing)
            display.rect(0, H-self._line_spacing, W, self._line_spacing, 0, True) # clear the bottom row
            display.text(text, 0, y-self._line_spacing, 1)
        else:
            self._current_line += 1
            display.text(text, 0, y, 1)
        display.show()
        
    def clear(self):
        display.fill(0)
        display.show()
        self._current_line = 0


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
            

