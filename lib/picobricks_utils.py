from picobricks import SSD1306_I2C,WS2812, DHT11,NEC_16, IR_RX
from utime import sleep
import time
import machine
import network

OLED_WIDTH = 128
OLED_HEIGHT = 64

class picobricks_button:
    def __init__ (self, btn_pin= 10, detect_time_ms= 500):
        self.button = machine.Pin(btn_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.switch_state = False
        self.last_check = time.ticks_ms()

    def set_button_callback(self, on_callback=None, off_callback=None):
        self.on_callback = on_callback
        self.off_callback = off_callback
        
    def get_value(self):
        return self.button.value()
        
    def set_togle_button_state (self):  
        if (time.ticks_ms()-self.last_check) > 500:
            if self.get_value() == 1:  # Button is pressed
                self.switch_state = not self.switch_state  # Toggle the switch
                print(f'Switch is {"on" if self.switch_state else "off"}')
                if self.switch_state and self.on_callback:
                    self.on_callback()
                elif not self.switch_state and self.off_callback:
                    self.off_callback()
                
            self.last_check = time.ticks_ms()

class picobricks_oled:

    def __init__(self, sda_pin = 4, scl_pin = 5, i2c_ch= 0):
        sda=machine.Pin(sda_pin)
        scl=machine.Pin(scl_pin)
        i2c=machine.I2C(i2c_ch, sda=sda, scl=scl, freq=1000000)
        
        self.oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
        self.oled.text("Power On",30,0)
        self.oled.text("Waiting for ",20, 30)
        self.oled.text("Connection",23, 40)
        self.oled.show()
        time.sleep(1)

        self.oled.fill(0)
        
    def deinit(self):
        self.oled.fill(0)
        self.oled.show()
        
        
    def print_to_oled(self, string, start_x=5, start_y=5, max_len=15, line_spacing=10):
        x, y = start_x, start_y
        
        self.oled.fill(0)
        while string:
            chunk, string = string[:max_len], string[max_len:]
            self.oled.text(chunk,x, y)
            y += line_spacing
        self.oled.show()

class picobricks_neopixel:
    def __init__(self, neopixel_pin= 6):
    #define colors
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
    
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


def wiznet_init():
    spi = machine.SPI(0, 2_000_000, mosi=machine.Pin(19), miso=machine.Pin(16), sck=machine.Pin(18))
    nic = network.WIZNET5K(spi, machine.Pin(17), machine.Pin(20))   # spi, cs, reset pin
    #DHCP
    nic.active(True)

    while not nic.isconnected():
        time.sleep(1)
    print('IP address :', nic.ifconfig())        




