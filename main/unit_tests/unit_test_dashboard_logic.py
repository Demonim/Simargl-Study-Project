import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from dashboard.dashboard_logic import *

class TestDashboardLogic(unittest.TestCase):
    # Unit tests for dashboard logic functions
    def test_get_pie_chart_none(self):
        # Test pie chart generation with None input (should return error chart)
        fig = get_pie_chart(None)
        self.assertTrue(hasattr(fig, 'axes'))

    @patch('main.dashboard.dashboard_logic.subject_hours', side_effect=Exception('fail'))
    def test_get_pie_chart_exception(self, mock_subject_hours):
        # Test pie chart generation when subject_hours raises exception
        fig = get_pie_chart('dummy')
        self.assertTrue(hasattr(fig, 'axes'))

    def test_get_scatter_plot_exception(self):
        # Test scatter plot generation with invalid input (should return error chart)
        fig = get_scatter_plot([])
        self.assertTrue(hasattr(fig, 'axes'))

    def test_get_heatmap_none(self):
        # Test heatmap generation with None input (should return error chart)
        fig = get_heatmap(None)
        self.assertTrue(hasattr(fig, 'axes'))

    @patch('main.dashboard.dashboard_logic.create_heatmap', side_effect=Exception('fail'))
    def test_get_heatmap_exception(self, mock_create_heatmap):
        # Test heatmap generation when create_heatmap raises exception
        class DummyMail:
            # Dummy mail class for testing
            def show_subjects(self, last_n=300):
                return [], []
        fig = get_heatmap(DummyMail())
        self.assertTrue(hasattr(fig, 'axes'))

    def test_process_manual_input_invalid(self):
        # Test manual input processing with invalid input (should return dict)
        _tracker = MagicMock()
        result = process_manual_input(None)
        self.assertIsInstance(result, dict)
        result = process_manual_input([('Mon', None, None)])
        self.assertIsInstance(result, dict)

    def test_stop_study_session_invalid(self):
        # Test stop_study_session with invalid day_code and hours
        _tracker = MagicMock()
        _tracker.all.return_value = {}
        result = stop_study_session(None, 2)
        self.assertIsInstance(result, dict)
        result = stop_study_session('Mon', 'bad')
        self.assertIsInstance(result, dict)

    def test_clear_all_data(self):
        # Test clearing all tracker data
        _tracker = MagicMock()
        get_tracker_data = MagicMock(return_value={})
        result = clear_all_data()
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
