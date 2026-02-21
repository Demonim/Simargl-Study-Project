import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from ..dashboard.dashboard_logic import *

class TestDashboardLogic(unittest.TestCase):
    def test_get_pie_chart_none(self):
        fig = get_pie_chart(None)
        self.assertTrue(hasattr(fig, 'axes'))

    @patch('main.dashboard.dashboard_logic.subject_hours', side_effect=Exception('fail'))
    def test_get_pie_chart_exception(self, mock_subject_hours):
        fig = get_pie_chart('dummy')
        self.assertTrue(hasattr(fig, 'axes'))

    def test_get_scatter_plot_exception(self):
        # subject_data is not set, should raise and return error_chart
        fig = get_scatter_plot([])
        self.assertTrue(hasattr(fig, 'axes'))

    def test_get_heatmap_none(self):
        fig = get_heatmap(None)
        self.assertTrue(hasattr(fig, 'axes'))

    @patch('main.dashboard.dashboard_logic.create_heatmap', side_effect=Exception('fail'))
    def test_get_heatmap_exception(self, mock_create_heatmap):
        class DummyMail:
            def show_subjects(self, last_n=300):
                return [], []
        fig = get_heatmap(DummyMail())
        self.assertTrue(hasattr(fig, 'axes'))

    def test_process_manual_input_invalid(self):
        _tracker = MagicMock()
        result = process_manual_input(None)
        self.assertIsInstance(result, dict)
        result = process_manual_input([('Mon', None, None)])
        self.assertIsInstance(result, dict)

    def test_stop_study_session_invalid(self):
        _tracker = MagicMock()
        _tracker.all.return_value = {}
        result = stop_study_session(None, 2)
        self.assertIsInstance(result, dict)
        result = stop_study_session('Mon', 'bad')
        self.assertIsInstance(result, dict)

    def test_clear_all_data(self):
        _tracker = MagicMock()
        get_tracker_data = MagicMock(return_value={})
        result = clear_all_data()
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
