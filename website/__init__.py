from flask import Flask
from flask_session import Session
from website.config import config


def create_app():
    '''
    This is the starting method of the flask application. All the flask BASIC configurations are done here
    '''
    app = Flask(__name__)
    
    #Imports the views file and registers the routes inside the application
    from .views.views import views
    # from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    # app.register_blueprint(auth,url_prefix="/")

    #Creates a secure key to store the session under
    app.config['SECRET_KEY'] = config.SECRET_KEY

    #Session configurations to make sure session data is handled correctly
    app.config['SESSION_TYPE'] = config.SESSION_TYPE
    app.config['SESSION_PERMANENT'] = config.SESSION_PERMANENT
    app.config['SESSION_USE_SIGNER'] = config.SESSION_USE_SIGNER
    app.config['SESSION_KEY_PREFIX'] = config.SESSION_KEY_PREFIX
    Session(app)

    return app