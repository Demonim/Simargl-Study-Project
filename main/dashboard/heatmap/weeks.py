from datetime import datetime

def week_offset(date: datetime):
    """
    Reurns:
    0-current week
    1-last week ...
    """
    now = datetime.now()
    delta = now.date() - date.date()
    return delta.days // 7
