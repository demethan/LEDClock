import sys
import datetime
import os,time
import board
import busio
import adafruit_is31fl3731
from loguru import logger
import RPi.GPIO as GPIO
import time

class Clock():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.display = adafruit_is31fl3731.Matrix(self.i2c)
        #self.led_level = 255
        GPIO.setmode(GPIO.BCM) #for light sensor
        self.a_pin = 18
        self.b_pin = 23


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


    # create discharge function for reading capacitor data
    def discharge(self):
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(0.005)

    # create time function for capturing analog count value
    def charge_time(self):
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)
        count = 0
        GPIO.output(self.a_pin, True)
        while not GPIO.input(self.b_pin):
            count = count +1
        return count

    # create analog read function for reading charging and discharging data
    def analog_read(self):
        self.discharge()
        return self.charge_time()

    def light(self, pos, level):
        self.display.pixel(self.pos_dict[pos]["x"],self.pos_dict[pos]["y"],level) #clock side A
        pos = pos + 72
        self.display.pixel(self.pos_dict[pos]["x"],self.pos_dict[pos]["y"],level) #Clock sido B

    def animate(self):
        self.light(0,255)
        for x in range(0,60):   #address the LED matrix to a int. 0={0,0},1={0,1}, etc
            self.light(x,0)
            time.sleep(.0166)


    #get the time and drive the led
    def tick(self):
        #self.clear()
        ambiant_light = self.analog_read()
        led_level = int(round(((500 - ambiant_light)/450*255),0))
        if led_level > 255: 
            led_level = 255 #day mode
        if led_level < 25:
            led_level = 25 #night mode
        now = datetime.datetime.now()
        #led_a_level = int(round(led_level * (now.second/60),0))
        #led_b_level = led_level - led_a_level
        if now.hour >= 12:
            offset = 48 #convert 24h to 12
        else:
            offset = 60
        hour = now.hour + offset #offset for the led matrix, don't want to overlap minute's LEDs (minute LED 0-59, Hour LED 60-71).
        minute = now.minute
        second = now.second
        
        try:
            #minutes        
            #Light minut and keep minute lit
            if minute < 59:
                self.light(minute,led_level) #Light minute and
                #hour
                
                

            else: 
                if second < 59:
                    self.light(minute,led_level) #Light minute and
                    self.light(0,0) #turn off minute at 12 mark for readability. 
                    #hour
                    self.light(hour,led_level) #displaying hour LED

                else:#reset LED for next our.
                    self.animate()
                    self.light(0,led_level) #minute LED
                    hour = now.hour + offset
                    self.light(hour,led_level) #hour led
                    
                    
            #print(hour)
            if(hour==60):
                self.light(71,0) # when converting from 24h to 12h. need to turn off previous
            else:
                self.light(hour-1,0) #previous hour
            self.light(hour,led_level) #displaying hour LED
                
            
        except KeyboardInterrupt:
            self.display.fill(0)
        
        except Exception as err:
            logger.exception(err)



clock = Clock()
while True:
    clock.tick()
    time.sleep(0.2)