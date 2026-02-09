from ..utils_time import duration_hours

def subject_hours(schedule) -> dict[str, float]:

    subjects = {}

    for lesson in schedule.entries:
        hours = duration_hours(lesson.start, lesson.end)
        subjects[lesson.title] = subjects.get(lesson.title, 0) + hours

    return subjects
