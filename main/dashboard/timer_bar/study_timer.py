from datetime import datetime

class Study_Timer:
    """
    A logic class to track study session duration using system time.
    """
    def __init__(self):
        """Initializes the timer state."""
        self.start_time = None
        self.total_seconds = 0
        self.running = False
   
    def start(self):
        """Starts the timer by recording the current timestamp."""
        if not self.running:
            self.start_time = datetime.now()
            self.running = True

    def stop(self):
        """
        Stops the current session and records the elapsed time.
        """
        if self.running:
            delta = datetime.now() - self.start_time
            self.total_seconds += delta.total_seconds()
            self.running = False

    def get_session_hours(self):
        """
        Calculates fractional hours for the most recent session only.
        Returns:
            float: Fractional hours.
        """
        if self.start_time and not self.running:
            delta = datetime.now() - self.start_time
            return delta.total_seconds() / 3600.0
        return 0.0

    def reset(self):
        """Resets all recorded time and stops the timer."""
        self.start_time = None
        self.total_seconds = 0
        self.running = False

    def hours(self):
        """
        Converts accumulated seconds into fractional hours.
        Returns:
            float: Total time in hours.
        """
        return self.total_seconds / 3600