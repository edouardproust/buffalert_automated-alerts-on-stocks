import requests
from flask import flash
import urllib.parse

if __name__ == "helpers._stock": # cli
    from models import User
else: # flask run
    from ..models import User


def quote(ticker, user_id=None):
    """Look up quote for ticker."""

    user = get_user(user_id)

    # Contact API
    try:
        token = user.token
        ticker_safe = urllib.parse.quote_plus(ticker)
        url = f"https://cloud.iexapis.com/stable/stock/{ticker_safe}/quote?token={token}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        strerror = e.args[0]
        print(f'Quote - Request Error: {e}')
        print(strerror)
        if '403' in strerror:
            flash('The security token is not valid. Please update it in "Account" page.')
        elif '404' in strerror:
            flash('Ticker is not valid.')
        else:
            flash('An error occured while calling the API. Please contact us.')
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "ticker": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError) as e:
        e_class = e.__class__.__name__
        print(f'Quote - Parsing Error: {e_class} {e} (Request: {url})')
        flash('Quote parsing error. Please contact us.')
        return None


def get_user(user_id=None):
    if user_id:
        user = User.find(user_id)
        if not user:
            raise Exception('No user with the ID provided in the database.')
    else:
        user = User.find()
        if not user:
            raise Exception('You must precise an ID manually.')
    # return
    return user