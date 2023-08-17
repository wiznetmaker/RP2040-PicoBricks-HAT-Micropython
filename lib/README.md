# Picobricks API Documentation

## picobricks_button

### Methods

- `__init__(self, btn_pin=10, detect_time_ms=500, mode="on/off")`: Initializes the button with the specified pin, detect time (in milliseconds), and mode.
- `set_button_callback(self, on_callback=None, off_callback=None, push_callback=None)`: Sets the callback functions for the on, off, and push events.
- `get_value(self)`: Gets the value of the button (1 if pressed, 0 if not pressed).
- `set_toggle_button_state(self)`: Checks for button presses and toggles the switch state if pressed.

## picobricks_oled

### Methods

- `__init__(self, sda_pin=4, scl_pin=5, i2c_ch=0)`: Initializes the OLED display with the specified pins and I2C channel.
- `deinit(self)`: Clears the OLED display.
- `print_to_oled(self, string, start_x=5, start_y=5)`: Prints a string to the OLED at the specified coordinates.
- `print_line_oled(self, line1='', line2='', line3='', line4='', line5='')`: Prints up to five lines of text to the OLED.
- `print_string_oled(self, string, start_x=5, start_y=5, max_len=15, line_spacing=10)`: Prints a long string to the OLED with word wrapping.

## picobricks_neopixel

### Methods

- `__init__(self, neopixel_pin=6)`: Initializes the Neopixel LED with the specified pin.
- `set_neopixel(self, color, brightness)`: Sets the Neopixel LED color and brightness.
- `set_color(self, color)`: Sets the Neopixel LED color.
- `set_brightness(self, brightness)`: Sets the Neopixel LED brightness.

## RGBController

### Methods

- `__init__(self)`: Initializes the RGB controller with the default states.
- `cycle_rgb_state(self)`: Cycles through the RGB states.
- `get_rgb_state(self)`: Gets the current RGB state.

## picobricks_hum_temp

### Methods

- `__init__(self, humtemp_pin=11, get_timer=2)`: Initializes the humidity and temperature sensor with the specified pin and timer interval.
- `get_value_once(self)`: Gets the humidity and temperature values once.
- `get_value(self)`: Gets the humidity and temperature values at the specified timer interval.

## picobricks_potentiometer

### Methods

- `__init__(self, pot_pin=26, read_timer=1, min_val=0, max_val=100)`: Initializes the potentiometer with the specified pin, read timer, and min/max values.
- `get_value_once(self)`: Gets the potentiometer value once.
- `get_value(self)`: Gets the potentiometer value at the specified read timer interval.

## picobricks_LDR

### Methods

- `__init__(self, ldr_pin=27, get_timer=5)`: Initializes the light-dependent resistor (LDR) with the specified pin and timer interval.
- `map_value(self, old_value, old_min=10000, old_max=2000, new_min=0, new_max=100)`: Maps the LDR value to the specified range.
- `get_value_once(self)`: Gets the mapped LDR value once.
- `get_value(self)`: Gets the mapped LDR value at the specified timer interval.
