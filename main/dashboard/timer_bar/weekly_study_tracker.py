import json
import os

class WeeklyStudyTracker:
    """
    Manages the persistence and retrieval of weekly study time data.
    Stores data in a JSON file partitioned by the user's login.
    """
    def __init__(self, login, storage_dir="storage"):
        """
        Initializes the tracker, sets up storage paths, and loads existing data.
       
        Args:
            login (str): The username used to name the data file.
            storage_dir (str): The directory where JSON files are stored.
        """
        self.filename = os.path.join(storage_dir, f"{login}_study_data.json")

        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir, exist_ok=True)

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
        """
        Reads the study data from the local JSON file.
        Returns:
            dict: The loaded data or default_data if the file is missing/corrupt.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    loaded_data = json.load(f)
                    return loaded_data if loaded_data else self.default_data
            except (json.JSONDecodeError, IOError) as e:
                print(f"[WeeklyStudyTracker] Error loading file: {e}")
                return self.default_data
        return self.default_data

    def save_to_disk(self):
        """Saves the current state of self.data to the JSON file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except (IOError, OSError, TypeError) as e:
            print(f"[WeeklyStudyTracker] Error saving file: {e}")

    def set_day(self, day, hours):
        """
        Overwrites the 'manual' input hours for a specific day.
        Args:
            day (str): The key (e.g., "Mon").
            hours (float): The amount of study time to set.
        """
        if day not in self.data:
            return
        try:
            hours = float(hours) if hours is not None else 0.0
            if hours < 0:
                hours = 0.0
        except (ValueError, TypeError):
            hours = 0.0
        if day in self.data and isinstance(self.data[day], dict):
            self.data[day]['manual'] = hours
            try:
                self.save_to_disk()
            except Exception as e:
                print(f"[WeeklyStudyTracker] Error saving after set_day: {e}")

    def add_time(self, day, hours):
        """
        Accumulates time onto the 'timer' record for a specific day.
        Args:
            day (str): The key (e.g., "Tue").
            hours (float): The amount of study time to add.
        """
        if day not in self.data:
            return
        try:
            hours = float(hours) if hours is not None else 0.0
            if hours < 0:
                hours = 0.0
        except (ValueError, TypeError):
            hours = 0.0
        if day in self.data and isinstance(self.data[day], dict):
            current_timer = self.data[day].get('timer', 0.0)
            try:
                current_timer = float(current_timer) if current_timer is not None else 0.0
            except (ValueError, TypeError):
                current_timer = 0.0
            self.data[day]['timer'] = current_timer + hours
            try:
                self.save_to_disk()
            except Exception as e:
                print(f"[WeeklyStudyTracker] Error saving after add_time: {e}")

    def reset_all(self):
        """
        Resets the study data for all days to zero.
        Uses a copy of default_data to ensure a clean state.
        """
        self.data = {k: v.copy() for k, v in self.default_data.items()}
        self.save_to_disk()

    def all(self):
        """
        Retrieves the entire study data dictionary.
       
        Returns:
            dict: The full study records.
        """
        return self.data