from datetime import datetime

#class to work with timer
class Study_Timer:
    def __init__(self):
        self.start_time = None
        self.total_seconds = 0
        self.running = False
    
    def start(self):
        if not self.running:
            self.start_time = datetime.now()
            self.running = True

    def stop(self):
        if self.running:
            delta = datetime.now() - self.start_time
            self.total_seconds += delta.total_seconds()
            self.running = False

    def reset(self):
        self.start_time = None
        self.total_seconds = 0
        self.running = False

    def hours(self):
        return self.total_seconds / 3600
