from utils_time import parse_hhmm, duration_hours, hour_float
from datetime import date, datetime

def message_indicator(messages):
    return {
        "count": len(messages),
        "has_messages": len(messages) > 0
    }

def subject_hours_pie(schedule):

    subjects = {}

    for lesson in schedule.entries:
        hours = duration_hours(lesson.start, lesson.end)
        subjects[lesson.title] = subjects.get(lesson.title, 0) + hours

    return subjects



