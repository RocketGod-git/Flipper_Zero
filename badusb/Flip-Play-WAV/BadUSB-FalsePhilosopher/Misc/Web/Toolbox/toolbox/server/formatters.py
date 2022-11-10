import math
from datetime import datetime


def pretty_date(date, now=None):
    if now == None:
        now = datetime.now()
    difference = now - date

    seconds = difference.total_seconds()
    if seconds < 60:
        return f"{math.floor(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{math.floor(seconds / 60)} minutes ago"
    elif seconds < (3600 * 24):
        return f"{math.floor(seconds / 3600)} hours ago"
    else:
        return f"{difference.days} days ago"
