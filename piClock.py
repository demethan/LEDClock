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
        #self.clear = lambda: os.system('clear') 

        self.pos_dict = {}
        counter = 0
        for x in range(0,16):   #address the LED matrix to a int. 0={0,0},1={0,1}, etc
            for y in range(0,9):
                self.pos_dict[counter] ={"x": x,"y":y}
                counter += 1
                self.display.pixel(x,y,127) #turn on LED at that possition. 
                time.sleep(.01)
        #test LEDs
        self.display.fill(255)
        time.sleep(.2)
        self.display.fill(0)
        self.previous_hour_led = 0 
        self.previous_min_led = 0




    #get the time and drive the led
    def tick(self):
        #elf.clear()
        now = datetime.datetime.now()
        led_a_level = int(round(self.led_level * (now.second/60),0))
        led_b_level = self.led_level - led_a_level
        if now.hour >= 12:
            offset = 48 #convert 24h to 12
        else:
            offset = 60
        hour = now.hour + offset #offset for the led matrix, don't want to overlap minute's LEDs (minute LED 0-59, Hour LED 60-71).
        minute = now.minute
        #print(now.hour,now.minute, now.second," ",hour,minute) #for debug
        
        try:
            self.light(self.previous_hour_led,0) #turn off previous LED
            self.light(hour,self.led_level) #displaying hour LED
            self.previous_hour_led = hour
                    
            self.light(self.previous_min_led,0) #turn off previous minute LED
            self.light(minute,led_b_level) #Current minute LED
            if minute < 59:
                self.light(minute+1,led_a_level) #Next minute LED
            else:
                self.light(0,led_a_level) #Next minute LED
            self.previous_min_led = minute
            
            """ msg = "x:"+str(self.pos_dict[hour]["x"])+" y:"+str(self.pos_dict[hour]["y"])+"\n"
            msg += "x:"+str(self.pos_dict[minute]["x"])+" y:"+str(self.pos_dict[minute]["y"])+" lvl:"+str(led_b_level)+"\n"
            print(msg) #debug """
        except Exception as err:
            logger.exception(err)
    
    def light(self, pos, level):
        self.display.pixel(self.pos_dict[pos]["x"],self.pos_dict[pos]["y"],level) #clock side A
        pos = pos + 72
        self.display.pixel(self.pos_dict[pos]["x"],self.pos_dict[pos]["y"],level) #Clock sido B


clock = Clock()
while True:
    clock.tick()
    time.sleep(1)