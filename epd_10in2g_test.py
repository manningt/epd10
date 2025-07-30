#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import time
import os
import traceback

import logging
import epd10in2g
import datetime
from PIL import Image,ImageDraw,ImageFont

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

def change_message(top_msg, bottom_msgs):
    if top_msg.lower() == "closed":
        top_fill_color = epd.RED
        top_text_color = epd.WHITE
        bottom_fill_color = epd.BLACK
        bottom_text_color = epd.YELLOW
    else:
        top_fill_color = epd.YELLOW
        top_text_color = epd.BLACK
        bottom_fill_color = epd.BLACK
        bottom_text_color = epd.WHITE
    
    # width is 960, height is 640
    Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    # top half is a pie-slice (start and end angles are from 3 o'clock), bottom half is black
    shape = [(0, 0), (epd.width, epd.height)]
    draw.pieslice(shape, start = 180, end = 0, fill = top_fill_color)
    draw.rectangle(((0, epd.height/2), (epd.width, epd.height)), fill = bottom_fill_color)

    font180 = ImageFont.truetype(FONT_ITALIC_PATH, 180)
    w = font180.getlength(top_msg)
    draw.text(((epd.width-w)/2, 60), top_msg, font = font180, fill = top_text_color)

    previous_font_size = 0
    for line in bottom_msgs:
        fontsize = find_font_fit(line)
        lower_msg_font = ImageFont.truetype(FONT_NORMAL_PATH, fontsize)
        w = lower_msg_font.getlength(line)
        draw.text(((epd.width-w)/2, (epd.height/2 + 25 + previous_font_size)), line, font = lower_msg_font, fill = bottom_text_color)
        previous_font_size = fontsize + 20
            # could use font.getheight()
    buf = epd.getbuffer(Himage)
    
    start_time = datetime.datetime.now()
    logging.info("Before display image")
    epd.display(buf)
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    logging.info(f"Time taken to display: {elapsed_time.seconds} seconds {elapsed_time.microseconds} microseconds")


if __name__ == '__main__':
    try:
        epd = epd10in2g.EPD()
        epd.init()

    except Exception as e:
        logging.info(e)
        exit()

    try:
        # change_message("Closed", ("Sorry for the inconvenience", "Our tour guide is unavailable"))
        # logging.info("Should display closed message")
        # time.sleep(5)
        change_message("Open", ("Tour in progress", "Please return at 2 for a tour"))
        logging.info("Should display Return at 2 message")
 
    except Exception as e:
        logging.info(e)
        exit()

    '''
        logging.info("2.read bmp file")
        Himage = Image.open(os.path.join(picdir, '10in2g.bmp'))
        epd.display(epd.getbuffer(Himage))
        time.sleep(3)
    '''
