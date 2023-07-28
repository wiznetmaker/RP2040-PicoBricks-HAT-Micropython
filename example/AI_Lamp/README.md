

When you press the button, AI Lamp measures temperature, humidity, and ambient light to turn on with the recommended lighting color and brightness suggested by ChatGPT. Additionally, it displays messages of good fortune on its OLED screen.

----


While there are many lamps available with adjustable colors and brightness, users often struggle with color selection, leading them to stick to fixed colors or default settings. This can leave one feeling regretful about not fully utilizing the lamp's functionalities.

By harnessing the power of Pico and ChatGPT, AI Lamp automatically adjusts its colors and brightness to perfectly match your environment, enabling a smarter and more efficient use of the lamp. Through this integration of Pico and ChatGPT, the lamp can be used even more intelligently, automatically adapting its colors and brightness to suit the user's environment.

# HW Configuration

## Pico + WIZnet Ethernet Hat (or W5100S-EVB-Pico)
This is a wired Ethernet module that can be used with Pico.
Please attach the pin header to connect PICO + WIZnet Ethernet HAT + Pico Bricks."

 
If you find this configuration inconvenient, please use W5100S-EVB-Pico.
Product:
Pico: https://www.raspberrypi.com/products/raspberry-pi-pico/ 
WIZnet Ethernet HAT: https://eshop.wiznet.io/shop/module/wiznet-ethernet-hat/ 
W5100S-EVB-Pico: https://eshop.wiznet.io/shop/module/w5100s-evb-pico/

 
## Pico Bricks
The modules to be used are RGB LED, OLED, Temp&Hum sensor, LDR, and Button.
>OLED: SSD1306_I2C/ RGB Ramp: WS2812/ Temp& Hum: DHT11/ LDR: NORP12
Data sheets: https://docs.picobricks.com/en/latest/datasheet.html

With Pico Bricks, module integration is possible without the need for separate wiring.
 

 
# SW Configuration

## Firmware Configuration
This is the firmware required for using OpenAI. Make sure to use the following version
>open_ai_w5100_evb_pico_fw_v1.19.1.uf2

Downloading the firmware follows the same steps as setting up other MicroPython device..
If you find it difficult, you can refer to this YouTube video for assistance:
>WIZnet Pico Board How to Program WIZnet Pico board using MicroPython
https://www.youtube.com/watch?v=8FcFhZRNNxE

## Code Writing
### Network
Since DHCP is used, there is no need to input IP or other settings. Just call the *wiznet_init()* function in ***lib/WIZnet_utils.py***
If you are using a different SPI from the default configuration, please modify the settings for mosi, miso, sck, spi CS, and Ethernet chip reset in the wiznet_init() function as follows:

```python
spi = machine.SPI(0, 2_000_000, mosi=machine.Pin(19), miso=machine.Pin(16), sck=machine.Pin(18))
nic = network.WIZNET5K(spi, machine.Pin(17), machine.Pin(20))
```

### OpenAI
The communication with OpenAI is written in the ***lib/chatGPT.py*** module.
Create an API Key and insert it into the following code in *chatGPT.py* file:
> Get OpenAI API Key: https://platform.openai.com/account/api-keys
 
```python
api_key = "Insert your API Key"
```
For instructions on how to interact with ChatGPT using the WIZnet Pico board and MicroPython, you can refer to this YouTube video

> How to interact with ChatGPT using WIZnet Pico board and MicroPython.
https://www.youtube.com/watch?v=QUTDCNpLAoY&t=7s

The code for sending prompts is written next step!
 
### Modules Basic Code
The control logic for the Pico Bricks module is written based on the official provided library *picobricks.py* and is included in *picobricks_utils.py*

If you are using Pico Bricks, you can use it without any additional GPIO settings.
 
However, if you are using other modules, please input the GPIO values in the initialization functions of each module accordingly.

**Example**
```python
from picobricks_utils import picobricks_neopixel as _PB_neopixel
PB_neopixel= _PB_neopixel(neopixel_pin= 6)
```

**- Button**
 
***lib/picobricks_utils.py/ class picobricks_button***

```python
from picobricks_utils import picobricks_button as _PB_BTN
PB_BTN= _PB_BTN()
```

If you want to change the current button detect time, please input the new detect_time_ms
```python
PB_BTN= _PB_BTN(detect_time_ms= 500)
```

And upon receiving the input signal for the button, you can set the callback function to be executed
```python
PB_BTN.set_button_callback(on_callback= turn_on_AI_Lamp, off_callback=deinit_device)
```
The button is used in a toggle format, not a push format.
Add logic to set the button state in the actual operation's 'while' loop.
Detect button inputs and execute the callback accordingly.
```python
while True:
        PB_BTN.set_togle_button_state()
```

---
**- Temperature and Humidity**

The DHT11 module seems to have a problem with reading pulses correctly when executing code written in lib (library).
It appears that the problem is related to the ADC read timing.
As a solution, the PB_HumTemp module in *picobricks_utils.py* is not used.
Instead, the DHT11 module is directly called and used in the main file.

```python
# Class Init 
dht_sensor = dht.DHT11(Pin(11))
# Measure Temp& Hum
dht_sensor.measure()
temperature = dht_sensor.temperature()
humidity = dht_sensor.humidity()
```
---

**- LDR**
 
***lib/picobricks_utils.py/ class picobricks_LDR***
```python
from picobricks_utils import picobricks_LDR as _PB_LDR
PB_LDR= _PB_LDR()
```
The light intensity measurement returns values between **2000 and 10000**. If you use the *get_value_once()* function, it will convert this value into a percentage. 
If you want to change the range, please use the following code

```python
old_value= PB_LDR.ldr.read_u16()
PB_LDR.map_value( old_value, old_min=10000, old_max=2000, new_min=0, new_max=100):
```
---

**- RGB LED(Lamp)**
 
***lib/picobricks_utils.py/ class picobricks_neopixel***
```python
from picobricks_utils import picobricks_neopixel as _PB_neopixel
PB_neopixel= _PB_neopixel()
```
You can input the desired RGB values and brightness level to adjust the color. 
For brightness, it should be adjusted within the range of 0.01 to 1.
```python 
PB_neopixel.set_neopixel((PB_Lamp_R, PB_Lamp_G,PB_Lamp_B), PB_Lamp_bright/100)
```
---

**- OLED**
 
***lib/picobricks_utils.py/ class picobricks_oled***
```python
from picobricks_utils import picobricks_oled as _PB_oled
PB_oled= _PB_oled()
```
By default, the text starts from position x=5, y=5, and displays a line of 10 characters.

```python
PB_oled.print_to_oled(string= “Insert text”)
```
To change the text output position or modify the characters displayed in a line, you can input parameters into the function.

```python
PB_oled.print_to_oled(string= “Insert text”, start_x=5, start_y=5, max_len=15, line_spacing=10)
```
To print multiple lines, please use the following functions.
```python
PB_oled.oled.fill(0)
PB_oled.oled.text("Line 1",5, 5)
PB_oled.oled.text("Line 2",5, 10)
PB_oled.oled.show()
```

Up to this point, we have covered the basic operations of the modules.
Now, let's proceed to control Smart Lamp!!

---

### Smart Lamp Control

The operational scenario is as follows
**Press the button (On) -> Measure temperature and humidity -> Request Lamp value to OpenAI -> Set Lamp -> Press the button (Off) -> Reset**

**- Button On**
This is the callback function for the button when it's turned on.
```python
# on_callback= turn_on_AI_Lamp
def turn_on_AI_Lamp():
    # measure humidity and temperature
    humidity, temperature, ldr= get_environmental_data()
    # Request Lamp value to OpenAI
    get_lamp_values_from_openai(humidity, temperature, ldr)
    # Set lamp RGB value
    set_lamp_value()
```
The temperature and humidity information are obtained using functions from *picobricks_utils.py*. Each sensor's value is received as a return value.

```python
def get_environmental_data():
    dht_sensor.measure()
    
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    ldr= PB_LDR.get_value_once()
    
    return humidity, temperature, ldr
```

Based on the provided values of temperature, humidity, and light intensity, we construct a prompt string to request the LAMP RGB color and brightness values, as well as a lucky message

If you have any other specific requests, modify the prompt accordingly.

```python 
def create_AI_Lamp_prompt(humidity, temperature, ldr):
	prompt= f"The current temperature is {temperature} degrees with {humidity}% humidity, and the brightness level is {ldr}%. Please provide me with the recommended RGB values and brightness level for the lighting based on the temperature. Also, include a lucky comment. The response format should be in JSON {{R:, G:, B:, bright:, comment:}}"
	return prompt
```

After sending the constructed prompt to OpenAI, the response content is parsed.
In some cases, the response may contain strings other than JSON. 
We will extract only the JSON content.

```python
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

```

---

**- Lamp Turn on**

After analyzing the parsed RGB and light intensity values, we set the Lamp accordingly and display the lucky message on the OLED screen.
```python
def set_lamp_value():
    PB_neopixel.set_color((PB_Lamp_R, PB_Lamp_G,PB_Lamp_B))
    PB_neopixel.set_brightness(PB_Lamp_bright/100)    
    PB_oled.print_to_oled(string=PB_Lamp_comment)
```

## Demonstrate

At a temperature of **27 degrees Celsius and 70% humidity**, OpenAI recommends using colors in the red spectrum.
 
OpenAI tends to recommend similar colors when there is a small temperature difference.
You have created a test program that uses dummy values to set the temperature and humidity and input Lamp values.


***example/AI_Lamp/test.py***

```python
get_lamp_values_from_openai(70,30,20)
set_lamp_value()
time.sleep(3)

get_lamp_values_from_openai(50,20,80)
set_lamp_value()
time.sleep(3)

get_lamp_values_from_openai(30,10,90)
set_lamp_value()
time.sleep(3)
```

In **hot and humid** environments, the **R value** tends to be higher, 
while in **cold and dry** environments, the **B value** tends to be higher.
I've noticed that there are many repeated phrases in the [short lucky message]. 
You can customize this part with the desired phrases.

Although I used Pico Bricks' RGB LED, nowadays there are many lamps available that can be controlled through Bluetooth or Wi-Fi. Many of them are open source, so if you integrate them, you can turn your existing lamps into Smart Lamps.

I might try that in my next project!
See you in the next project!
