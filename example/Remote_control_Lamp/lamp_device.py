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
USERNAME = "umqtt_client"
BROKER_IP = "192.168.11.100"
DEVICE_IP = "192.168.11.101"
GATEWAY = "192.168.11.1"
NETMASK = "255.255.255.0"
DNS = "8.8.8.8"
SUB_TOPIC = "ctrl_state"
PUB_TOPIC = "chack_state"
KEEP_ALIVE = 60
SPI_BAUDRATE = 2000000
SPI_MOSI = 19
SPI_MISO = 16
SPI_SCK = 18
SPI_CS = 17
SPI_RST = 20

PB_OLED = _PB_oled()

mqtt = None

def update_oled_display(rgb=None, brightness=None):
    PB_OLED.print_line_oled(f"Color: {rgb}", f"Brightness:{brightness}%")
    
def wiznet_init():
    spi = machine.SPI(0, baudrate=SPI_BAUDRATE, mosi=machine.Pin(SPI_MOSI), miso=machine.Pin(SPI_MISO), sck=machine.Pin(SPI_SCK))
    nic = network.WIZNET5K(spi, machine.Pin(SPI_CS), machine.Pin(SPI_RST))
    nic.active(True)
    nic.ifconfig((DEVICE_IP, NETMASK, GATEWAY, DNS))

def mqtt_sub_callback(topic, msg):
    color_dict = {
    'R': (255, 0, 0),
    'G': (0, 255, 0),
    'B': (0, 0, 255)
    }
    print((topic, msg))
    try:
        # Check if msg is of type bytes and decode it
        if isinstance(msg, bytes):
            msg = msg.decode('utf-8')
        
        data = json.loads(msg)
        color = data.get("color", None)
        brightness = data.get("brightness", None)

        if color not in ["R", "G", "B"]:
            print("Invalid color value!")
            return
        if not 0 <= brightness <= 100:
            print("Invalid brightness value!")
            return

        neo.set_neopixel(color_dict[color], brightness/100)
        update_oled_display(color, brightness)

        print(f"Received color: {color}, brightness: {brightness}")
    except Exception as e:
        print(f"Error decoding JSON! Details: {e}")

def main():
    global mqtt

    wiznet_init()
    mqtt = WIZnet_MQTT.WIZnetMQTT(USERNAME, BROKER_IP, PUB_TOPIC, SUB_TOPIC, KEEP_ALIVE, mqtt_sub_callback)
    mqtt.init_mqtt()
    last_pub_time = time.time()
    get_timer= 1
    
    while True:
        mqtt.check_msg()
        time.sleep(0.1)  # A small sleep to avoid maxing out CPU usage
        
        if (time.time() - last_pub_time) > get_timer:
            mqtt.publish("check")
            last_pub_time = time.time()
        

if __name__ == "__main__":
    main()

