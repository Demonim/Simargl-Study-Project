import unittest
from unittest.mock import MagicMock, patch, mock_open

import json
import email
import hashlib
import os
import simargl 

class TestStudIP(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.login = "test_user"
        self.password = "secret_pass"
        self.base_url = "https://mock-url.com/"
        self.studip = simargl.StudIP(self.login, self.password, self.base_url)

    def test_init(self):
        """Test initialization of credentials and URL."""
        self.assertEqual(self.studip.login, self.login)
        self.assertEqual(self.studip.password, self.password)
        self.assertEqual(self.studip.base_url, self.base_url)

    @patch('simargl.studipy.Client')
    def test_create_client(self, MockClient):
        """Test that create_client initializes the studipy.Client correctly."""
        self.studip.create_client()
        
        # Verify studipy.Client was called with correct args
        MockClient.assert_called_once_with(self.login, self.password, self.base_url)
        # Verify self.client is set to the instance returned by MockClient
        self.assertEqual(self.studip.client, MockClient.return_value)

    def test_get_courses(self):
        """Test retrieval of courses via the client."""
        # Mock the client and the return value of get_courses
        self.studip.client = MagicMock()
        expected_courses = [{'title': 'Math 101'}, {'title': 'Physics 202'}]
        self.studip.client.Courses.get_courses.return_value = expected_courses

        result = self.studip.get_courses()

        self.studip.client.Courses.get_courses.assert_called_once()
        self.assertEqual(result, expected_courses)

    def test_get_my_messages(self):
        """Test retrieval of messages."""
        self.studip.client = MagicMock()
        expected_messages = [{'subject': 'Hello'}, {'subject': 'Exam'}]
        self.studip.client.Messages.get_messages.return_value = expected_messages

        result = self.studip.get_my_messages()

        self.studip.client.Messages.get_messages.assert_called_once()
        self.assertEqual(result, expected_messages)

    def test_new_messages_counter(self):
        """Test the counter for new unread messages."""
        self.studip.client = MagicMock()
        # Mock returning 3 unread messages
        fake_unread_msgs = ['msg1', 'msg2', 'msg3']
        self.studip.client.Messages.get_messages.return_value = fake_unread_msgs

        count = self.studip.new_messages_counter()

        # Verify it called get_messages with True (unread flag)
        self.studip.client.Messages.get_messages.assert_called_once_with(True)
        self.assertEqual(count, 3)

    def test_get_schedule(self):
        """Test retrieval of the schedule."""
        self.studip.client = MagicMock()
        expected_schedule = [{'event': 'Lecture'}, {'event': 'Lab'}]
        self.studip.client.Calendar.get_schedule.return_value = expected_schedule

        result = self.studip.get_schedule()

        self.studip.client.Calendar.get_schedule.assert_called_once()
        self.assertEqual(result, expected_schedule)

    def test_get_folders(self):
        """Test retrieving folders for a list of courses."""
        # Create a mock client to pass as argument
        mock_clnt = MagicMock()
        
        # Mock courses objects (can be simple strings or objects)
        courses = ['course_id_1', 'course_id_2']
        
        # Setup the side_effect to return different folders for different courses
        mock_clnt.Files.get_folders.side_effect = [['folder_A'], ['folder_B']]

        result = self.studip.get_folders(mock_clnt, courses)

        # Verify calls were made for each course
        self.assertEqual(mock_clnt.Files.get_folders.call_count, 2)
        mock_clnt.Files.get_folders.assert_any_call('course_id_1')
        mock_clnt.Files.get_folders.assert_any_call('course_id_2')
        
        # Verify structure of result list
        self.assertEqual(result, [['folder_A'], ['folder_B']])

    def test_get_files(self):
        """
        Test retrieving files for a list of courses.
        Note: The implementation in simargl.py calls `get_folders` inside `get_files`.
        """
        mock_clnt = MagicMock()
        courses = ['course_1']
        
        mock_clnt.Files.get_folders.return_value = ['file_object_1']

        result = self.studip.get_files(mock_clnt, courses)

        # Verify the code calls Files.get_folders as written in the source
        mock_clnt.Files.get_folders.assert_called_once_with('course_1')
        self.assertEqual(result, [['file_object_1']])


class TestECampusMail(unittest.TestCase):

    def setUp(self):
        self.login = "j.doe"
        self.password = "password123"
        self.server_addr = "mail.uni-test.de"
        self.mailer = simargl.ECampusMail(self.login, self.password, self.server_addr)

    def test_init(self):
        """Test that the username is correctly prefixed with 'ug-student\\'."""
        expected_login = "ug-student\\j.doe"
        self.assertEqual(self.mailer.login, expected_login)
        self.assertEqual(self.mailer.password, self.password)
        self.assertEqual(self.mailer.server, self.server_addr)

    @patch('imaplib.IMAP4_SSL')
    def test_read_email_init(self, mock_imap):
        """Test initializing the IMAP connection."""
        self.mailer.read_email_init()
        
        # Check connection to port 993
        mock_imap.assert_called_once_with(self.server_addr, 993)
        # Check login was called on the instance
        self.mailer.mail.login.assert_called_once_with(self.mailer.login, self.password)

    def test_clean_header_static(self):
        """Test the static method clean_header for different encodings."""
        # Test 1: None input
        self.assertEqual(simargl.ECampusMail.clean_header(None), "None")

        # Test 2: Simple ASCII
        self.assertEqual(simargl.ECampusMail.clean_header("Hello World"), "Hello World")

        # Test 3: Encoded header (Subject: =?utf-8?b?Tes...?=)
        # We simulate a typical encoded header object or string
        encoded_subject = email.header.Header("Tést", "utf-8").encode()
        decoded = simargl.ECampusMail.clean_header(encoded_subject)
        self.assertEqual(decoded, "Tést")

    def test_mail_notifications(self):
        """Test counting unread messages."""
        self.mailer.mail = MagicMock()
        
        # Mock search return: ('OK', [b'1 2 3 4 5']) -> 5 messages
        self.mailer.mail.search.return_value = ('OK', [b'1 2 3 4 5'])
        
        count = self.mailer.mail_notifications()
        
        self.mailer.mail.select.assert_called_with("inbox")
        self.mailer.mail.search.assert_called_with(None, "UNSEEN")
        self.assertEqual(count, 5)

    def test_show_subjects(self):
        """Test fetching recent email subjects and dates."""
        self.mailer.mail = MagicMock()
        
        # 1. Mock search to return 2 email IDs
        self.mailer.mail.search.return_value = ('OK', [b'101 102'])
        
        # 2. Mock fetch to return headers for these IDs
        # The structure of imaplib fetch return is complex. 
        # It returns a list of tuples (header_bytes, body_bytes) or just bytes.
        
        raw_email_1 = b"Subject: Test Email 1\r\nDate: Mon, 1 Jan 2024 10:00:00 +0000\r\n\r\n"
        raw_email_2 = b"Subject: Test Email 2\r\nDate: Invalid Date\r\n\r\n"
        
        # The code iterates over response_part in msg_data
        # Simulating the list returned by mail.fetch
        mock_fetch_data = [
            (b'101 (BODY...)', raw_email_1),
            b')', # imaplib sometimes includes closing parens as separate list items
            (b'102 (BODY...)', raw_email_2)
        ]
        
        self.mailer.mail.fetch.return_value = ('OK', mock_fetch_data)

        # Execute
        subjects, dates = self.mailer.show_subjects(2)

        # Assertions
        self.assertEqual(subjects, ["Test Email 1", "Test Email 2"])
        # First date should be parsed, second should be None (exception handling)
        self.assertIsNotNone(dates[0])
        self.assertIsNone(dates[1])

    def test_open_mail(self):
        """Test fetching full content of a specific email."""
        self.mailer.mail = MagicMock()
        # Mock IDs stored in the class (usually populated by a previous search)
        self.mailer.email_ids = [b'100', b'101']
        
        # Mock fetch return
        raw_email = b"Subject: Full Content\r\n\r\nBody text here."
        self.mailer.mail.fetch.return_value = ('OK', [(b'101 (RFC822)', raw_email)])
        
        # Access index 1 (ID b'101')
        msg = self.mailer.open_mail(1)
        
        self.mailer.mail.fetch.assert_called_with(b'101', "(RFC822)")
        self.assertEqual(msg['Subject'], "Full Content")
        self.assertEqual(msg.get_payload(), "Body text here.")

    @patch('smtplib.SMTP')
    def test_write_email_init(self, mock_smtp):
        """Test initializing SMTP connection."""
        self.mailer.write_email_init()
        
        mock_smtp.assert_called_with(self.server_addr, 587)
        instance = mock_smtp.return_value
        instance.starttls.assert_called_once()
        instance.login.assert_called_with(self.mailer.login, self.password)

    def test_send_email_no_attachment(self):
        """Test sending a simple text email."""
        self.mailer.server = MagicMock()
        
        self.mailer.send_email(
            text="Body Content",
            subject="Test Subject",
            sender="me@test.com",
            receiver="you@test.com"
        )
        
        # Verify sendmail was called
        self.mailer.server.sendmail.assert_called_once()
        args, _ = self.mailer.server.sendmail.call_args
        sender, receiver, msg_str = args
        
        self.assertEqual(sender, "me@test.com")
        self.assertEqual(receiver, "you@test.com")
        self.assertIn("Subject: Test Subject", msg_str)

    def test_send_email_with_attachment(self):
        """Test sending an email with a file attachment."""
        self.mailer.server = MagicMock()
        
        # Mock file opening to avoid needing a real file
        with patch("builtins.open", mock_open(read_data=b"file_content")) as mock_file:
            self.mailer.send_email(
                text="Body",
                subject="Subj",
                sender="me",
                receiver="you",
                filename="test.txt"
            )
            
            mock_file.assert_called_with("test.txt", "rb")
            
            # Check if sendmail was called
            self.mailer.server.sendmail.assert_called_once()
            # Check if the message contains the attachment filename in headers
            args, _ = self.mailer.server.sendmail.call_args
            msg_str = args[2]
            self.assertIn('filename= test.txt', msg_str)

    def test_close_connections(self):
        """Test safe closing of connections."""
        self.mailer.mail = MagicMock()
        self.mailer.smtp_conn = MagicMock() # The code checks for smtp_conn attribute
        
        # Inject smtp_conn manually to test the 'if hasattr' logic
        self.mailer.smtp_conn = MagicMock()
        
        self.mailer.close_conections()
        
        self.mailer.mail.logout.assert_called_once()
        self.mailer.smtp_conn.quit.assert_called_once()


class TestLoginStorage(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_db"
        self.login = "test_user"
        self.password = "secret_pass"
        self.expected_hash = hashlib.sha256(b"password").hexdigest()

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_init(self, mock_sql, mock_makedirs):
        """Test initialization of storage paths."""
        storage = simargl.LoginStorage(self.db_name)
        
        mock_makedirs.assert_called_with("storage", exist_ok=True)
        self.assertEqual(storage.file_path, os.path.join("storage", f"{self.db_name}.db"))

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_load_existing_table(self, mock_sql_connect, mock_makedirs):
        """Test loading when the users table exists."""
        storage = simargl.LoginStorage(self.db_name)
        mock_con = mock_sql_connect.return_value
        mock_cur = mock_con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself (chaining support)
        mock_cur.execute.return_value = mock_cur
        
        # Mock finding the table
        mock_cur.fetchone.return_value = ('users',) 
        
        result = storage.load()
        
        mock_cur.execute.assert_any_call("SELECT name FROM sqlite_master WHERE name='users'")
        mock_cur.execute.assert_any_call("SELECT * FROM users")
        self.assertIsNotNone(result)

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_load_no_table(self, mock_sql_connect, mock_makedirs):
        """Test loading when the users table does not exist."""
        storage = simargl.LoginStorage(self.db_name)
        mock_con = mock_sql_connect.return_value
        mock_cur = mock_con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself
        mock_cur.execute.return_value = mock_cur
        
        # Mock NOT finding the table
        mock_cur.fetchone.return_value = None
        
        result = storage.load()
        
        self.assertIsNone(result)

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_create_user(self, mock_sql_connect, mock_makedirs):
        """Test creating a new user and hashing password."""
        storage = simargl.LoginStorage(self.db_name)
        storage.con = mock_sql_connect.return_value
        storage.cur = storage.con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself
        storage.cur.execute.return_value = storage.cur

        storage.create(self.login, self.password)
        
        storage.cur.execute.assert_any_call("CREATE TABLE users (name TEXT, password TEXT, banned INTEGER)")
        
        expected_query = f"INSERT INTO users VALUES ('{self.login}','{self.expected_hash}',0)"
        storage.cur.execute.assert_any_call(expected_query)
        storage.con.commit.assert_called_once()

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_compare_existing_user(self, mock_sql_connect, mock_makedirs):
        """Test comparing credentials for an existing user."""
        storage = simargl.LoginStorage(self.db_name)
        storage.con = mock_sql_connect.return_value
        storage.cur = storage.con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself
        storage.cur.execute.return_value = storage.cur

        # Mock query returning a user
        storage.cur.fetchone.return_value = (self.login, self.expected_hash, 0)
        
        result = storage.compare(self.login, self.password)
        
        self.assertTrue(result)

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_compare_non_existent_user(self, mock_sql_connect, mock_makedirs):
        """Test comparing credentials for a new user (auto-register)."""
        storage = simargl.LoginStorage(self.db_name)
        storage.con = mock_sql_connect.return_value
        storage.cur = storage.con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself
        storage.cur.execute.return_value = storage.cur

        # Mock query returning None (user not found)
        storage.cur.fetchone.return_value = None
        
        result = storage.compare(self.login, self.password)
        
        self.assertFalse(result)
        
        expected_insert = f"INSERT INTO users VALUES ('{self.login}','{self.expected_hash}',0)"
        storage.cur.execute.assert_any_call(expected_insert)
        storage.con.commit.assert_called_once()

    @patch("simargl.os.makedirs")
    @patch("simargl.sql.connect")
    def test_un_ban_user_fixed(self, mock_sql_connect, mock_makedirs):
        """
        Test banning a user with the FIXED logic.
        Assumes code fixes: fetch[2] used for indexing, SQL quotes fixed.
        """
        storage = simargl.LoginStorage(self.db_name)
        storage.con = mock_sql_connect.return_value
        storage.cur = storage.con.cursor.return_value
        
        # FIX: Ensure execute() returns the cursor itself
        storage.cur.execute.return_value = storage.cur

        # Mock fetchone to return a single tuple: (name, password, banned_status)
        # 0 = not banned
        storage.cur.fetchone.return_value = (self.login, self.expected_hash, 0)
        
        result = storage.un_ban(self.login, self.password)
        
        # Should return True because we flipped 0 -> 1 (Banned)
        self.assertTrue(result) 
        
        # Verify Update call has the CLOSING QUOTE now
        expected_update = f"UPDATE users SET banned=1 WHERE name='{self.login}' AND password='{self.expected_hash}'"
        storage.cur.execute.assert_called_with(expected_update)


class TestNotesStorage(unittest.TestCase):

    def setUp(self):
        self.login = "test_user"
        self.storage = simargl.NotesStorage(self.login)
        self.expected_path = os.path.join("storage/data", f"{self.login}.json")

    @patch("simargl.os.makedirs")
    def test_init(self, mock_makedirs):
        """Test initialization creates the directory structure."""
        # Re-initialize to capture the makedirs call
        s = simargl.NotesStorage("new_user")
        mock_makedirs.assert_called_with("storage/data", exist_ok=True)
        self.assertEqual(s.file_path, os.path.join("storage/data", "new_user.json"))

    @patch("simargl.os.path.exists")
    def test_load_notes_file_exists(self, mock_exists):
        """Test loading notes when the file exists."""
        mock_exists.return_value = True
        
        # JSON content to simulate
        file_content = json.dumps({"notes": [{"id": "1", "title": "Test Note"}]})
        
        with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
            notes = self.storage.load_notes()
            
            mock_file.assert_called_with(self.expected_path, "r", encoding="utf-8")
            self.assertEqual(len(notes), 1)
            self.assertEqual(notes[0]['title'], "Test Note")

    @patch("simargl.os.path.exists")
    def test_load_notes_no_file(self, mock_exists):
        """Test loading notes when the file does NOT exist."""
        mock_exists.return_value = False
        
        # Should not attempt to open a file
        with patch("builtins.open", mock_open()) as mock_file:
            notes = self.storage.load_notes()
            
            mock_file.assert_not_called()
            self.assertEqual(notes, [])

    def test_save_notes(self):
        """Test saving notes to a JSON file."""
        notes_data = [{"id": "1", "title": "New Note"}]
        
        with patch("builtins.open", mock_open()) as mock_file:
            self.storage.save_notes(notes_data)
            
            mock_file.assert_called_with(self.expected_path, "w", encoding="utf-8")
            
            # Check if json.dump wrote the correct structure
            # We combine the written chunks to verify the JSON string
            handle = mock_file()
            # This captures all write calls (e.g. '{"notes": ', '...', '}')
            written_content = "".join(call.args[0] for call in handle.write.call_args_list)
            
            # Verify the key "notes" is in the output
            self.assertIn('"notes":', written_content)
            self.assertIn('New Note', written_content)

    @patch("simargl.uuid.uuid4")
    @patch("simargl.datetime.datetime")
    def test_create_note(self, mock_datetime, mock_uuid):
        """Test creating a note dictionary."""
        # Mock UUID
        mock_uuid.return_value = "1234-5678"
        # Mock Datetime
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2024-01-01 12:00"
        mock_datetime.now.return_value = mock_now

        note = self.storage.create_note("My Title", "My Content")

        self.assertEqual(note['id'], "1234-5678")
        self.assertEqual(note['title'], "My Title")
        self.assertEqual(note['content'], "My Content")
        self.assertEqual(note['created'], "2024-01-01 12:00")


class TestCourseDaysStorage(unittest.TestCase):

    def setUp(self):
        self.login = "test_user"
        self.storage = simargl.CourseDaysStorage(self.login)
        self.expected_path = f"storage/course_days_{self.login}.json"

    def test_init(self):
        self.assertEqual(self.storage.path, self.expected_path)

    @patch("simargl.os.path.exists")
    def test_load_exists(self, mock_exists):
        """Test loading course days when file exists."""
        mock_exists.return_value = True
        
        fake_data = {"Math": "Monday", "Science": "Friday"}
        json_data = json.dumps(fake_data)
        
        with patch("builtins.open", mock_open(read_data=json_data)) as mock_file:
            result = self.storage.load()
            
            mock_file.assert_called_with(self.expected_path, "r", encoding="utf-8")
            self.assertEqual(result, fake_data)

    @patch("simargl.os.path.exists")
    def test_load_not_exists(self, mock_exists):
        """Test loading returns empty dict if file missing."""
        mock_exists.return_value = False
        
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.storage.load()
            
            mock_file.assert_not_called()
            self.assertEqual(result, {})

    def test_save(self):
        """Test saving course days data."""
        data_to_save = {"History": "Tuesday"}
        
        with patch("builtins.open", mock_open()) as mock_file:
            self.storage.save(data_to_save)
            
            mock_file.assert_called_with(self.expected_path, "w", encoding="utf-8")
            
            # check the write content
            handle = mock_file()
            written = "".join(call.args[0] for call in handle.write.call_args_list)
            
            self.assertIn("History", written)
            self.assertIn("Tuesday", written)


if __name__ == '__main__':
    unittest.main()