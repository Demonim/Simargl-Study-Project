import json
import os

class WeeklyStudyTracker:
    def __init__(self, filename="study_data.json"):
        self.filename = filename

        # автоматичне створення папки, якщо її немає
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        self.default_data = {
            "Mon": {'manual': 0.0, 'timer': 0.0}, 
            "Tue": {'manual': 0.0, 'timer': 0.0}, 
            "Wed": {'manual': 0.0, 'timer': 0.0}, 
            "Thu": {'manual': 0.0, 'timer': 0.0}, 
            "Fri": {'manual': 0.0, 'timer': 0.0}, 
            "Sat": {'manual': 0.0, 'timer': 0.0}, 
            "Sun": {'manual': 0.0, 'timer': 0.0}
        }
        self.data = self.load_from_disk()
        
    def load_from_disk(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return self.default_data
        return self.default_data

    def save_to_disk(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def set_day(self, day, hours):
        if day in self.data:
            self.data[day]['manual'] = hours
            self.save_to_disk()

    def add_time(self, day, hours):
        if day in self.data:
            self.data[day]['timer'] += hours
            self.save_to_disk()

    def reset_all(self):
        self.data = {k: v.copy() for k, v in self.default_data.items()}
        self.save_to_disk()

    def all(self):
        return self.data