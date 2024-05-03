from flask import Flask
from flask_session import Session
from website.config.config import get_config


def create_app():
    '''
    This is the starting method of the flask application. All the flask BASIC configurations are done here
    '''
    app = Flask(__name__)
    
    #Imports the views file and registers the routes inside the application
    from .views.views import views

    app.register_blueprint(views,url_prefix="/")

    # Get the appropriate configuration based on the environment
    app_config = get_config()

    # Set the configurations for the Flask application
    app.config['SECRET_KEY'] = app_config.SECRET_KEY

    # Session configurations to make sure session data is handled correctly
    app.config['SESSION_TYPE'] = app_config.SESSION_TYPE
    app.config['SESSION_PERMANENT'] = app_config.SESSION_PERMANENT
    app.config['SESSION_USE_SIGNER'] = app_config.SESSION_USE_SIGNER
    app.config['SESSION_KEY_PREFIX'] = app_config.SESSION_KEY_PREFIX

    # Initialize Flask Session
    Session(app)

    return app