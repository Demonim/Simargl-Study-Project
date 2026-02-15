from ..utils_time import duration_hours
import re


def subject_hours(schedule) -> dict[str, float]:
    """
    Analyzes the user's schedule to calculate the total study hours per subject.
   
    Args:
        schedule: The schedule object containing lesson entries with start/end times.
       
    Returns:
        dict[str, float]: A dictionary mapping subject titles to total hours.
    """

    subjects = {}

    for lesson in schedule.entries:
        hours = duration_hours(lesson.start, lesson.end)
        subjects[lesson.title] = subjects.get(lesson.title, 0) + hours

    return subjects




def pie_values_labels(subject_hours: dict[str, float]):
    """
    Prepares raw study data for visualization by cleaning subject names.
   
    Args:
        subject_hours: Dictionary of analyzed subject data.
       
    Returns:
        tuple: (values_list, cleaned_labels_list)
    """

    if not subject_hours:
        return [], []

    values = list(subject_hours.values())
    labels = [re.sub(r'^\d+\s*', '', subject) for subject in subject_hours.keys()]
   
    return values, labels