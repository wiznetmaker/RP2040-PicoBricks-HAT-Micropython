from machine import Pin,SPI,PWM,ADC

from picobricks import SSD1306_I2C,WS2812, DHT11,NEC_16, IR_RX
from picobricks_utils import picobricks_oled as _PB_oled
from picobricks_utils import picobricks_neopixel as _PB_neopixel
from picobricks_utils import picobricks_hum_temp as _PB_HumTemp
from picobricks_utils import picobricks_LDR as _PB_LDR
from picobricks_utils import picobricks_button as _PB_BTN

import picobricks_utils as PB
import dht 
import json
import time
import chatGPT

PB_oled= _PB_oled()
PB_neopixel= _PB_neopixel()
PB_HumTemp= _PB_HumTemp()
PB_LDR= _PB_LDR(get_timer=1)
PB_BTN= _PB_BTN()

PB_Lamp_R=None
PB_Lamp_G=None
PB_Lamp_B=None
PB_Lamp_bright=None
PB_Lamp_comment=None

dht_sensor = dht.DHT11(Pin(11))

def main():
    PB.wiznet_init() 
    PB_BTN.set_button_callback(on_callback= turn_on_AI_Lamp, off_callback=deinit_device)
    
    print("start")
    while True:
        PB_BTN.set_togle_button_state()
        
def get_environmental_data():

    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    ldr= PB_LDR.get_value_once()
    
    print(f"Temperature: {temperature:.2f}")
    print(f"Humidity: {humidity:.2f}")
    print(f"LDR: {ldr}")
    
    return humidity, temperature, ldr

def deinit_device():
    PB_Lamp_R=None
    PB_Lamp_G=None
    PB_Lamp_B=None
    PB_Lamp_bright=None
    
    PB_neopixel.set_color((0,0,0))
    
    PB_oled.deinit()

def turn_on_AI_Lamp():
    humidity, temperature, ldr= get_environmental_data()
    get_lamp_values_from_openai(humidity, temperature, ldr)
    set_lamp_value()
    
    
def set_lamp_value():
    PB_neopixel.set_color((PB_Lamp_R, PB_Lamp_G,PB_Lamp_B))
    PB_neopixel.set_brightness(PB_Lamp_bright/100)    
    PB_oled.print_to_oled(string=PB_Lamp_comment)
    print(f"json value: RGB({PB_Lamp_R},{PB_Lamp_G},{PB_Lamp_B}), bright ({PB_Lamp_bright/100}), comment({PB_Lamp_comment})")

def get_lamp_values_from_openai(humidity, temperature, ldr):
    PB_oled.print_to_oled(string="Wait OpenAI message")
    
    prompt= create_AI_Lamp_prompt(humidity, temperature, ldr)
    print(f"prompt: \"{prompt}\"")
    response= chatGPT.send_prompt_to_chatGPT(prompt)
    print(f"chatGPT: \"{response}\"")
    
    start = response.find('{')
    end = response.rfind('}') + 1
    json_string = response[start:end]

    response_dict = json.loads(json_string)

    if response_dict is not None:
        for key, value in response_dict.items():
            globals()[f"PB_Lamp_{key}"] = value    

def create_AI_Lamp_prompt(humidity, temperature, ldr):
    prompt= f"The current temperature is {temperature} degrees with {humidity}% humidity, and the brightness level is {ldr}%. Please provide me with the recommended RGB values and brightness level for the lighting based on the temperature. Also, include a lucky comment. The response format should be in JSON {{R:, G:, B:, bright:, comment:}}"
    return prompt


if __name__ == "__main__":
    main()
