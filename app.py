from flask import render_template, redirect, flash, url_for, request, session
from werkzeug.security import generate_password_hash
from datetime import datetime
import config as c
from models import User, Stock, StockCategory, Alert
from helpers import _form, _session, _string, _number, _email

app = c.get_app()

# Templates variables & filters
app.jinja_env.globals['sitename'] = c.SITE_NAME
app.jinja_env.filters["usd"] = _number.usd
app.jinja_env.filters["float"] = _number.float
app.jinja_env.filters["hour_format"] = _number.hour_format
app.jinja_env.filters["dt"] = _string.datetime_to_string
app.jinja_env.filters["frequency"] = _string.frequency_to_word
app.jinja_env.filters["time_str"] = _string.alert_time_string


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.errorhandler(404)
def not_found(e):
    """404 Error page"""
    return render_template("404.html")


@app.route("/")
def index():
    # Get request
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
@_session.redirect_if_loggedin
def register():
    # POST request
    if request.method == "POST":
        # Form validation
        data = _form.register_validate()
        if data:
            # Save user, connect him/her and redirect to dashboard
            user = User.create(data["email"], data["password"])
            _session.connect(user)
            flash("You have been registered successfully.")
            _email.send_register(user)
            return redirect(url_for("dashboard"))
    # GET request
    return render_template("register.html", email=_form.post('email'))


@app.route("/login", methods=["GET", "POST"])
@_session.redirect_if_loggedin
def login():
    # POST request
    if request.method == "POST":
        # Form validation
        user = _form.login_validate()
        if user:
            # Connect and redirect user to dashboard
            _session.connect(user)
            flash("You are now logged in.")
            return redirect(url_for("dashboard"))
    # GET request
    return render_template("login.html", email=_form.post('email'))


@app.route("/logout")
@_session.login_required
def logout():
    """Log user out"""

    session.clear()
    flash("You are been logged out.")
    return redirect(url_for("login"))


@app.route("/dashboard")
@_session.login_required
def dashboard():
    user = User.find()
    alerts = Alert.find_by_user()
    return render_template("dashboard.html", user=user, alerts=alerts)


@app.route("/account", methods=["GET", "POST"])
@_session.login_required
def account():
    # POST request
    if request.method == "POST":
        data = _form.account_token_validate()
        if data:
            user = User.find()
            User.update(user, {"token": data['token']})
            flash("Token updated.")
        data = _form.account_credentials_validate()
        if data:
            user = User.find()
            hash = generate_password_hash(data['password']) if data['password'] else getattr(user, "hash")
            User.update(user, {"email":data["email"], "hash":hash})
            flash("Your account credentials have been updated.")
    # GET request
    return render_template("account.html", user=User.find())


@app.route("/account/delete", methods=["GET", "POST"])
@_session.login_required
def account_delete():
    # POST request
    if request.method == "POST":
        User.delete(User.find())
        session.clear()
        flash("You account has been deleted.")
        return redirect(url_for("login"))
    # GET request
    else:
        # Security: forcing to use POST request
        flash("Account deletion must be made throught the action button on \"Account\" page.")
        return redirect(url_for('account'))
        

@app.route("/alert/create", methods=["GET", "POST"])
@_session.login_required
def alert_create():
    # POST method
    if request.method == "POST":
        data = _form.alert_create_validate()
        if data:
            category = StockCategory.get_by_name("US Stocks")
            # Create stock
            stock = Stock.update(data["ticker"], data["last_price"], data["name"], category.id)
            # Create alert
            Alert.create(stock.id, data["alert_price"], data["frequency"], data["hour"], data["weekday"], data["day"])
            flash("Alert created.")
            return redirect(url_for("dashboard"))
    # GET request
    return render_template("alert-create.html", 
        frequencies=c.ALERT_FREQUENCIES, 
        weekdays=c.ALERT_WEEKDAYS,
        # Form values
        ticker=_form.post("ticker"),
        price=_form.post("price"),
        frequency=_form.post("frequency"),
        hour=_form.post("hour"),
        weekday=_form.post("weekday"),
        day=_form.post("day"),
    )


@app.route("/alert/update", methods=["GET", "POST"])
@_session.login_required
def alert_update():
    # POST request
    if request.method == "POST":
        data = _form.alert_update_handle()
        if data:
            Alert.update(data['alert'], {
                'stock_id': data['stock_id'], 
                'user_id': session['user_id'],
                'price': data['price'],
                'frequency': data['frequency'],
                'hour': data['hour'],
                'weekday': data['weekday'],
                'day': data['day']
            })
            flash("Alert updated.")
            return redirect(url_for('dashboard'))
    # GET request
    if not _form.get('id'):
        flash("No alert ID provided.")
        return redirect(url_for('dashboard'))
    return render_template('alert-update.html', 
        frequencies=c.ALERT_FREQUENCIES,
        weekdays=c.ALERT_WEEKDAYS, 
        alert=Alert.find(_form.get('id'))
    )
    

@app.route("/alert/delete")
@_session.login_required
def alert_delete():
    # GET request
    id = _form.get('id')
    if not id:
        flash("No alert ID provided.")
    else:
        alert = Alert.find(id)
        Alert.delete(alert)
        flash("Alert deleted.")
    # Response
    return redirect(url_for('dashboard'))
