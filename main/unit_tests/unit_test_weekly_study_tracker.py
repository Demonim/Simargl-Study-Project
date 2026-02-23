import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from dashboard.timer_bar.weekly_study_tracker import WeeklyStudyTracker

class TestWeeklyStudyTracker(unittest.TestCase):
    # Unit tests for WeeklyStudyTracker class
    def setUp(self):
        # Prepare test environment before each test
        self.login = "testuser"
        self.storage_dir = "test_storage"
        abs_storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'storage'))
        self.filename = os.path.join(abs_storage_dir, f"{self.login}_study_data.json")
        # Remove any leftover test files/directories
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(abs_storage_dir):
            try:
                os.rmdir(abs_storage_dir)
            except OSError:
                pass

    def tearDown(self):
        # Clean up test environment after each test
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.storage_dir):
            try:
                os.rmdir(self.storage_dir)
            except OSError:
                pass

    def test_load_from_missing_file(self):
        # Test loading tracker when file is missing (should use default data)
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker.data, tracker.default_data)

    def test_save_and_load(self):
        # Test saving and loading tracker data
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Mon", 2.5)
        tracker2 = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker2.data["Mon"]["manual"], 2.5)

    def test_set_day_invalid_input(self):
        # Test setting invalid manual input (string and negative)
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Mon", "bad")
        self.assertEqual(tracker.data["Mon"]["manual"], 0.0)
        tracker.set_day("Mon", -5)
        self.assertEqual(tracker.data["Mon"]["manual"], 0.0)

    def test_add_time(self):
        # Test adding timer hours (valid, invalid, negative)
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.add_time("Tue", 1.5)
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)
        tracker.add_time("Tue", "bad")
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)
        tracker.add_time("Tue", -2)
        self.assertEqual(tracker.data["Tue"]["timer"], 1.5)

    def test_reset_all(self):
        # Test resetting all data to default
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        tracker.set_day("Wed", 3)
        tracker.add_time("Wed", 2)
        tracker.reset_all()
        self.assertEqual(tracker.data, tracker.default_data)

    @patch("builtins.open", new_callable=mock_open, read_data="not json")
    def test_load_from_corrupt_file(self, mock_file):
        # Test loading from a corrupt file (should fallback to default)
        os.makedirs(self.storage_dir, exist_ok=True)
        with open(self.filename, "w") as f:
            f.write("not json")
        tracker = WeeklyStudyTracker(self.login, self.storage_dir)
        self.assertEqual(tracker.data, tracker.default_data)

if __name__ == "__main__":
    unittest.main()
