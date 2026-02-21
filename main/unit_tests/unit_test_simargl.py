import unittest
from unittest.mock import patch, MagicMock, call
import os
import json
import sqlite3
import shutil
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import simargl
from simargl import StudIP, ECampusMail, LoginStorage, NotesStorage, CourseDaysStorage

class TestStudIP(unittest.TestCase):
    def setUp(self):
        self.studip = StudIP("test_user", "test_pass")

    def test_init(self):
        self.assertEqual(self.studip.login, "test_user")
        self.assertEqual(self.studip.password, "test_pass")
        self.assertEqual(self.studip.base_url, "https://studip.uni-goettingen.de/")

    @patch('simargl.studipy.Client')
    def test_create_client(self, MockClient):
        self.studip.create_client()
        MockClient.assert_called_once_with("test_user", "test_pass", "https://studip.uni-goettingen.de/")
        self.assertIsNotNone(self.studip.client)

    def test_get_courses(self):
        self.studip.client = MagicMock()
        self.studip.client.Courses.get_courses.return_value = ["course1", "course2"]
        result = self.studip.get_courses()
        self.assertEqual(result, ["course1", "course2"])

    def test_get_my_messages(self):
        self.studip.client = MagicMock()
        self.studip.client.Messages.get_messages.return_value = ["msg1", "msg2"]
        result = self.studip.get_my_messages()
        self.assertEqual(result, ["msg1", "msg2"])

    def test_new_messages_counter(self):
        self.studip.client = MagicMock()
        self.studip.client.Messages.get_messages.return_value = ["new_msg1"]
        result = self.studip.new_messages_counter()
        self.studip.client.Messages.get_messages.assert_called_with(True)
        self.assertEqual(result, 1)

    def test_get_schedule(self):
        self.studip.client = MagicMock()
        self.studip.client.Calendar.get_schedule.return_value = ["event1"]
        result = self.studip.get_schedule()
        self.assertEqual(result, ["event1"])

    def test_get_folders(self):
        self.studip.client = MagicMock()
        self.studip.client.Files.get_folders.side_effect = ["folder_data_1", "folder_data_2"]
    
        result = self.studip.get_folders(["course1", "course2"])
        
        self.assertEqual(result, ["folder_data_1", "folder_data_2"])
        self.assertEqual(self.studip.client.Files.get_folders.call_count, 2)

    def test_get_files(self):
        self.studip.client = MagicMock()
        self.studip.client.Files.get_files.side_effect = ["file_data_1", "file_data_2"]
        
        result = self.studip.get_files(["course1", "course2"])
        
        self.assertEqual(result, ["file_data_1", "file_data_2"])
        self.assertEqual(self.studip.client.Files.get_files.call_count, 2)


class TestECampusMail(unittest.TestCase):
    def setUp(self):
        self.mail = ECampusMail("john.doe", "password123")

    def test_init(self):
        self.assertEqual(self.mail.login, "ug-student\\john.doe")
        self.assertEqual(self.mail.password, "password123")
        self.assertEqual(self.mail.server, "email.stud.uni-goettingen.de")

    @patch('simargl.imaplib.IMAP4_SSL')
    def test_read_email_init(self, MockIMAP):
        mock_imap_instance = MockIMAP.return_value
        self.mail.read_email_init()
        MockIMAP.assert_called_once_with("email.stud.uni-goettingen.de", 993)
        mock_imap_instance.login.assert_called_once_with("ug-student\\john.doe", "password123")

    def test_clean_header(self):
        # Test empty header
        self.assertEqual(self.mail.clean_header(None), "None")
        # Test simple string
        self.assertEqual(self.mail.clean_header("Simple Subject"), "Simple Subject")

    def test_mail_notifications(self):
        self.mail.mail = MagicMock()
        self.mail.mail.search.return_value = ("OK", [b"1 2 3"])
        result = self.mail.mail_notifications()
        self.mail.mail.select.assert_called_with("inbox")
        self.mail.mail.search.assert_called_with(None, "UNSEEN")
        self.assertEqual(result, 3)

    @patch('simargl.email.message_from_bytes')
    def test_show_subjects(self, mock_msg_from_bytes):
        self.mail.mail = MagicMock()
        # Mock search to return 3 email IDs
        self.mail.mail.search.return_value = ("OK", [b"10 11 12"])
        
        # Mock fetch response (simplified structure to bypass tuple unpacking loop)
        self.mail.mail.fetch.return_value = ("OK", [(b'12 (RFC822)', b'dummy_bytes')])
        
        # Mock the parsed email message
        mock_msg = MagicMock()
        mock_msg.__getitem__.side_effect = lambda key: "Test Subject" if key == "Subject" else "Thu, 19 Feb 2026 08:00:00 +0000"
        mock_msg_from_bytes.return_value = mock_msg

        subjects, dates = self.mail.show_subjects(1)
        
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0], "Test Subject")
        self.assertIsNotNone(dates[0])

    @patch('simargl.email.message_from_bytes')
    def test_open_mail(self, mock_msg_from_bytes):
        self.mail.mail = MagicMock()
        self.mail.email_ids = [b"1", b"2"]
        self.mail.mail.fetch.return_value = ("OK", [[None, b"raw_email_data"]])
        
        mock_msg_from_bytes.return_value = "ParsedEmailObject"
        
        result = self.mail.open_mail(1)
        self.mail.mail.fetch.assert_called_with(b"2", "(RFC822)")
        self.assertEqual(result, "ParsedEmailObject")

    @patch('simargl.smtplib.SMTP')
    def test_write_email_init(self, MockSMTP):
        mock_smtp_instance = MockSMTP.return_value
        self.mail.write_email_init()
        MockSMTP.assert_called_once_with("email.stud.uni-goettingen.de", 587)
        self.assertEqual(mock_smtp_instance.ehlo.call_count, 2)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with("ug-student\\john.doe", "password123")

    @patch('simargl.email.mime.multipart.MIMEMultipart')
    def test_send_email_no_attachment(self, MockMultipart):
        self.mail.server = MagicMock()
        self.mail.send_email("Body text", "Subject", "sender@test.com", "receiver@test.com")
        self.mail.server.sendmail.assert_called_once()

    def test_close_connections(self):
        self.mail.mail = MagicMock()
        self.mail.smtp_conn = MagicMock()
        self.mail.close_conections()
        self.mail.mail.logout.assert_called_once()
        self.mail.smtp_conn.quit.assert_called_once()


class TestLoginStorage(unittest.TestCase):
    def setUp(self):
        self.test_db_name = "test_users_db"
        self.storage = LoginStorage(self.test_db_name)

    def tearDown(self):
        # Close connection and remove test database file
        self.storage.con.close()
        if os.path.exists(self.storage.file_path):
            os.remove(self.storage.file_path)

    def test_create_table(self):
        # Table is created in __init__, let's verify it exists
        self.storage.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        self.assertIsNotNone(self.storage.cur.fetchone())

    def test_generate_unique_id(self):
        uid = self.storage.generate_unique_id()
        self.assertTrue(uid.isdigit())
        self.assertEqual(len(uid), 10)

    def test_create_and_user_exists(self):
        self.assertTrue(self.storage.create("newuser", "pass", "Real Name"))
        self.assertTrue(self.storage.user_exists("newuser"))
        self.assertFalse(self.storage.user_exists("nonexistent"))
        # Test unique constraint
        self.assertFalse(self.storage.create("newuser", "pass2", "Another Name"))

    def test_compare(self):
        self.storage.create("testlogin", "mypassword", "John")
        self.assertTrue(self.storage.compare("testlogin", "mypassword"))
        self.assertFalse(self.storage.compare("testlogin", "wrongpass"))

    def test_load(self):
        self.storage.create("user1", "pass", "User One")
        self.storage.create("user2", "pass", "User Two", is_admin=1)
        users = list(self.storage.load())
        self.assertEqual(len(users), 1) # Should only load non-admins
        self.assertEqual(users[0][1], "user1")

    def test_set_ban_status(self):
        self.storage.create("banuser", "pass", "To Be Banned")
        self.storage.set_ban_status("banuser", 1)
        
        self.storage.cur.execute("SELECT banned FROM users WHERE login='banuser'")
        result = self.storage.cur.fetchone()
        self.assertEqual(result[0], 1)


class TestNotesStorage(unittest.TestCase):
    def setUp(self):
        self.login = "test_notes_user"
        self.storage = NotesStorage(self.login)

    def tearDown(self):
        if os.path.exists(self.storage.file_path):
            os.remove(self.storage.file_path)
        # Safely attempt to remove the test storage dir if empty
        try:
            os.rmdir("storage/data")
            os.rmdir("storage")
        except OSError:
            pass 

    def test_create_note(self):
        note = self.storage.create_note("Title", "Content")
        self.assertIn("id", note)
        self.assertEqual(note["title"], "Title")
        self.assertEqual(note["content"], "Content")
        self.assertIn("created", note)

    def test_save_and_load_notes(self):
        # Initially empty
        self.assertEqual(self.storage.load_notes(), [])
        
        # Save and load
        note = self.storage.create_note("Test", "Data")
        self.storage.save_notes([note])
        
        loaded = self.storage.load_notes()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Test")


class TestCourseDaysStorage(unittest.TestCase):
    def setUp(self):
        self.login = "test_course_user"
        abs_storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'storage'))
        self.storage = CourseDaysStorage(self.login, storage_dir=abs_storage_dir)

    def tearDown(self):
        if os.path.exists(self.storage.path):
            os.remove(self.storage.path)

    def test_save_and_load(self):
        # Initially empty
        self.assertEqual(self.storage.load(), {})
        
        # Save data
        test_data = {"Math": "Monday", "Science": "Wednesday"}
        self.storage.save(test_data)
        
        # Load data
        loaded_data = self.storage.load()
        self.assertEqual(loaded_data, test_data)

if __name__ == '__main__':
    unittest.main()