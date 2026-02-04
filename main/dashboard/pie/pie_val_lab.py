from utils_time import hour_str

#to get values and labels for pie
def pie_values_labels(subject_hours: dict[str, float]):
    values = list(subject_hours.values())
    labels = ["{}/n{}".format(subject, hour_str(h)) 
              for subject, h in subject_hours.keys()]
    
    return values, labels