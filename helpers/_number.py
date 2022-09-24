def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def float(value):
    """Format price in float with 2 decimal digits"""
    return f"{value:,.2f}" 
    
    
def is_float_between(int, boundary_1, boundary_2):
    """
    Check if a number is between 2 other numbers.
    Returns True if is between. False otherwise.
    """

    if boundary_1 <= boundary_2:
        if int >= boundary_1 and int <= boundary_2:
            return True
    elif boundary_1 > boundary_2:
        if int <= boundary_1 and int >= boundary_2:
            return True
    else:
        return False


def days_in_month():
    """Returns the number of days in the current month"""

    import calendar
    import datetime

    currentDate = datetime.date.today()
    daysInMonth= calendar.monthrange(currentDate.year, currentDate.month)[1]

    return daysInMonth


def hour_format(hour):
    """Ensure the hour is displayed with 2 digits"""
    if len(str(hour)) < 2:
        hour = "0" + str(hour)
    return str(hour)
