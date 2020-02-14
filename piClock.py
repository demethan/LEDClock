import sys
from tkinter import *
import datetime
import time
import board
import busio
import adafruit_is31fl3731

i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_is31fl3731.Matrix(i2c)
led_level = 255

pos_dict = {}
counter = 1
for x in range(1,9):
    for y in range(1,16):
        pos_dict[counter] ={"x": x,"y":y}
        counter += 1
 

#get the time and drive the led
def tick():
    now = datetime.datetime.now()
    led_a_level = round(led_level * (now.second/60),0)
    led_b_level = led_level - led_a_level
    hour = now.hour +60
    minute = now.minute
    
    display.pixel(pos_dict[hour]["x"],pos_dict[hour]["y"],led_level) #displaying hour
    if minute < 59:
        display.pixel(pos_dict[minute]["x"],pos_dict[minute]["y"],led_a_level)
        display.pixel(pos_dict[minute+1]["x"],pos_dict[minute+1]["y"],led_b_level)
    else
        display.pixel(pos_dict[minute]["x"],pos_dict[minute]["y"],led_a_level)
        display.pixel(pos_dict[minute-59]["x"],pos_dict[minute-59]["y"],led_b_level)




while true:
    tick()
    time.sleep(1)