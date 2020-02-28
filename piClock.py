import sys
import datetime
import os,time
import board
import busio
import adafruit_is31fl3731
from loguru import logger

class Clock():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.display = adafruit_is31fl3731.Matrix(self.i2c)
        self.led_level = 255
        self.clear = lambda: os.system('clear')

        self.pos_dict = {}
        counter = 0
        for x in range(0,16):
            for y in range(0,9):
                self.pos_dict[counter] ={"x": x,"y":y}
                counter += 1
                self.display.pixel(x,y,127)
                time.sleep(.05)
        #test LEDs
        self.display.fill(255)
        time.sleep(.2)
        self.display.fill(0)
        self.previous_hour_led = 0 
        self.previous_min_led = 0




    #get the time and drive the led
    def tick(self):
        self.clear()
        now = datetime.datetime.now()
        led_a_level = int(round(self.led_level * (now.second/60),0))
        led_b_level = self.led_level - led_a_level
        hour = now.hour + 60
        minute = now.minute
        print(now.hour,now.minute, now.second," ",hour,minute)
        try:
            if hour > 72:
                hour = hour -12

            self.display.pixel(self.pos_dict[self.previous_hour_led]["x"],self.pos_dict[self.previous_hour_led]["y"],0) #turn off previous LED
            self.display.pixel(self.pos_dict[hour]["x"],self.pos_dict[hour]["y"],self.led_level) #displaying hour LED
            self.previous_hour_led = hour
                    
            self.display.pixel(self.pos_dict[self.previous_min_led]["x"],self.pos_dict[self.previous_min_led]["y"],0) #turn off previous minute LED
            self.display.pixel(self.pos_dict[minute]["x"],self.pos_dict[minute]["y"],led_b_level) #Current minute LED
            if minute < 59:
                self.display.pixel(self.pos_dict[minute+1]["x"],self.pos_dict[minute+1]["y"],led_a_level) #Next minute LED
            else:
                self.display.pixel(self.pos_dict[0]["x"],self.pos_dict[0]["y"],led_a_level) #Next minute LED
            self.previous_min_led = minute
            
            msg = "x:"+str(self.pos_dict[hour]["x"])+" y:"+str(self.pos_dict[hour]["y"])+"\n"
            msg += "x:"+str(self.pos_dict[minute]["x"])+" y:"+str(self.pos_dict[minute]["y"])+" lvl:"+str(led_b_level)+"\n"
            print(msg)
        except Exception as err:
            logger.exception(err)
    
    


clock = Clock()
while True:
    clock.tick()
    time.sleep(1)