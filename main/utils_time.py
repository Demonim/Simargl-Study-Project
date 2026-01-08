from datetime import datetime

def parse_hhmm(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M")

def duration_hours(start: str, end: str) -> float:
    start_dt = parse_hhmm(start)
    end_dt = parse_hhmm(end)
    return (end_dt - start_dt).total_seconds() / 3600
    
def hour_float(time_str: str) -> float:
    t = parse_hhmm(time_str)
    return t.hour + t.minute / 60

def hour_str(hours: float) -> str:
    total_minutes = int(round(hours * 60))
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h} hours {m} minutes"

