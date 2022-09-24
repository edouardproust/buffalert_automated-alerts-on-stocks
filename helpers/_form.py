from flask import flash, request
from werkzeug.security import check_password_hash
from ..models import User, Stock, Alert
from ..helpers import _stock


def get(key):
    return request.args.get(key)


def post(key):
    return request.form.get(key)


def register_validate():
    """
    Check that the register form is correctly submitted by the user.
    Returns form data if form is valid. None otherwise.
    """

    # Get data from the form
    email = post("email")
    password = post("password")
    password_confirmation = post("password_confirmation")

    isValid  = True
    
    # Ensure email, password and confirmation were submitted
    if not email:
        flash("Email is mandatory.")
        isValid  = False
    if not password:
        flash("Password is mandatory.")
        isValid  = False
    if not password_confirmation:
        flash("Password confirmation is mandatory.")
        isValid  = False

    if email and password and password_confirmation:
        # Ensure that email is unique
        user = User.find_by_email(email)
        if user:
            flash(f"An account already exist with this email.")
            isValid = False
        # Ensure that password is longer than 8 chars
        if len(password) < 8:
            flash("Password must be 8 characters long or more.")
            isValid  = False
        # Ensure that password and confirmation match
        if password != password_confirmation:
            flash("Password and confirmation don't match.")
            isValid  = False
    # Return
    return {"email":email, "password":password} if isValid else None


def login_validate():
    """
    Check that the login form is correctly submitted by the user.
    Returns User if form is valid. None otherwise.
    """
    
    # Get data from the form
    email = post("email")
    password = post("password")

    isValid  = True
    # Ensure email and password were submitted
    if not email:
        flash("Email is mandatory.")
        isValid  = False
    if not password:
        flash("Password is mandatory.")
        isValid  = False
    # Ensure email exists and password is correct
    if email and password:
        user = User.find_by_email(email)
        if not user or (user and not check_password_hash(user.hash, password)):
            flash("Invalid email and/or password.")
            isValid  = False
    # Return
    return user if isValid else None


def account_token_validate():
    """
    Validate account-token form.
    Returns form data if is valid, None otherwise.
    """
    # Get data from the form
    token = post("token")

    isValid = True
    # Ensure form is not empty
    if not token:
        isValid = False
    #return 
    return {"token":token} if isValid else None


def account_credentials_validate():
    """
    Validate account-credentials form.
    Returns form data if is valid, None otherwise.
    """

    # Get data from the form
    email = post("email")
    password = post("password")
    password_confirmation = post("password_confirmation")

    isValid = True
    # Ensure form is not empty
    if not email and not password:
        isValid = False
    # Ensure that password confirmation is set and matches
    if password:
        if not password_confirmation:
            flash("Password confirmation can't be blank.")
            isValid = False
        elif password_confirmation != password:
            flash("Password and confirmation don't match.")
            isValid = False
    # Ensure that email is unique
    user = User.find()
    if email and email != user.email:
        if User.find_by_email(email):
            flash("An account already exist with this email.")
            isValid = False
    # Ensure that password is longer than 8 chars
    if password and len(password) < 8:
        flash("Password must be 8 characters long or more.")
        isValid  = False
    # Return
    return {"email":email, "password":password} if isValid else None


def alert_create_validate():
    """
    Validate alert-create form.
    Returns form data.
    """
    
    quote = {}
    # Get data from the form
    ticker = post("ticker")
    price = post("price")
    frequency = post("frequency")
    # Ensure all the fields are set
    if not ticker or not price or not frequency:
        flash("Ticker, price and frequency are mandatory.")
    else: 
        # Ensure the ticker is supported
        quote = _stock.quote(ticker)
        if quote:
            return {
                "ticker": ticker, 
                "name": quote["name"], 
                "last_price": quote["price"], 
                "alert_price": price, 
                "frequency": frequency, 
                "hour": post("hour"),
                "weekday": post("weekday"),
                "day": post("day")
            }
    return None


def alert_update_handle():
    """
    Handle alert-update form.
    Returns form data if filled by the user of the one existing in db.
    """

    # Get data from the form
    ticker = post("ticker") or get('ticker')
    price = post("price")
    frequency = post("frequency")
    # Ensure mandatory fields are set
    if not ticker or not price or not frequency:
        flash("Ticker, price and frequency are mandatory.")
    else:
        return {
            "alert": Alert.find(get("id")), 
            "stock_id": Stock.get_by_ticker(ticker).id, 
            "price": price, 
            "frequency": frequency, 
            "hour": post("hour"),
            "weekday": post("weekday"),
            "day": post("day")
        }
    return None