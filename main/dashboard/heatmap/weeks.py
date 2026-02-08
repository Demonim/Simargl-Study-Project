from datetime import datetime
def week_offset(date):
    if isinstance(date, str):
        date = datetime.strptime(date[:10], "%Y-%m-%d")

    now = datetime.now()
    delta = now.date() - date.date()
    return delta.days // 7
