from flask import session
from flask import redirect, flash, url_for, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def redirect_if_loggedin(f):
    """Redirect to dashboard if user is already connected."""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" in session:
            flash("You are already logged in!")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def connect(user):
    """Connect a user"""
    
    session.clear()
    session.permanent = True
    session["user_id"] = user.id