class WeeklyStudyTracker:
    def __init__(self):
        self.data = {
            "Mon": {'manual': 0.0, 'timer': 0.0}, 
            "Tue": {'manual': 0.0, 'timer': 0.0}, 
            "Wed": {'manual': 0.0, 'timer': 0.0}, 
            "Thu": {'manual': 0.0, 'timer': 0.0}, 
            "Fri": {'manual': 0.0, 'timer': 0.0}, 
            "Sat": {'manual': 0.0, 'timer': 0.0}, 
            "Sun": {'manual': 0.0, 'timer': 0.0}
        }
        
    def set_day(self, day, hours):
        self.data[day]['manual'] = hours

    def get_day(self, day):
        return self.data[day]

    def add_time(self, day, hours):
        self.data[day]['timer'] += hours

    def all(self):
        return self.data

