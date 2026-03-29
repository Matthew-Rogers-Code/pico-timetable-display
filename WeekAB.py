import time
import urtc
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
switch = Pin(28, Pin.IN, Pin.PULL_DOWN)

# Initialize RTC (connected to I2C)
i2c = I2C(1, scl=Pin(3), sda=Pin(2))
rtc = urtc.DS3231(i2c)
SDA = 0
SCL = 1
I2C_BUS = 0
LCD_ADDR = 0x27
LCD_NUM_ROWS = 2
LCD_NUM_COLS = 16
lcdi2c = I2C(I2C_BUS, sda=machine.Pin(SDA), scl=machine.Pin(SCL), freq=400000)
lcd = I2cLcd(lcdi2c, LCD_ADDR, LCD_NUM_ROWS, LCD_NUM_COLS)

# Set the current time using a specified time tuple
# Time tuple: (year, month, day, day of week, hour, minute, seconds, milliseconds)
#initial_time = (2026, 7, 28, 1, 16, 30, 0, 0)

# Or get the local time from the system
initial_time_tuple = time.localtime()  # tuple (microPython)
initial_time_seconds = time.mktime(initial_time_tuple)  # local time in seconds

# Convert to tuple compatible with the library
initial_time = urtc.seconds2tuple(initial_time_seconds)

# Sync the RTC
rtc.datetime(initial_time)

dictionary = {}
with open('data.txt', 'r') as file:
    for line in file:
        if ':' in line:
            key, value = line.strip().split(':', 1)
            dictionary[key.strip()] = value.strip()

while True:
    current_datetime = rtc.datetime()
    temperature = rtc.get_temperature()
        
    if switch.value() == 1:
        display_hour = (current_datetime.hour + 1) % 24
    else:
        display_hour = current_datetime.hour

    # Display time details
    #print('Current date and time:')
    #print('Year:', current_datetime.year)
    #print('Month:', current_datetime.month)
    #print('Day:', current_datetime.day)
    #print('Hour:', current_datetime.hour)
    #print('Minute:', current_datetime.minute)
    #print('Second:', current_datetime.second)
    #print('Day of the Week:', days_of_week[current_datetime.weekday])
    #print(f"Current temperature: {temperature}°C")    
    # Format the date and time
    day_output = current_datetime.day-current_datetime.weekday
    current_date = (f"{current_datetime.year:04d}-{current_datetime.month:02d}-{day_output:02d}")
    try:
        output = dictionary[current_date]
    except:
        output = "?"
    formatted_datetime = f"{current_datetime.day:02d}-{current_datetime.month:02d}-{current_datetime.year:04d} {temperature:04.1f}C{display_hour:02d}:{current_datetime.minute:02d}:{current_datetime.second:02d}  Week {output}"
    lcd.putstr(f"{formatted_datetime}")
    if display_hour < 7 or display_hour > 16:
        lcd.backlight_off()
    else:
        lcd.backlight_on()
    time.sleep(1)
    
    
