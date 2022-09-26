from dotenv import load_dotenv
import os
load_dotenv()

# App configuration

DEV_MODE = True

SITE_NAME = 'BuffAlert'
SITE_DOMAIN = 'buffalert.xyz'
SITE_EMAIL = 'contact@' + SITE_DOMAIN

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

# Database variables setup

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
DB = os.getenv('DB')

# Email variables setup

EMAIL_HOST = os.getenv('MAILTRAP_HOST') if DEV_MODE else os.getenv('MAILGUN_SMTP_HOSTNAME')
EMAIL_PORT = os.getenv('MAILTRAP_PORT') if DEV_MODE else os.getenv('MAILGUN_PORT')
EMAIL_USERNAME = os.getenv('MAILTRAP_USERNAME') if DEV_MODE else os.getenv('MAILGUN_LOGIN')
EMAIL_PASSWORD = os.getenv('MAILTRAP_PASSWORD') if DEV_MODE else os.getenv('MAILGUN_PASSWORD')


def app_config(app):
    from flask_session import Session

    app.config['SECRET_KEY'] = os.getenv('APP_SECRET')

    # Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}/{DB}"
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
