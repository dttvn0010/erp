from datetime import datetime

def formatDate(date, fmt='%d/%m/%Y'):
    try:
        return date.strftime(fmt)
    except:
        return ''

def formatDateTime(date, fmt='%d/%m/%Y %H:%M:%S'):
    try:
        return date.strftime(fmt)
    except:
        return ''

def parseStringToDate(st, fmt='%d/%m/%Y'):
    if not st:
        return None
    try:
        return datetime.strptime(st, fmt)
    except ValueError:
        return None

def parseStringToDateTime(st, fmt='%d/%m/%Y %H:%M:%S'):
    if not st:
        return None
    try:
        return datetime.strptime(st, fmt)
    except ValueError:
        return None

def validateTime(time):
    try:
        datetime.strptime(time or '', '%H:%M')
        return True
    except ValueError:
        return False
