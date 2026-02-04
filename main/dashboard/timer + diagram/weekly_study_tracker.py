class WeeklyStudyTracker:
    def __init__(self):
        self.days = {
            "Mon": 0.0,
            "Tue": 0.0,
            "Wed": 0.0,
            "Thu": 0.0,
            "Fri": 0.0,
            "Sat": 0.0,
            "Sun": 0.0,
        }

    def set_day(self, day, hours):
        self.days[day] = hours

    def get_day(self, day):
        return self.days[day]

    def add_time(self, day, hours):
        self.days[day] += hours

    def all(self):
        return self.days
