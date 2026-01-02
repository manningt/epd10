from flask import Flask
from routes import main
import logging
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')
    app.logger.debug(f"in create_app()")
    app.register_blueprint(main)

    socketio = SocketIO()
    socketio = SocketIO(app)
    socketio.init_app(app)
    # from . import events
    # app.register_blueprint(events.bp)

    return app
