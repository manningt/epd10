from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)
import os

socketio = SocketIO(app)

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
    radio_fieldset = {
        'name': 'Message',
        'buttons': [
            {'label': 'Closed: See website for hours', 'value': '6', 'checked': True},
            {'label': 'Closed: No tour guide', 'value': '5'},
            {'label': 'Open: Welcome', 'value': '4'},
            {'label': 'Open: Come back at 1', 'value': '1'},
            {'label': 'Open: Come back at 2', 'value': '2'},
            {'label': 'Open: Come back at 3', 'value': '3'},
        ]
    }
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