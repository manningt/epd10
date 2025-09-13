from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
app = Flask(__name__)

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
    return render_template('index.html')

@socketio.on('change_message')
def handle_change_message(data):
   app.logger.info(f'received change_message. {data=}')
   

if __name__ == '__main__':
    socketio.run(app, debug=True)