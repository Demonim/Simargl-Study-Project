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
    if schedule is None or not hasattr(schedule, 'entries'):
        return subjects
    
    for lesson in schedule.entries:
        try:
            # Calculate hours for each lesson
            hours = duration_hours(lesson.start, lesson.end)
            if hours < 0:
                continue
            # Use lesson title or 'Unknown' if missing
            title = str(lesson.title) if lesson.title else "Unknown"
            # Accumulate hours for each subject
            subjects[title] = subjects.get(title, 0) + hours
        except Exception:
            continue
    
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

    values = []
    labels = []

    for subject, hours in subject_hours.items():
        try:
            # Convert hours to float and skip negative values
            hours_float = float(hours)
            if hours_float < 0:
                continue
            values.append(hours_float)
            # Remove leading numbers from subject title for cleaner label
            cleaned_label = re.sub(r'^\d+\s*', '', str(subject))
            labels.append(cleaned_label)
        except (ValueError, TypeError):
            continue
    
    return values, labels