if __name__ == "helpers._string": # cli
    import config as c
else: # flask run
    from .. import config as c


def datetime_to_string(datetime, format='full'):
    if format == 'full':
        f = '%A %d-%m-%Y, %H:%M:%S'
    elif format == 'medium':
        f = '%d/%m/%y at %H:%M'
    elif format == 'short':
        f = '%d/%m, %H:%M'
    elif format == 'time':
        f = '%H:%M:%S'
    elif format == 'date':
        f = '%d/%m/%Y'
    else:
        return datetime
    return datetime.strftime(f)


def frequency_to_word(key):
    for i in c.ALERT_FREQUENCIES:
        if key == i:
            return c.ALERT_FREQUENCIES[i]
    return "/"


def tupleToString(tuple):
    string = ''.join(map(str, tuple))
    return string


def alert_time_string(alert):
    if alert.frequency not in ['m', 'w', 'd']:
        return 'Every hour'
    else:
        string = ''
        if alert.frequency == 'm':
            if alert.day in [1, 21, 31]:
                th = 'st'
            elif alert.day in [2, 22]:
                th = 'nd'
            elif alert.day == 3:
                th = 'rd'
            else: 
                th = 'th'
            string += f'On the {str(alert.day)}{th} at '
        elif alert.frequency == 'w':
            string += 'On ' + c.ALERT_WEEKDAYS[alert.weekday] + 's at '
        elif alert.frequency == 'd':
            string += 'At '
        if alert.frequency in ['m', 'w', 'd']:
            string += f'{str(alert.hour)}:00'
        return string
        
