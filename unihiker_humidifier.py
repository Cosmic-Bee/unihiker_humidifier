import time
import requests
from unihiker import GUI
from pinpong.board import Board, I2C, Pin, NeoPixel
from pinpong.extension.unihiker import *
from pinpong.libs.dfrobot_sht31 import SHT31

LIGHT_ENABLE_THRESHOLD = 300

# API User and password, set via ESPHome
BASIC_USERNAME = 'BASIC_USER'
BASIC_PASSWORD = 'BASIC_PASS'

# You'll need to provide the IP address of your ESPHome
# device on your local network. Giving it a static IP is
# helpful here.
BASE_URL = "http://192.168.2.103"

# These endpoints are provided by ESPHome
# https://esphome.io/web-api/index.html
HUMIDIFIER_ON_PATH = "/switch/humidifier/turn_on"
HUMIDIFIER_OFF_PATH = "/switch/humidifier/turn_off"
SENSOR_HUMIDITY_PATH = "/sensor/xiao_humidity"

# An example response from the sensor:
# {"id":"sensor-xiao_humidity","value":49,"state":"49 %"}

Board("UNIHIKER").begin()

# Pin 22 is the pinbeing used to control the LEDs
NEOPIXEL_PIN = Pin(22)
PIXELS_NUM = 8
neopixel = NeoPixel(NEOPIXEL_PIN, PIXELS_NUM)

# Initialize GUI
gui = GUI()
lightEnabled = None

# Page header
gui.draw_text(text="Humidifier", x=45, y=15, font_size=25, color="teal")

# Initialize sensor
sensor = SHT31(i2c_addr=0x44)

# Initial set point for humidity
humidity_set_point = 50

# Draw initial values on GUI
current_state = gui.draw_text(text="OFF", x=20, y=70, font_size=9, color="teal")

gui.draw_text(text="Xiao Humidity", x=20, y=170, font_size=9, color="teal")
gui.draw_text(text="Device Humidity and Temperature", x=20, y=290, font_size=9, color="teal")

# These draw the humidity and temperature text on the screen
# That text is then updated during the program loop
humidity_text = gui.draw_digit(x=180, y=140, text=str(humidity_set_point), origin="center", color="blue", font_size=50)
current_humidity_text = gui.draw_digit(x=50, y=140, text="0", origin="center", color="blue", font_size=50)
unihiker_humidity_text = gui.draw_digit(x=50, y=260, text="0", origin="center", color="red", font_size=40)
unihiker_temperature_text = gui.draw_digit(x=180, y=260, text="0F", origin="center", color="red", font_size=40)

def handleNightMode():
    global lightEnabled
    lightValue = light.read()
    if 0 <= lightValue < LIGHT_ENABLE_THRESHOLD:
        lightEnabled = True
        for i in range(PIXELS_NUM):
            neopixel[i] = (20, 20, 20)
    elif lightEnabled:
        lightEnabled = False
        for i in range(PIXELS_NUM):
            neopixel[i] = (0, 0, 0)

def increase_humidity_set_point():
    global humidity_set_point
    humidity_set_point = min(100, humidity_set_point + 1)
    humidity_text.config(text=str(humidity_set_point))

def decrease_humidity_set_point():
    global humidity_set_point
    humidity_set_point = max(0, humidity_set_point - 1)
    humidity_text.config(text=str(humidity_set_point))

def get_current_humidity():
    response = requests.get(f"{BASE_URL}{SENSOR_HUMIDITY_PATH}", auth=(BASIC_USERNAME, BASIC_PASSWORD))
    data = response.json()
    return data["value"]

def set_humidifier_state(state):
    url = f"{BASE_URL}{HUMIDIFIER_ON_PATH}" if state else f"{BASE_URL}{HUMIDIFIER_OFF_PATH}"
    requests.post(url, auth=(BASIC_USERNAME, BASIC_PASSWORD))

# Add up and down buttons for humidity set point adjustment
gui.add_button(x=180, y=80, w=50, h=30, text="Up", origin='center', onclick=increase_humidity_set_point)
gui.add_button(x=180, y=190, w=50, h=30, text="Down", origin='center', onclick=decrease_humidity_set_point)

humidifier_enabled = False

while True:
    handleNightMode()

    xiao_humidity = get_current_humidity()
    current_temperature = int(sensor.temp_f())
    current_humidity = int(sensor.humidity())

    current_humidity_text.config(text=str(xiao_humidity))
    unihiker_humidity_text.config(text=str(current_humidity))
    unihiker_temperature_text.config(text=f"{current_temperature}F")

    if button_a.is_pressed():
        current_state.config(text="ON")
        humidifier_enabled = True
    elif button_b.is_pressed():
        current_state.config(text="OFF")
        humidifier_enabled = False
        set_humidifier_state(False)

    if humidifier_enabled:
        if xiao_humidity < humidity_set_point:
            set_humidifier_state(True)
        else:
            set_humidifier_state(False)

    time.sleep(0.1)
