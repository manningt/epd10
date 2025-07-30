from flask import Blueprint, render_template

from flask import current_app as app

main = Blueprint('main', __name__)

@main.route('/')
def index():
   return render_template('index.html')

# Define the routes for each button click
@main.route('/closed_normal', methods=['POST'])
def handle_closed_normal():
   app.logger.debug(f"closed_normal called")
   print("closed_normal called")
   return render_template('index.html')

@main.route('/closed_no_staff', methods=['POST'])
def handle_closed_no_staff():
   return render_template('index.html')

@main.route('/open_normal', methods=['POST'])
def handle_open_normal():
   return render_template('index.html')

@main.route('/tour_in_progress_1', methods=['POST'])
def handle_tour_in_progress_1():
   return render_template('index.html')

@main.route('/tour_in_progress_2', methods=['POST'])
def handle_tour_in_progress_2():
   return render_template('index.html')

@main.route('/tour_in_progress_3', methods=['POST'])
def handle_tour_in_progress_3():
   return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
