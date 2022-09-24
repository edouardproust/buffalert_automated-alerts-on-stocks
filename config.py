from dotenv import load_dotenv
import os

load_dotenv()


# App configuration

SITE_NAME = 'BuffAlert'
SITE_DOMAIN = 'buffalert.com'
APP_SECRET = os.getenv('APP_SECRET')

# Database
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Email
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_SERVER = os.getenv('EMAIL_SERVER')
EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')

# Alerts

ALERT_FREQUENCIES = {
    # Extra fields/checks are precised in comment for each
    'h': 'Hourly', # none
    'd': 'Daily', # hour
    'w': 'Weekly', # day of the week, hour
    'm': 'Monthly' # day (number), hour
}

ALERT_WEEKDAYS = {
    0: 'Monday', 
    1: 'Tuesday', 
    2: 'Wednesday', 
    3: 'Thursday', 
    4: 'Friday', 
    5: 'Saturday', 
    6: 'Sunday'
}

def app_config(app):
    from flask_session import Session

    app.config['SECRET_KEY'] = APP_SECRET

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Ensure templates are auto-reloaded
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Save config into session
    Session(app)


# Helpers =================================================================

app = None

def set_app():
    from flask import Flask

    global app
    if not app:
        app = Flask(__name__)
        app_config(app)


def get_app():

    if not app:
        set_app()

    return app
