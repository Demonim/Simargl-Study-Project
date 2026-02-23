import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call
from collections import namedtuple

from PySide6.QtWidgets import QApplication, QLineEdit, QCheckBox, QPushButton, QListWidget, QComboBox
from PySide6.QtCore import Qt

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Initialize QApplication once for the entire test suite
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

import main     

# Dummy objects for mocking
DummyCourse = namedtuple('DummyCourse', ['course_id', 'title', 'subtitle'])
DummyEntry = namedtuple('DummyEntry', ['start', 'end', 'title', 'related_course_id'])

class TestMainGUIHelperFunctions(unittest.TestCase):

    def setUp(self):
        main.current_theme_name = "Dark Theme"

    def test_get_plot_colors(self):
        main.current_theme_name = "Dark Theme"
        self.assertEqual(main.get_plot_colors(), 'white')
        
        main.current_theme_name = "Light Theme"
        self.assertEqual(main.get_plot_colors(), 'black')

    @patch('main.QApplication.setStyleSheet')
    def test_change_theme(self, mock_set_style):
        # Mock QApplication.instance() to avoid overwriting the real one's style in tests
        mock_app = MagicMock()
        main.change_theme(mock_app, "Dark Theme")
        mock_app.setStyleSheet.assert_called_once()
        self.assertEqual(main.current_theme_name, "Dark Theme")

    @patch('main.QTimer')
    def test_setup_auto_logout(self, MockTimer):
        mock_window = MagicMock()
        mock_timer_instance = MockTimer.return_value
        
        main.setup_auto_logout(mock_window)
        
        MockTimer.assert_called_with(mock_window)
        mock_timer_instance.setSingleShot.assert_called_with(True)
        mock_timer_instance.timeout.connect.assert_called_with(main.universal_logout)
        mock_timer_instance.start.assert_called_with(300000)


@patch('main.load_ui')
class TestMainWindowsAndNavigation(unittest.TestCase):
    """
    Tests the window opening functions by mocking load_ui so we don't need real .ui files.
    """
    def setUp(self):
        # Setup global mocks for simargl interactions
        main.current_login = "testuser"
        main.ecampusmail = MagicMock()
        main.studip = MagicMock()
        main.notes_storage = MagicMock()
        main.schedule = MagicMock()
        main.user_courses = [DummyCourse("1", "Math", "101"), DummyCourse("2", "Physics", "102")]

        self.mock_prev_window = MagicMock()

    def create_mock_window(self):
        window = MagicMock()
        mock_child = MagicMock()
        # Provide an int return for grid.count() so range() doesn't throw a TypeError
        mock_child.count.return_value = 0  
        mock_child.findChild.return_value = mock_child
        window.findChild.return_value = mock_child
        return window

    def test_open_menu(self, mock_load_ui):
        mock_window = self.create_mock_window()
        mock_load_ui.return_value = mock_window
        
        main.open_menu(self.mock_prev_window)
        
        mock_load_ui.assert_called_with("UI/menu.ui")
        mock_window.show.assert_called_once()
        self.mock_prev_window.close.assert_called_once()
        self.assertEqual(self.mock_prev_window.menu_window, mock_window)

    def test_open_courses(self, mock_load_ui):
        mock_window = self.create_mock_window()
        mock_load_ui.return_value = mock_window
        
        main.open_courses(self.mock_prev_window)
        
        mock_load_ui.assert_called_with("UI/courses.ui")
        mock_window.show.assert_called_once()

    def test_open_calendar(self, mock_load_ui):
        mock_window = self.create_mock_window()
        mock_load_ui.return_value = mock_window
        main.schedule.entries = []
        
        with patch('main.simargl.CourseDaysStorage') as MockStorage:
            MockStorage.return_value.load.return_value = {"Math": "MO"}
            main.open_calendar(self.mock_prev_window)
            
        mock_window.show.assert_called_once()

    @patch('main.load_ecampus_mail_data')
    def test_open_Email(self, mock_load_data, mock_load_ui):
        mock_window = self.create_mock_window()
        mock_load_ui.return_value = mock_window
        
        main.open_Email(self.mock_prev_window)
        
        mock_load_ui.assert_called_with("UI/Email.ui")
        mock_load_data.assert_called_with(mock_window)
        mock_window.show.assert_called_once()

    def test_open_Notes(self, mock_load_ui):
        mock_window = self.create_mock_window()
        mock_load_ui.return_value = mock_window
        main.notes_storage.load_notes.return_value = [{"title": "Test", "content": "Body"}]
        
        main.open_Notes(self.mock_prev_window)
        
        mock_load_ui.assert_called_with("UI/notes.ui")
        mock_window.show.assert_called_once()

    @patch('main.QMessageBox.information')
    def test_universal_logout(self, mock_msg_box, mock_load_ui):
        mock_prelogin = self.create_mock_window()
        mock_load_ui.return_value = mock_prelogin
        main.prelogin_window = None
        main.current_active_window = MagicMock()
        
        main.universal_logout()
        
        mock_prelogin.show.assert_called_once()
        mock_msg_box.assert_called_once()
        self.assertEqual(main.current_active_window, mock_prelogin)


class TestDialogsAndModals(unittest.TestCase):
    
    def test_AddNoteDialog(self):
        dialog = main.AddNoteDialog()
        dialog.line_edit.setText("My New Note")
        self.assertEqual(dialog.get_name(), "My New Note")

    def test_DayScheduleDialog(self):
        entries = [DummyEntry("10:00", "12:00", "Math", "1")]
        dialog = main.DayScheduleDialog("Monday", entries)
        self.assertEqual(dialog.list.count(), 1)
        self.assertIn("Math", dialog.list.item(0).text())

    @patch('main.simargl.CourseDaysStorage')
    def test_CourseDayDialog(self, mock_storage_class):
        mock_storage = mock_storage_class.return_value
        mock_storage.load.return_value = {"Math": "MO"}
        
        courses = [DummyCourse("1", "Math", "101"), DummyCourse("2", "Physics", "102")]
        
        dialog = main.CourseDayDialog(courses, mock_storage)
        self.assertEqual(dialog.list.count(), 2)
        
        # Test Save
        dialog.inputs["1"].setText("TU")
        dialog.inputs["2"].setText("WE")
        
        # Prevent actual close
        with patch.object(dialog, 'accept'):
            dialog.save_and_close()
            mock_storage.save.assert_called_with({"1": "TU", "2": "WE"})

    @patch('main.load_ui')
    @patch('main.QMessageBox.warning')
    def test_handle_auth_invalid(self, mock_warn, mock_load_ui):
        mock_window = MagicMock()
        mock_window.findChild.return_value.text.return_value = "" # Empty login
        
        main.handle_auth(mock_window, MagicMock())
        mock_warn.assert_called_once()

    @patch('main.load_ui')
    @patch('main.start_main_app')
    def test_handle_auth_user(self, mock_start_app, mock_load_ui):
        mock_window = MagicMock()
        mock_window.findChild.return_value.text.return_value = "user"
        
        mock_storage = MagicMock()
        mock_storage.compare.return_value = True
        mock_storage.cur.fetchone.return_value = (0, 0) # Not banned, not admin
        
        main.handle_auth(mock_window, mock_storage)
        mock_start_app.assert_called_with(mock_window)

    @patch('main.load_ui')
    @patch('main.open_admin')
    def test_handle_auth_admin(self, mock_open_admin, mock_load_ui):
        mock_window = MagicMock()
        mock_window.findChild.return_value.text.return_value = "admin"
        
        mock_storage = MagicMock()
        mock_storage.compare.return_value = True
        mock_storage.cur.fetchone.return_value = (0, 1) # Not banned, IS admin
        
        main.handle_auth(mock_window, mock_storage)
        mock_open_admin.assert_called_with(mock_window)


class TestDashboardLogic(unittest.TestCase):
    @patch('main.refresh_stacked_bar')
    @patch('main.apply_bar_theme')
    def test_save_tracker_data(self, mock_apply_theme, mock_refresh):
        mock_window = MagicMock()
        mock_line_edit = MagicMock()
        mock_line_edit.text.return_value = "5"
        mock_window.findChild.return_value = mock_line_edit
        
        mock_canvas = MagicMock()
        
        main.save_tracker_data(mock_window, mock_canvas, "Dark Theme")
        
        expected_inputs = [
            ('Mon', '5', '5'), ('Tue', '5', '5'), ('Wed', '5', '5'), 
            ('Thu', '5', '5'), ('Fri', '5', '5'), ('Sat', '5', '5'), ('Sun', '5', '5')
        ]
        
        mock_refresh.assert_called_with(mock_canvas, manual_inputs=expected_inputs)
        mock_apply_theme.assert_called_with(mock_canvas, "Dark Theme")
        mock_canvas.draw.assert_called_once()

    @patch('main.stop_study_session')
    @patch('main.refresh_stacked_bar')
    @patch('main.apply_bar_theme')
    def test_stop_timer_and_save(self, mock_apply_theme, mock_refresh, mock_stop_session):
        main.study_timer.running = True
        main.active_timer_day = "Mon"
        
        with patch.object(main.study_timer, 'stop'), patch.object(main.study_timer, 'reset'):
            main.study_timer.start_time = None  # defaults session_hours calculation to 0.0
            
            mock_canvas = MagicMock()
            main.stop_timer_and_save(mock_canvas, "Light Theme")
            
            mock_stop_session.assert_called_with("Mon", 0.0)
            mock_refresh.assert_called_with(mock_canvas)
            mock_canvas.draw.assert_called_once()
            self.assertIsNone(main.active_timer_day)

if __name__ == '__main__':
    unittest.main()