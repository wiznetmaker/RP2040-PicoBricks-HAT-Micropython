import machine
import time
from picobricks_utils import picobricks_neopixel as _PB_neopixel
from picobricks_utils import picobricks_oled as _PB_oled
import picobricks_utils
import json
import time
import chatGPT


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
    #If it's warm and humid, you need bluish light, and if it's cold and dry, you need bluish light. 

    prompt= f"The current temperature is {temperature} degrees with {humidity}% humidity, and the brightness level is {ldr}%. Please provide me with the recommended RGB values and brightness level for the lighting based on the temperature. Also, include a lucky comment. The response format should be in JSON {{R:, G:, B:, bright:, comment:}}"
    return prompt

PB_neopixel= _PB_neopixel()
PB_oled= _PB_oled()

picobricks_utils.wiznet_init()

get_lamp_values_from_openai(70,30,20)
set_lamp_value()
time.sleep(3)

get_lamp_values_from_openai(50,20,80)
set_lamp_value()
time.sleep(3)

get_lamp_values_from_openai(30,10,90)
set_lamp_value()
time.sleep(3)

PB_neopixel.set_color((0,0,0))
PB_oled.deinit()