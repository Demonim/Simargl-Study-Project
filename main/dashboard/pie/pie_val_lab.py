from main.dashboard.utils_time import hour_str
import re

#to get values and labels for pie
def pie_values_labels(subject_hours: dict[str, float]):
    values = list(subject_hours.values())
    
    labels = []
    for subject in subject_hours.keys():
        clean_name = re.sub(r'^\d+\s*', '', subject)
        labels.append(clean_name)
    
    return values, labels