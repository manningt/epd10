from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)
import os

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
   app.logger.debug(f"Directories in current path: {dir_list}")
   for directory in dir_list:
      os.rmdir(directory)
   try:
      os.mkdir(str(message_number))
   except Exception as e:
      app.logger.error(f"Error creating directory {message_number}: {e}")
   app.logger.debug(f"Changed message to {message_number}")


@app.route('/')
def index():
   radio_fieldset = {'name': 'Message','buttons': []}
   for i in range(len(labels)):
      radio_fieldset['buttons'].append({'label': labels[i], 'value': label_values[i]})

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