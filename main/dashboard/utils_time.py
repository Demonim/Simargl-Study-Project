from datetime import datetime

def parse_hhmm(time_str: str) -> datetime:
    """Parse time string in HH:MM format to datetime object."""
    try:
        if time_str is None:
            raise ValueError("Time string cannot be None")
        return datetime.strptime(str(time_str), "%H:%M")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM format.") from e

def duration_hours(start: str, end: str) -> float:
    """Calculate duration in hours between two time strings."""
    try:
        if start is None or end is None:
            return 0.0
        
        start_dt = parse_hhmm(start)
        end_dt = parse_hhmm(end)
        
        duration = (end_dt - start_dt).total_seconds() / 3600
        return max(0.0, duration)
    except (ValueError, TypeError):
        return 0.0
    
def hour_float(time_str: str) -> float:
    """Convert time string to float hours."""
    try:
        if time_str is None:
            return 0.0
        t = parse_hhmm(time_str)
        return t.hour + t.minute / 60
    except (ValueError, TypeError):
        return 0.0

def hour_str(hours: float) -> str:
    """Convert float hours to readable string format."""
    try:
        if hours is None:
            return "0 hours 0 minutes"
        hours = float(hours)
        if hours < 0:
            hours = 0.0
        total_minutes = int(round(hours * 60))
        h = total_minutes // 60
        m = total_minutes % 60
        return f"{h} hours {m} minutes"
    except (ValueError, TypeError):
        return "0 hours 0 minutes"