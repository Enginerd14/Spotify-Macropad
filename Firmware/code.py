import board
import busio
import displayio
import i2cdisplaybus
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions import Extension

DISPLAY_ENABLED = False

try:
    displayio.release_displays()
    i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
    display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
    display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

    splash = displayio.Group()
    display.root_group = splash
    
    bmp = displayio.Bitmap(128, 32, 2)
    pal = displayio.Palette(2)
    pal[0] = 0x000000
    pal[1] = 0xFFFFFF

    rects = [
        (22, 0, 18),(22, 1, 18),(19, 2, 6),(28, 2, 15),(19, 3, 24),(19, 4, 24),
        (19, 5, 12),(113, 5, 5),(19, 6, 13),(113, 6, 5),(19, 7, 19),(113, 7, 5),
        (0, 8, 3),(16, 8, 12),(112, 8, 6),(0, 9, 3),(16, 9, 12),(113, 9, 5),
        (0, 10, 7),(13, 10, 22),(84, 10, 6),(103, 10, 6),(112, 10, 6),(121, 10, 7),
        (0, 11, 7),(13, 11, 22),(85, 11, 5),(103, 11, 6),(113, 11, 5),(121, 11, 6),
        (0, 12, 28),(32, 12, 3),(85, 12, 5),(93, 12, 3),(103, 12, 6),(113, 12, 5),
        (121, 12, 6),(0, 13, 28),(32, 13, 3),(85, 13, 5),(93, 13, 3),(103, 13, 6),
        (113, 13, 5),(121, 13, 6),(0, 14, 28),(85, 14, 5),(93, 14, 3),(103, 14, 6),
        (113, 14, 5),(121, 14, 6),(4, 15, 24),(78, 15, 3),(85, 15, 5),(93, 15, 3),
        (103, 15, 6),(113, 15, 5),(121, 15, 6),(4, 16, 24),(78, 16, 3),(85, 16, 5),
        (93, 16, 3),(103, 16, 6),(113, 16, 5),(121, 16, 6),(7, 17, 18),(78, 17, 3),
        (84, 17, 12),(103, 17, 24),(10, 18, 12),(78, 18, 3),(85, 18, 5),(106, 18, 18),
        (10, 19, 12),(78, 19, 3),(85, 19, 5),(106, 19, 18),(10, 20, 5),(19, 20, 3),
        (78, 20, 12),(112, 20, 6),(10, 21, 5),(19, 21, 3),(78, 21, 12),(113, 21, 5),
        (10, 22, 3),(19, 22, 3),(32, 22, 6),(53, 22, 7),(84, 22, 6),(113, 22, 5),
        (10, 23, 3),(19, 23, 3),(32, 23, 6),(53, 23, 7),(85, 23, 5),(113, 23, 5),
        (10, 24, 5),(19, 24, 6),(28, 24, 3),(38, 24, 2),(50, 24, 3),(60, 24, 3),
        (85, 24, 5),(112, 24, 6),(4, 25, 24),(40, 25, 10),(63, 25, 11),(75, 25, 6),
        (85, 25, 5),(93, 25, 6),(100, 25, 9),(113, 25, 5),(122, 25, 2),(125, 25, 2),
        (4, 26, 24),(40, 26, 10),(63, 26, 18),(85, 26, 5),(93, 26, 16),(113, 26, 5),
        (121, 26, 6),(32, 27, 6),(53, 27, 7),(84, 27, 6),(113, 27, 5),(32, 28, 6),
        (53, 28, 6),(85, 28, 5),(113, 28, 5),(7, 29, 6),(44, 29, 6),(63, 29, 5),
        (93, 29, 6),(103, 29, 6),(25, 30, 6),(75, 30, 6),(121, 30, 6),(25, 31, 6),
        (75, 31, 6),(121, 31, 6),
    ]

    for x, y, w in rects:
        for i in range(w):
            if 0 <= x + i < 128 and 0 <= y < 32:
                bmp[x + i, y] = 1

    splash.append(displayio.TileGrid(bmp, pixel_shader=pal, x=0, y=0))

    DISPLAY_ENABLED = True

except Exception as e:
    print(f"Display not available: {e}")

class DisplayExt(Extension):
    def during_bootup(self, keyboard): pass
    def before_matrix_scan(self, keyboard): pass
    def after_matrix_scan(self, keyboard): pass
    def before_hid_send(self, keyboard): pass
    def after_hid_send(self, keyboard): pass
    def on_powersave_enable(self, keyboard): pass
    def on_powersave_disable(self, keyboard): pass

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(DisplayExt())

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.RX, board.SCK, board.TX, False),)
encoder_handler.map = [((KC.VOLU, KC.VOLD, KC.MUTE),)]
keyboard.modules.append(encoder_handler)

keyboard.matrix = KeysScanner(
    pins=[board.A0, board.A1, board.A2, board.A3],
    value_when_pressed=False,
)

LIKE = KC.LALT(KC.LSFT(KC.B))
keyboard.keymap = [[KC.MPRV, KC.MNXT, KC.MPLY, LIKE]]

if __name__ == '__main__':
    keyboard.go()
