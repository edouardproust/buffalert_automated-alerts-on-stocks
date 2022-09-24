import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

if __name__ == "helpers._email": # cli
    import config as c
    from helpers import _string, _number
    from models import Stock, User
else: # flask run
    from .. import config as c
    from ..helpers import _string, _number
    from ..models import Stock, User

cta = 'https://' + c.SITE_DOMAIN + '/dashboard'


def send_register(user):

    text = f"""\
    Hello,
    You have been registered succesfully on {c.SITE_NAME}.
    - Email: {user.email}
    - Password: ******
    Go to your dashboard: {cta}
    """
    html = f"""\
    <html>
        <body>
            <p>Hello,<br>
            <p><b>You have been registered succesfully on {c.SITE_NAME}.</b></p>
            <ul>
                <li>Email: {user.email}</li>
                <li>Password: ******</li>
            </ul>
            <p><a href="{cta}" target="_blank">Go to your dashboard ➔</a></b>
        </body>
    </html>
    """
    subject = f"{c.SITE_NAME}: registration"
    send(user.email, text, html, subject)


def send_alert(alert):
    """Send an email to user when an stock alert is fired"""

    user = User.find(alert.user_id)
    stock = alert.stock

    text = f"""\
    Hello,
    One of your alerts set on {c.SITE_NAME} has been reached!
    - Ticker: {stock.ticker}
    - Price: {_number.usd(stock.price)}
    - Frequency: {c.ALERT_FREQUENCIES[alert.frequency]}
    - Time: {_string.alert_time_string(alert)}
    Go to your dashboard: {cta}
    """
    html = f"""\
    <html>
        <body>
            <p>Hello,<br>
            <p><b>One of your alerts set on {c.SITE_NAME} has been reached!</b></p>
            <ul>
                <li>Product: {stock.name} (Ticker: {stock.ticker})</li>
                <li>Price: {_number.usd(stock.price)}</li>
                <li>Alert checked {c.ALERT_FREQUENCIES[alert.frequency].lower()} {_string.alert_time_string(alert).lower()}</li>
            </ul>
            <p><a href="{cta}" target="_blank">Go to your dashboard ➔</a></b>
        </body>
    </html>
    """
    subject = f"Price reached on {stock.ticker}: {_number.usd(stock.price)}"

    if send(user.email, text, html, subject):
        # CLI log
        print(f'{datetime.now()} > Alert #{alert.id}: Email sent to user.')


def send_bug(content):
    """Send an email to admin when """
    # TODO
    print(f'{datetime.now()} > Email sent to admin.')


def send(receiver_email, msg_text, msg_html=None, subject=None):
    """
    Send an email
    https://mailtrap.io/blog/sending-emails-in-python-tutorial-with-code-examples#Sending-HTML-email
    """

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject or f"Email from {c.SITE_NAME}"
        message["From"] = f"{c.SITE_NAME} <{c.EMAIL_SENDER}>"
        message["To"] = receiver_email
        
        # convert both parts to MIMEText objects and add them to the MIMEMultipart message
        part1 = MIMEText(msg_text, "plain")
        message.attach(part1)
        if msg_html:
            part2 = MIMEText(msg_html, "html")
            message.attach(part2)
        # send your email
        with smtplib.SMTP(c.EMAIL_SERVER, c.EMAIL_PORT) as server:
            server.login(c.EMAIL_LOGIN, c.EMAIL_PASSWORD)
            server.sendmail(
                c.EMAIL_SENDER, receiver_email, message.as_string()
            )
    except:
        error = f'{datetime.now()} > Failed to send email.'
        print(f'{datetime.now()} > {error}')
        return False

    return True
    