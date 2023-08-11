from picobricks_utils import picobricks_button as _PB_BTN
from picobricks_utils import picobricks_potentiometer as _PB_POT
from picobricks_utils import picobricks_oled as _PB_oled
from picobricks_utils import picobricks_neopixel
import picobricks_utils
import machine
import network
import time
import json
import WIZnet_MQTT

# Neopixel
neo = picobricks_neopixel()

# Constants for MQTT
USERNAME = "ctrl_umqtt_client"
BROKER_IP = "192.168.11.100"
DEVICE_IP = "192.168.11.102"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"
PUB_TOPIC = "ctrl_state"
SUB_TOPIC = "none"
KEEP_ALIVE = 60
SPI_BAUDRATE = 2000000
SPI_MOSI = 19
SPI_MISO = 16
SPI_SCK = 18
SPI_CS = 17
SPI_RST = 20

# Rest of your code from the first snippet
RGB_Ctrl = picobricks_utils.RGBController()
PB_BTN = _PB_BTN(mode="push")
PB_POT = _PB_POT()
PB_OLED = _PB_oled()
last_rgb = "R"
last_brightness = 0

mqtt = None

def push_callback_setRGB():
    global last_rgb, last_brightness
    RGB_Ctrl.cycle_rgb_state()
    cur_rgb = RGB_Ctrl.get_rgb_state()
    last_rgb = cur_rgb
    update_display_and_publish_message(cur_rgb, last_brightness)
    print(f"RGB: {cur_rgb}")

def button_push_main():
    if PB_BTN.set_toggle_button_state():
        push_callback_setRGB()

def pot_value_scaled():
    return PB_POT.get_value_once()

def generate_json_message(rgb=None, brightness=None):
    message = {
        "color": last_rgb,
        "brightness": last_brightness
    }
    return json.dumps(message).encode('utf-8')

def update_display_and_publish_message(rgb=None, brightness=None):
    # Update OLED display
    PB_OLED.print_line_oled(f"Color: {rgb}", f"Brightness:{brightness}%")
    
    # Generate JSON message and publish
    message = generate_json_message(rgb, brightness)
    mqtt.publish(message)

def wiznet_init():
    spi = machine.SPI(0, baudrate=SPI_BAUDRATE, mosi=machine.Pin(SPI_MOSI), miso=machine.Pin(SPI_MISO), sck=machine.Pin(SPI_SCK))
    nic = network.WIZNET5K(spi, machine.Pin(SPI_CS), machine.Pin(SPI_RST))
    nic.active(True)
    nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))


def combined_main():
    global last_brightness, mqtt
    PB_BTN.set_button_callback(push_callback=push_callback_setRGB)
    prev_rgb_value = RGB_Ctrl.get_rgb_state()
    prev_pot_value = None
    current_pot_value= 0
    last_pot_check = time.time()
    get_pot_timer = 0.1

    wiznet_init()
    mqtt = WIZnet_MQTT.WIZnetMQTT(USERNAME, BROKER_IP, PUB_TOPIC, SUB_TOPIC, KEEP_ALIVE, None)
    mqtt.init_mqtt()

    while True:
        # Check for button pushes
        button_push_main()

        # Check Potentiometer value
        if (time.time() - last_pot_check) > get_pot_timer:
            current_pot_value = pot_value_scaled()
            if current_pot_value != prev_pot_value:
                print(f"Brightness Value changed to: {current_pot_value}")
                update_display_and_publish_message(last_rgb, current_pot_value)
                prev_pot_value = current_pot_value
                last_brightness = current_pot_value
            last_pot_check = time.time()

        # Check MQTT messages
        mqtt.check_msg()
        time.sleep(0.1)  # A small sleep to avoid maxing out CPU usage

if __name__ == "__main__":
    combined_main()
