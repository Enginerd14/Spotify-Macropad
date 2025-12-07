import board
import busio
import displayio
import terminalio
import time
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation
from kmk.modules.encoder import Encoder


# -------------------------------------------------------
# KMK SETUP
# -------------------------------------------------------

keyboard = KMKKeyboard()

# SW1–SW4 pins
keyboard.row_pins = [
    board.GP26,  # SW1
    board.GP27,  # SW2
    board.GP28,  # SW3
    board.GP29,  # SW4
]

keyboard.col_pins = []
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary encoder (SW5)
encoder = Encoder()
encoder.pins = (
    (board.GP0, board.GP1, board.GP2),  # A, B, Switch
)
encoder.map = [
    ((KC.VOLD, KC.VOLU), KC.MUTE)  # CCW → down, CW → up, press → mute
]
keyboard.modules.append(encoder)

# Keymap
keyboard.keymap = [
    [
        KC.LCTRL(KC.LEFT),     # SW1 - Previous song
        KC.LCTRL(KC.RIGHT),    # SW2 - Next song
        KC.SPACE,              # SW3 - Play/Pause
        KC.LALT(KC.LSFT(KC.B)) # SW4 - Add to Liked Songs
    ]
]


# -------------------------------------------------------
# OLED DISPLAY SETUP
# -------------------------------------------------------

displayio.release_displays()

# OLED uses GP7=SCL, GP6=SDA
i2c = busio.I2C(board.GP7, board.GP6)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1306(display_bus, width=128, height=32)

# Display group
splash = displayio.Group()
display.show(splash)

# Labels
weekday_label = label.Label(
    terminalio.FONT,
    text="---",
    color=0xFFFFFF,
    x=0,
    y=10
)

datetime_label = label.Label(
    terminalio.FONT,
    text="--:-- --/--/----",
    color=0xFFFFFF,
    x=0,
    y=26
)

splash.append(weekday_label)
splash.append(datetime_label)

# Weekday names
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

last_update = 0


# -------------------------------------------------------
# SMART AUTO-SCROLLING (ONLY IF TOO LONG)
# -------------------------------------------------------

def auto_scroll_label(label_obj, max_width=128, speed=1):
    """
    Scroll text if wider than the display; remain stationary if it fits.
    """
    text_width = label_obj.bounding_box[2]

    # Reset if text fits (stop scrolling)
    if text_width <= max_width:
        label_obj.x = 0
        return

    # Scroll left
    label_obj.x -= speed

    # Wraparound
    if label_obj.x < -text_width:
        label_obj.x = max_width


# -------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------

while True:
    # KMK processing
    keyboard.go(process_keyboard=True)

    # Update clock once per second
    now = time.monotonic()
    if now - last_update >= 1:
        last_update = now

        t = time.localtime()

        weekday = DAYS[t.tm_wday]

        # Format: HH:MM DD-MM-YYYY
        formatted = "{:02}:{:02} {:02}-{:02}-{:04}".format(
            t.tm_hour, t.tm_min,
            t.tm_mday, t.tm_mon, t.tm_year
        )

        weekday_label.text = weekday
        datetime_label.text = formatted

    # After updating text, determine if scrolling needed
    auto_scroll_label(datetime_label)