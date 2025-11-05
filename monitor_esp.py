#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
from subprocess import Popen, PIPE
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG)

'''
Monitor changes to the FTP log file using inotifywait.

Requires: 
  - sudo apt-get install inotify-tools
  - add to /etc/sudoers:  myusername ALL = (root) NOPASSWD: /home/pi/repos/epd10/monitor_esp.py   - use: sudo visudo


if day of week is Fri, Sat, Sun:
    between 11:30 and 15:10 do short_sleep
    between 15:20 and (15:20+9) do long_sleep (it should wake at 23:20 & 7:20)
    between 6:00 and 11:30 do medium_sleep

'''

from enum import Enum
class SleepDuration(Enum):
    LONG = 8 * 60 * 60  # 8 hours
    MEDIUM = 1 * 60 * 60  # 1 hour
    SHORT = 10 * 60  # 10 minutes
    VSHORT = 30  # 30 seconds

def monitor_ftp_log(timeout=10):
   cmd = ['sudo', 'inotifywait', '-q', '-e', 'modify', '/var/log/vsftpd.log', '-t', f'{timeout}']
   process = Popen(cmd, stdout=PIPE, stderr=PIPE)
   output, errors = process.communicate()
   if errors:
      logging.error(f'Error: {errors.decode()}')
      return None
   else:
      cmd = ['sudo', 'tail', '-1', '/var/log/vsftpd.log']
      process = Popen(cmd, stdout=PIPE, stderr=PIPE)
      output2, errors2 = process.communicate()
      if errors2:
         logging.error(f'Error: {errors2.decode()}')

      # return (output.decode(), output2.decode())[1]  # return last line of log file
      return (output.decode(), output2.decode())  # return last line of log file
   # print(f'{output.decode()=} {errors.decode()=}')


def get_current_sleep_duration():
   return_enum = None
   try:
      dir_list = next(os.walk('/home/pi/epaper'))[1]
   except StopIteration:
      dir_list = []
   for directory in dir_list:
      if directory[0] == 't' and directory[1:].isdigit():
         sleep_seconds = int(directory[1:])
         match sleep_seconds:
            case SleepDuration.LONG.value:
               return_enum = SleepDuration.LONG
            case SleepDuration.MEDIUM.value:
               return_enum = SleepDuration.MEDIUM
            case SleepDuration.SHORT.value:
               return_enum = SleepDuration.SHORT
            case SleepDuration.VSHORT.value:
               return_enum = SleepDuration.VSHORT
            case _:
               logging.debug(f'Unknown sleep duration: {sleep_seconds} seconds')
      if return_enum:
         break
   # logging.debug(f'sleep duration not found')
   return return_enum


def main():
   sleep_duration = get_current_sleep_duration()
   logging.debug(f'Current sleep duration: {sleep_duration.name}' if sleep_duration else "None")
   logging.debug('Monitoring /var/log/vsftpd.log for changes...')
   while True:
      modified, last_line = monitor_ftp_log(timeout=10)
      if modified:
         # print(f'\nLog file modified: {modified.strip()} at {datetime.now()}')
         # logging.debug(f'{last_line=}')
         if last_line and ('] OK LOGIN' in last_line):
            logging.info('login detected! Exiting monitor.')
            break
      else:
         print('. ', end='', flush=True)

'''
The following gets written to the ftp log:
Wed Nov  5 07:45:50 2025 [pid 3293] CONNECT: Client "::ffff:10.42.1.171"
Wed Nov  5 07:45:50 2025 [pid 3292] [user] OK LOGIN: Client "::ffff:10.42.1.171"
'''


if __name__ == '__main__':

   # day_of_week = datetime.now().weekday()  # Monday is 0 and Sunday is 6
   try:
      main()
   except KeyboardInterrupt:
      print('Interrupted - exiting...')
      try:
         sys.exit(130)
      except SystemExit:
         os._exit(130)
