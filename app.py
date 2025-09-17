from flask import Flask, render_template, logging
from flask_socketio import SocketIO
import os

import logging
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')

app = Flask(__name__)
socketio = SocketIO(app)

# img_map = [ "0", "open-tour-at-1", "open-tour-at-2","open-tour-at-3", \
#    "open-welcome","closed-no-guide","closed-see-website"]
labels = [ \
   "Closed: See website for hours", \
   "Closed: No tour guide", \
   "Open: Welcome", \
   "Open: Come back at 1", \
   "Open: Come back at 2", \
   "Open: Come back at 3"]
label_values = [ "6", "5", "4", "1", "2", "3"]

def change_message(message_number):
   try:
      os.chdir('/home/pi/epaper')
   except Exception as e:
      app.logger.error(f"Error changing directory: {e}")
      return
   try:
      dir_list = next(os.walk('.'))[1]
   except StopIteration:
      dir_list = []
   # app.logger.debug(f"Directories in current path: {dir_list}")
   for directory in dir_list:
      if directory[0] == 'm' and len(directory) == 2:
         os.rmdir(directory)
   try:
      os.mkdir(f'm{message_number}')
   except Exception as e:
      app.logger.error(f"Error creating directory {message_number}: {e}")
   app.logger.debug(f"Changed message to {message_number}")

def get_current_message_number():
   try:
      dir_list = next(os.walk('/home/pi/epaper'))[1]
   except StopIteration:
      dir_list = []
   for directory in dir_list:
      if directory[0] == 'm'and len(directory) == 2:
         return directory[1]
   return None

@app.route('/')
def index():
   current_message_number = get_current_message_number()
   # app.logger.debug(f'{current_message_number=}')
   radio_fieldset = {'name': 'Message','buttons': []}
   for i in range(len(labels)):
      button = {'label': labels[i], 'value': label_values[i]}
      if label_values[i] == current_message_number:
         button['checked'] = True
      radio_fieldset['buttons'].append(button)

   return render_template('index.html', \
      page_title="Select_Message", \
      heading="Select the message for the visitor's door display", \
      fieldset=radio_fieldset)


@socketio.on('change_message')
def handle_change_message(data):
   # app.logger.debug(f'received change_message. {data=}')
   if 'Message' in data:
      change_message(data['Message'])
   else:
      app.logger.error("No 'Message' key in data")


if __name__ == '__main__':
    socketio.run(app, debug=True)