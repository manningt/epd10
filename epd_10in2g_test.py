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

FONT_ITALIC_PATH = '/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf'
FONT_NORMAL_PATH = '/usr/share/fonts/truetype/piboto/Piboto-BoldItalic.ttf'

def find_font_fit(msg):
    fontsize = 9  # starting font size

    font = ImageFont.truetype(FONT_NORMAL_PATH, fontsize)
    while font.getlength(msg) < (epd.width-40):  
        fontsize += 1 # iterate until the text size is just larger than the criteria
        font = ImageFont.truetype(FONT_NORMAL_PATH, fontsize)

    fontsize -= 1 # optionally de-increment to be sure it is less than criteria

    # logging.info(f"final font size= {fontsize} for '{msg}'")
    return fontsize


try:
    epd = epd10in2g.EPD()
    if 1:
        logging.info("init")
        epd.init()
    if 0:
        logging.info("Clear")
        epd.Clear()

    closed = True
    if closed:
        top_fill_color = epd.RED
        top_text_color = epd.WHITE
    else:
        top_fill_color = epd.YELLOW
        top_text_color = epd.BLACK

    # bottom half is always black with white text; width is 960, height is 640

    start_time = datetime.datetime.now()
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    # top half is a pie-slice (start and end angles are from 3 o'clock), bottom half is black
    shape = [(0, 0), (epd.width, epd.height)]
    draw.pieslice(shape, start = 180, end = 0, fill = top_fill_color)
    draw.rectangle(((0, epd.height/2), (epd.width, epd.height)), fill = epd.BLACK)

    font180 = ImageFont.truetype(FONT_ITALIC_PATH, 180)
    msg = "Closed"
    w = font180.getlength(msg)
    draw.text(((epd.width-w)/2, 60), msg, font = font180, fill = top_text_color)

    msg_lines = ("Sorry for the inconvenience", "Our tour guide is unavailable")
    previous_font_size = 0
    for line in msg_lines:
        fontsize = find_font_fit(line)
        lower_msg_font = ImageFont.truetype(FONT_NORMAL_PATH, fontsize)
        w = lower_msg_font.getlength(line)
        draw.text(((epd.width-w)/2, (epd.height/2 + 25 + previous_font_size)), line, font = lower_msg_font, fill = epd.WHITE)
        previous_font_size = fontsize + 20


    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    # logging.info(f"Time taken to draw text: {elapsed_time.seconds} seconds {elapsed_time.microseconds} microseconds")

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
   '''
     
    logging.info("Goto Sleep...")
    epd.sleep()
    logging.info("Ending with Sleep.")
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd10in2g.epdconfig.module_exit(cleanup=True)
    exit()
