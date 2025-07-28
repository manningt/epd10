#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

import logging
import epd10in2g
import time
import datetime
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13g Demo")

    epd = epd10in2g.EPD()
    if 1:
        logging.info("init")
        epd.init()
    if 0:
        logging.info("Clear")
        epd.Clear()

    # font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
    # font40 = ImageFont.truetype('Font.ttc', 40)
    
    start_time = datetime.datetime.now()
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    font180 = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf', 180)
    msg = "Closed"
    w = font180.getlength(msg)
    draw.text(((epd.width-w)/2, 0), msg, font = font180, fill = epd.RED)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    # logging.info(f"Time taken to draw text: {elapsed_time.seconds} seconds {elapsed_time.microseconds} microseconds")

    # draw.line((5, 170, 80, 245), fill = epd.RED)
    # draw.line((80, 170, 5, 245), fill = epd.YELLOW)
    # draw.rectangle((5, 170, 80, 245), outline = epd.BLACK)
    # draw.rectangle((90, 170, 165, 245), fill = epd.YELLOW)
    # draw.arc((5, 250, 80, 325), 0, 360, fill = epd.BLACK)
    # draw.chord((90, 250, 165, 325), 0, 360, fill = epd.RED)

    start_time = datetime.datetime.now()
    buf = epd.getbuffer(Himage)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    # logging.info(f"Time taken to getbuffer: {elapsed_time.seconds} seconds {elapsed_time.microseconds} microseconds")

    start_time = datetime.datetime.now()
    logging.info("Before display image")
    epd.display(buf)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Time taken to display: {elapsed_time.seconds} seconds {elapsed_time.microseconds} microseconds")
    
    '''
    logging.info("2.read bmp file")
    Himage = Image.open(os.path.join(picdir, '10in2g.bmp'))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)
 
    logging.info("Clear...")
    epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
   '''
    logging.info("Ending without Clear & Sleep.")
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd10in2g.epdconfig.module_exit(cleanup=True)
    exit()
