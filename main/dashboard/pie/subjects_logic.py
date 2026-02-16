from ..utils_time import duration_hours
import re


def subject_hours(schedule) -> dict[str, float]:
    """
    Calculates the cumulative study hours for each unique subject.
    
    Args:
        schedule: Schedule object containing lesson entries.
        
    Returns:
        dict[str, float]: A dictionary where keys are subject names and values are total hours.
    """

    subjects = {}

    for lesson in schedule.entries:
        hours = duration_hours(lesson.start, lesson.end)
        subjects[lesson.title] = subjects.get(lesson.title, 0) + hours

    return subjects




def pie_values_labels(subject_hours: dict[str, float]):
    """
    Cleans data for visualization by stripping leading numeric prefixes.
    
    Args:
        subject_hours (dict): Raw data with subject titles and hours.
        
    Returns:
        tuple: (values_list, cleaned_labels_list). Both are empty if input is empty.
    """

    if not subject_hours:
        return [], []

    values = list(subject_hours.values())
    labels = [re.sub(r'^\d+\s*', '', subject) for subject in subject_hours.keys()]
   
    return values, labels