from picobricks import SSD1306_I2C,WS2812, DHT11,NEC_16, IR_RX
from utime import sleep
import time
import network
import machine
from machine import ADC, Pin

OLED_WIDTH = 128
OLED_HEIGHT = 64

class picobricks_button:
    def __init__(self, btn_pin=10, detect_time_ms=500, mode="on/off"):
        self.button = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.switch_state = False
        self.last_check = time.ticks_ms()
        self.detect_time_ms = detect_time_ms
        self.on_callback = None
        self.off_callback = None
        self.push_callback = None
        self.mode = mode
        
    def set_button_callback(self, on_callback=None, off_callback=None, push_callback=None):
        self.on_callback = on_callback
        self.off_callback = off_callback
        self.push_callback = push_callback

    def get_value(self):
        return self.button.value()

    def set_toggle_button_state(self):  
        if (time.ticks_ms() - self.last_check) > self.detect_time_ms:
            current_state = self.get_value()
            if current_state == 1:  # Button is pressed
                if self.mode == "on/off":
                    self.switch_state = not self.switch_state  # Toggle the switch
                    print(f'Switch is {"on" if self.switch_state else "off"}')
                    if self.switch_state and self.on_callback:
                        self.on_callback()
                    elif not self.switch_state and self.off_callback:
                        self.off_callback()
                elif self.mode == "push" and self.push_callback:
                    self.push_callback()
            self.last_check = time.ticks_ms()


class picobricks_oled:

    def __init__(self, sda_pin=4, scl_pin=5, i2c_ch=0):
        sda = machine.Pin(sda_pin)
        scl = machine.Pin(scl_pin)
        i2c = machine.I2C(i2c_ch, sda=sda, scl=scl, freq=1000000)

        self.oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
        self.oled.text("Power On", 30, 0)
        self.oled.text("Waiting for ", 20, 30)
        self.oled.text("Connection", 23, 40)
        self.oled.show()
        time.sleep(1)

        self.oled.fill(0)

    def deinit(self):
        self.oled.fill(0)
        self.oled.show()

    def print_to_oled(self, string, start_x=5, start_y=5):
        self.oled.text(string, start_x, start_y)
        self.oled.show()

    def print_line_oled(self, line1='', line2='', line3='', line4='', line5=''):
        self.oled.fill(0)  # Clear the screen
        
        if line1:
            self.oled.text(line1, 5, 0)
        if line2:
            self.oled.text(line2, 5, 12)
        if line3:
            self.oled.text(line3, 5, 24)
        if line4:
            self.oled.text(line4, 5, 36)
        if line5:
            self.oled.text(line5, 5, 48)
        self.oled.show()

    def print_string_oled(self, string, start_x=5, start_y=5, max_len=15, line_spacing=10):
        x, y = start_x, start_y

        self.oled.fill(0)
        while string:
            chunk, string = string[:max_len], string[max_len:]
            self.oled.text(chunk, x, y)
            y += line_spacing
        self.oled.show()



class picobricks_neopixel:
    def __init__(self, neopixel_pin= 6):  
        self.neopixel = WS2812(neopixel_pin, brightness=0.4)
        self.neopixel.pixels_fill((0,0,0))
        self.neopixel.pixels_show()
        
    def set_neopixel(self, color, brightness):
        self.neopixel.pixels_fill(color)
        self.neopixel.brightness=brightness
        self.neopixel.pixels_show()
    
    def set_color(self, color):
        self.neopixel.pixels_fill(color)        
        self.neopixel.pixels_show()
        
    def set_brightness(self, brightness):
        self.neopixel.brightness=brightness
        self.neopixel.pixels_show()

class RGBController:
    def __init__(self):
        self.rgb_states = ['R', 'G', 'B']
        self.current_state_index = -1

    def cycle_rgb_state(self):
        # Get the current RGB state
        current_state = self.rgb_states[self.current_state_index]
        #print(f"RGB state changed to: {current_state}")

        # Increment the index for the next cycle
        self.current_state_index += 1

        # Reset the index if it exceeds the length of the rgb_states list
        if self.current_state_index >= len(self.rgb_states):
            self.current_state_index = 0
            
    def get_rgb_state(self):
        return self.rgb_states[self.current_state_index]

class picobricks_hum_temp:
    def __init__(self, humtemp_pin= 11, get_timer= 2):
        self.dht_sensor = DHT11(machine.Pin(humtemp_pin))
        self.get_timer= get_timer
        self.last_ticks= 0

    def get_value_once (self):
        self.dht_sensor.measure()
        temperature = self.dht_sensor.temperature()
        humidity = self.dht_sensor.humidity()
        
        print(f"Temperature: {temperature:.2f}")
        print(f"Humidity: {humidity:.2f}")
        return humidity, temperature
        
    def get_value (self):
        if ((time.time()-self.last_ticks) >self.get_timer):
            try:
                self.dht_sensor.measure()
                temperature = self.dht_sensor.temperature
                humidity = self.dht_sensor.humidity
                self.last_ticks= time.time()
                
                return humidity, temperature
            except OSError as e:
                print(e)
                print('dht_sensor Reading Failed')
                return -1, -1



class picobricks_potentiometer:
    def __init__(self, pot_pin=26, read_timer=1, min_val=0, max_val=100):
        self.pot = ADC(Pin(pot_pin))
        self.read_timer = read_timer
        self.last_ticks = 0
        self.min_val = min_val
        self.max_val = max_val

    def get_value_once(self):
        pot_value = self._read_potentiometer()
        mapped_value = int(self._map_value(pot_value))
        #print(f"Potentiometer Value: {mapped_value}")
        return mapped_value

    def get_value(self):
        if (time.time() - self.last_ticks) > self.read_timer:
            pot_value = self._read_potentiometer()
            mapped_value = int(self._map_value(pot_value))
            self.last_ticks = time.time()
            return mapped_value
        else:
            return None

    def _read_potentiometer(self):
        # Normalize the ADC reading (0-1 range) and scale it to 1-21 range
        return ((self.pot.read_u16() / 65535.0) * 20) + 1

    def _map_value(self, value):
        # Map the value from [1, 21] range to [self.min_val, self.max_val] range
        return ((value - 1) / (21 - 1)) * (self.max_val - self.min_val) + self.min_val


class picobricks_LDR:
    def __init__(self, ldr_pin=27, get_timer=5):
        self.ldr = machine.ADC(machine.Pin(ldr_pin))
        self.get_timer = get_timer
        self.last_ticks = time.time()  # use time.time() to initialize last_ticks

    def map_value(self, old_value, old_min=10000, old_max=2000, new_min=0, new_max=100):
        new_value = (old_value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min
        new_value = max(min(new_value, new_max), new_min)
        return int(new_value)

    def get_value_once(self):
        return self.map_value(self.ldr.read_u16())
            
    def get_value(self):
        if ((time.time()-self.last_ticks) >self.get_timer):
            self.last_ticks = time.time()
            return self.map_value(self.ldr.read_u16())
