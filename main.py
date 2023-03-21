# Import
from machine import ADC, I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from time import sleep

# Variables
relay_pin = Pin(4, Pin.OUT)
soil_pin = ADC(Pin(26))
moistureReading = soil_pin.read_u16()

# LDC Screen Setup
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    
# Welcome Message
def welcomeMessage():
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Moisture Measure')
    lcd.move_to(1,1)
    lcd.putstr('System Loading')
    sleep(5)
    
# First Reading
def initalReading():
    moistureReading = soil_pin.read_u16()
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Moisture Level')
    lcd.move_to(0,1)
    lcd.putstr('Units: ')
    lcd.putstr(str(moistureReading))
    sleep(5)

# Start Program
relay_pin.value(0)
welcomeMessage()
initalReading()

while True:
    lcd.clear()
    moistureReading = soil_pin.read_u16()
    if moistureReading < 15000:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr('Moisture Low')
        lcd.move_to(0,1)
        lcd.putstr(str(moistureReading))
        sleep(3)
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr('Watering...')
        relay_pin.value(1)
        sleep(5)
    else:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr('Levels Optimal')
        lcd.move_to(0,1)
        lcd.putstr(str(moistureReading))
        relay_pin.value(0)
        sleep(5)
    
    
