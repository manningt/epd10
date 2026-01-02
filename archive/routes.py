from flask import Blueprint, render_template
from flask import current_app as app
import os

main = Blueprint('main', __name__)

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


@main.route('/')
def index():
   return render_template('index.html')

# Define the routes for each button click
@main.route('/closed_normal', methods=['POST'])
def handle_closed_normal():
   app.logger.debug(f"closed_normal called")
   change_message(6)
   return render_template('index.html')

@main.route('/closed_no_guide', methods=['POST'])
def handle_closed_guide():
   change_message(5)
   return render_template('index.html')

@main.route('/open_normal', methods=['POST'])
def handle_open_normal():
   change_message(4)
   return render_template('index.html')

@main.route('/tour_in_progress_1', methods=['POST'])
def handle_tour_in_progress_1():
   change_message(1)
   return render_template('index.html')

@main.route('/tour_in_progress_2', methods=['POST'])
def handle_tour_in_progress_2():
   change_message(2)
   return render_template('index.html')

@main.route('/tour_in_progress_3', methods=['POST'])
def handle_tour_in_progress_3():
   change_message(3)
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
