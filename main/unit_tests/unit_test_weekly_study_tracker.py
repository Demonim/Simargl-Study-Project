import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from main.dashboard.timer_bar.weekly_study_tracker import WeeklyStudyTracker

class TestWeeklyStudyTracker(unittest.TestCase):
    def setUp(self):
        self.login = "testuser"
        self.storage_dir = "test_storage"
        self.filename = os.path.join(self.storage_dir, f"{self.login}_study_data.json")
        # Ensure test storage dir is clean
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.storage_dir):
            try:
                os.rmdir(self.storage_dir)
            except OSError:
                pass

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.storage_dir):
            try:
                os.rmdir(self.storage_dir)
            except OSError:
                pass

    def test_load_from_missing_file(self):
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker.data, tracker.default_data)

    def test_save_and_load(self):
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Mon", 2.5)
        tracker2 = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker2.data["Mon"]["manual"], 2.5)

    def test_set_day_invalid_input(self):
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Mon", "bad")
        self.assertEqual(tracker.data["Mon"]["manual"], 0.0)
        tracker.set_day("Mon", -5)
        self.assertEqual(tracker.data["Mon"]["manual"], 0.0)

    def test_add_time(self):
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.add_time("Tue", 1.5)
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)
        tracker.add_time("Tue", "bad")
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)
        tracker.add_time("Tue", -2)
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)

    def test_reset_all(self):
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Wed", 3)
        tracker.add_time("Wed", 2)
        tracker.reset_all()
        self.assertEqual(tracker.data, tracker.default_data)

    @patch("builtins.open", new_callable=mock_open, read_data="not json")
    def test_load_from_corrupt_file(self, mock_file):
        os.makedirs(self.storage_dir, exist_ok=True)
        with open(self.filename, "w") as f:
            f.write("not json")
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker.data, tracker.default_data)

if __name__ == "__main__":
    unittest.main()
