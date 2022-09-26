from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from helpers._email import send_alert, send_bug
from helpers._number import float, is_float_between, days_in_month
from helpers._stock import quote
from models import Alert, Stock


def run():
    """
    Launch the cronjob
    (This function is called at the bottom of the file)
    """
    
    sched = BlockingScheduler()
    set_cronjobs(sched)
    print(f"{datetime.now()} > Cronjobs set for {__name__}")
    sched.start()


def set_cronjobs(sched):
    """@sched.scheduled_job
    - List of parameters for 'cron' trigger: https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
    - Other triggers: 'interval' 'date', 'combining' and 'base' (https://apscheduler.readthedocs.io/en/3.x/modules/triggers/{trigger}.html)
    """
    @sched.scheduled_job('cron', hour='*/1')
    def hourly():
        for alert in get_now_alerts():
            if is_triggered(alert):
                send_alert(alert)
                Alert.update(alert, {"triggered_at": datetime.now()})


def get_now_alerts():
    print(f'{datetime.now()} > Building now_alerts list...')
    
    # Get current time
    now = datetime.now()
    
    # Get alerts with the current time
    now_alerts = []
    alerts = Alert.all()

    for alert in alerts:
        append = False

        # Hourly alerts:
        if alert.frequency == 'h':
            append = True

        # Daily alerts:
        elif alert.frequency == 'd':
            # Append alert if alert's hour matches with 'now'
            append = (alert.hour == now.hour)

        # Weekly alerts:
        elif alert.frequency == 'w':
            # Append alert if alert's weekday and hour match with 'now'
            append = (alert.weekday == now.weekday() and alert.hour == now.hour)

        # Montly alerts:
        elif alert.frequency == 'm':
            if alert.hour == now:
                # In the case that alert's day exceeds this month's nb of days...
                if alert.day > days_in_month():
                    # ...Append if today is the last day of this month
                    append = (now.day == days_in_month())
                else:
                    # Append if alert's day matches with 'now'
                    append = (alert.day == now.day)

        # Add alert to the listor not
        if append:
            now_alerts.append(alert)

    # Return list
    if not len(now_alerts):
        print(f'{datetime.now()} > No alert set at this time.')
    return now_alerts


def is_triggered(alert):
    id = str(alert.id)
    stock = alert.stock
    price_before = float(stock.price)
    price_limit = float(alert.price)
    quote_str = f"limit: {price_limit}, before: {price_before}"

    try:
        price_now = float(quote(stock.ticker, alert.user_id)['price'])
        quote_str += f', now: {price_now}'
        Stock.update(stock.ticker, price_now)
    except:
        send_bug()
        print(f'{datetime.now()} > ERROR: Failed to fetch the alert data.')

    if is_float_between(price_limit, price_before, price_now):
        print(f'{datetime.now()} > Alert #{id}: Price reached! ({quote_str})')
        return True
    print(f'{datetime.now()} > Alert #{id}: Price limit not reached. ({quote_str})')
    return False


run()