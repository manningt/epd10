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

'''


def check_ftp_log(timeout=10):

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

def main():
    print('Monitoring /var/log/vsftpd.log for changes...')
    while True:
        modified, last_line = check_ftp_log(timeout=10)
        if modified:
            print(f'\nLog file modified: {modified.strip()} at {datetime.now()}')
            print(f'{last_line=}')
        else:
            print('. ', end='', flush=True)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted - exiting...')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
