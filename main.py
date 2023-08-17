#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd2in7
import getopt, sys
import RPi.GPIO as GPIO
import PIL
import random
import time
import traceback
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont

text = 'hello world'
width = len(text) * 6
height = 8
reset = False
bgcolor = 1 # black or white
showDate = True
showStart = False

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
options = "r"

# Long options
long_options = ["reset"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-r", "--reset"):
            reset = True
            print ("resetting")

except getopt.error as err:
    print (str(err))

GPIO.setmode(GPIO.BCM)

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def interrupt(channel):
    global reset
    global bgcolor
    if channel == key1:
        reset = True
        bgcolor = 1
    elif channel == key2:
        reset = True
        bgcolor = 0
    elif channel == key3:
        global showDate
        showDate = not showDate
    elif channel == key4:
        global showStart
        showStart = not showStart


GPIO.add_event_detect(key1, GPIO.FALLING, callback=interrupt, bouncetime=200)
GPIO.add_event_detect(key2, GPIO.FALLING, callback=interrupt, bouncetime=200)
GPIO.add_event_detect(key3, GPIO.FALLING, callback=interrupt, bouncetime=200)
GPIO.add_event_detect(key4, GPIO.FALLING, callback=interrupt, bouncetime=200)


try:
    epd = epd2in7.EPD()
    epd.init()
    epd.Clear(0xFF)
    
    while True:
        current_date_time = datetime.now().strftime("%Y/%m/%d, %H:%M")

        if reset:
            color = '1'
            if bgcolor == 0:
                color = '0'
            lImage = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), bgcolor)  # 255: clear the frame
            reset = False
        else: 
            lImage = Image.open('temp.bmp')

        draw = ImageDraw.Draw(lImage)

        draw.text((random.randint(0,epd2in7.EPD_WIDTH), random.randint(0,epd2in7.EPD_HEIGHT)), text, fill = random.randint(0,1))

        c = 0
        for x in range(epd2in7.EPD_WIDTH):
            for y in range (epd2in7.EPD_HEIGHT):
                c += lImage.getpixel((x,y))

        back = 1
        front = 0
        # average color light or dark, invert date
        if c < 255 * epd2in7.EPD_WIDTH*epd2in7.EPD_HEIGHT/2:
            back = 0
            front = 1

        if showStart:
            draw.rectangle((0, 0, width+2, height+2), fill = back)
            draw.text((2, 0), text, fill = front)

        if showDate:
            timeX = epd2in7.EPD_WIDTH-142
            timeY = epd2in7.EPD_HEIGHT-20
            draw.rectangle((timeX, timeY, timeX+102, timeY+10), fill = back)
            draw.text((timeX, timeY), current_date_time, fill = front)
        
        lImage.save("temp.bmp", format="bmp")
    
        hImage = Image.open('temp.bmp')
        epd.display(epd.getbuffer(hImage))
        time.sleep(10)
    
except:
    print('traceback.format_exc():\n%s',traceback.format_exc())
    exit()

