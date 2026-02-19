import studipy

import imaplib
import email
import email.mime.multipart
import email.mime.text
import email.mime.base
import email.encoders
import smtplib

import os
import json
import uuid
import datetime
import random

import sqlite3 as sql
import hashlib


BASE_URL = "https://studip.uni-goettingen.de/"
SERVER = "email.stud.uni-goettingen.de"


class StudIP:
    """
    A controller class for interacting with the Stud.IP learning management system.

    This class serves as a wrapper around the `studipy` library to handle user 
    authentication and retrieve academic data such as registered courses, 
    messages, schedules, and course files.
    """

    def __init__(self, login, password, base_url=BASE_URL):
        """
        Initialize the StudIP handler with user credentials.

        Args:
            login (str): The user's login username.
            password (str): The user's password.
            base_url (str, optional): The base URL of the Stud.IP instance. 
                                      Defaults to the University of Goettingen URL.
        """

        self.login = login
        self.password = password
        self.base_url = base_url

    def create_client(self):
        """
        Establishes the connection to Stud.IP by creating a studipy Client instance.
        
        This method must be called before attempting to fetch data (courses, messages, etc.).
        """

        self.client = studipy.Client(self.login, self.password, self.base_url)

    def get_courses(self):
        """
        Retrieves the list of courses the user is enrolled in.

        Returns:
            list: A collection of course objects/dictionaries returned by the API.
        """

        courses = self.client.Courses.get_courses()
        return courses

    def get_my_messages(self):
        """
        Retrieves all messages from the user's inbox.

        Returns:
            list: A list of message objects.
        """

        my_messages = self.client.Messages.get_messages()
        return my_messages

    def new_messages_counter(self):
        """
        Counts the number of unread (new) messages.

        Returns:
            int: The count of unread messages.
        """

        new_messages = self.client.Messages.get_messages(True)
        return len(new_messages)

    def get_schedule(self):
        """
        Retrieves the user's personal schedule/calendar.

        Returns:
            list: A list of schedule entries or calendar events.
        """

        schedule = self.client.Calendar.get_schedule()
        return schedule

    def get_folders(self, courses):
        """
        Retrieves document folders for a specific list of courses.

        Args:
            courses (list): A list of course objects to fetch folders for.

        Returns:
            list: A list containing folder structures for the provided courses.
        """

        folders = []
        for element in range(len(courses)):
            folders.append(self.client.Files.get_folders(courses[element]))
        return folders

    def get_files(self, courses):
        """
        Retrieves files contained within the course folders.

        Args:
            courses (list): A list of course objects to fetch folders for.

        Returns:
            list: A list of file objects associated with the courses.
        """

        files = []
        for element in range(len(courses)):
            files.append(self.client.Files.get_files(courses[element]))
        return files


class ECampusMail:
    """
    A controller class for handling email interactions with the university's eCampus mail server.

    This class manages connections for both reading emails (via IMAP) and sending emails 
    (via SMTP), specifically formatted for the University of Goettingen's infrastructure.
    """

    def __init__(self, login, password, server=SERVER):
        """
        Initialize the EcampusMail handler.

        Args:
            login (str): The student's username. The prefix 'ug-student\\' is 
                         automatically prepended to match the server's requirement.
            password (str): The user's email password.
            server (str, optional): The email server address. Defaults to the global SERVER constant.
        """

        self.login = str("ug-student\\"+login)
        self.password = password
        self.server = server

    def read_email_init(self):
        """
        Initializes the IMAP connection for reading emails.

        Connects to the server using SSL on port 993 and logs in with the 
        stored credentials.
        """

        self.mail = imaplib.IMAP4_SSL(self.server, 993)
        self.mail.login(self.login, self.password)

    @staticmethod
    def clean_header(header_value):
        """
        Decodes an email header (Subject, From, etc.) to a readable string.
        
        Handles various encodings and formats.
        
        Args:
            header_value (str or bytes): The raw header value from the email.
            
        Returns:
            str: The decoded and concatenated header string, or "None" if empty.
        """
        
        if not header_value:
            return "None"
    
        decoded_list = email.header.decode_header(header_value)
        header_text = ""
    
        for token, encoding in decoded_list:
            if isinstance(token, bytes):
            # If no encoding is specified, usually assume utf-8 or ascii
                try:
                    token = token.decode(encoding if encoding else 'utf-8')
                except (LookupError, UnicodeDecodeError):
                # Fallback if encoding is unknown or fails
                    token = token.decode('utf-8', errors='ignore')

            header_text += token
        
        return header_text

    def mail_notifications(self):
        """
        Checks the inbox for unread messages.

        Returns:
            int: The count of unseen (unread) emails in the inbox.
        """
        try:
            if not hasattr(self, 'mail') or self.mail is None or self.mail is False:
                return 0
            
            self.mail.select("inbox")
            result, data = self.mail.search(None, "UNSEEN")
            if data and data[0]:
                return len(data[0].split())
            return 0
        except (imaplib.IMAP4.abort, ConnectionResetError, OSError, AttributeError):
            return 0
        except Exception:
            return 0
    
    def show_subjects(self, last_n: int):
        """
        Fetches the subjects and timestamps for the N most recent emails.
        
        Args:
            last_n (int): The number of recent emails to retrieve.

        Returns:
            list: A list containing two sub-lists [subjects_list, dates_list].
                  subjects_list (list[str]): Decoded email subjects.
                  dates_list (list[datetime]): Timezone-aware datetime objects.
        """

        # Fetching searched mails
        self.mail.select("inbox")
        result, data = self.mail.search(None, "ALL")
        self.email_ids = data[0].split()
        latest_ids = self.email_ids[-last_n:]
        
        if not latest_ids:
            return [[], []]

        subjects_list = []
        dates_list = []

        # Rightly decode the mails
        id_string = b",".join(latest_ids).decode('utf-8')
        result, msg_data = self.mail.fetch(id_string, '(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE)])')

        # For each mail search subjects and dates
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                subject = self.clean_header(msg['Subject'])
                subjects_list.append(subject)
                
                raw_date = msg['Date']
                try:
                    date_obj = email.utils.parsedate_to_datetime(raw_date)
                    dates_list.append(date_obj)
                except Exception:
                    dates_list.append(None) 
        
        return [subjects_list, dates_list]
    
    def open_mail(self, mail_id):
        """
        Fetches and parses the full content of a specific email.

        Uses the 'RFC822' protocol to retrieve the raw email body and headers (also marks the email as seen).

        Args:
            mail_id (int or str): The index of the email in self.email_ids to fetch.
        
        Returns:
            email.message.Message: The parsed email object. You can access parts 
                                   using msg['Subject'] or msg.get_payload().
        """

        status, data = self.mail.fetch(self.email_ids[mail_id], "(RFC822)")
        raw_email_bytes = data[0][1]
        msg = email.message_from_bytes(raw_email_bytes)
        return msg

    def write_email_init(self):
        """
        Initializes the SMTP connection for sending emails.

        Connects to the server on port 587, secures the connection with TLS, 
        and logs in.
        """

        self.server = smtplib.SMTP(self.server, 587)
        self.server.ehlo() 
        self.server.starttls() 
        self.server.ehlo()
        self.server.login(self.login, self.password)

    def send_email(self, text, subject, sender, receiver, filename=None):
        """
        Composes and sends an email via the SMTP server, optionally with an attachment.

        This method constructs a MIME multipart message including the subject, sender, 
        receiver, and body text. If a filename is provided, the file is read in 
        binary mode, encoded in base64, and attached to the email.

        Args:
            text (str): The body content of the email.
            subject (str): The subject line of the email.
            sender (str): The email address of the sender.
            receiver (str): The email address of the recipient.
            filename (str, optional): The local file path of an attachment to include. 
                                      Defaults to None.

        Raises:
            Exception: If the underlying SMTP server fails to send the message.
        """

        message = email.mime.multipart.MIMEMultipart()
        message["Subject"] = str(subject)
        message["From"] = str(sender)
        message["To"] = str(receiver)
        message.attach(email.mime.text.MIMEText(str(text), "plain"))

        if filename is not None:
            with open(filename, "rb") as attachment:
                part = email.mime.multipart.MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            email.encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(filename)}")
            message.attach(part)

        try: 
            self.server.sendmail(str(sender),str(receiver), message.as_string())
        except Exception:
            raise Exception("Error in sending email")

    def close_conections(self):
        """Safely closes active connections."""

        if hasattr(self, 'mail') and self.mail and hasattr(self.mail, 'logout'):
            try:
                self.mail.logout()
            except Exception:
                pass
        if hasattr(self, 'server') and self.server and hasattr(self.server, 'quit'):
            try:
                self.server.quit()
                self.server.close()
            except Exception:
                pass


class LoginStorage:
    """
    A storage manager for user authentication and account status using SQLite.

    This class handles the creation of user databases, password hashing (SHA-256),
    credential verification, and the management of user ban statuses.
    """

    def __init__(self, name):
        """
        Initialize the database connection.

        Sets up the storage directory and connects to (or creates) the SQLite 
        database file specific to the provided name.

        Args:
            name (str): The identifier for the database file (e.g., 'users' or a specific group).
                        The file will be created at 'storage/{name}.db'.
        """
        self.base_path = "storage"
        os.makedirs(self.base_path, exist_ok=True)
        self.file_path = os.path.join(self.base_path, f"{name}.db")
        self.con = sql.connect(self.file_path)
        self.cur = self.con.cursor()
        self._create_table()

    def _create_table(self):
        """
        Initializes the 'users' table if it does not already exist.

        The table schema updated to include:
        - user_id (TEXT PRIMARY KEY): A unique 10-digit numeric identifier.
        - login (TEXT UNIQUE): The username used for authentication.
        - password (TEXT): The hashed password.
        - real_name (TEXT): The actual name of the user.
        - banned (INTEGER): A flag indicating if the user is banned (0 or 1).
        """
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY, 
                login TEXT UNIQUE, 
                password TEXT, 
                real_name TEXT, 
                banned INTEGER,
                is_admin INTEGER DEFAULT 0
            )
        """)
        self.con.commit()

    def generate_unique_id(self):
        """
        Generates a unique 10-digit numeric ID.

        This method ensures that the generated ID does not already exist
        in the database to maintain primary key integrity.
        """
        while True:
            new_id = str(random.randint(1000000000, 9999999999))

            # Check if this ID is already taken
            self.cur.execute("SELECT user_id FROM users WHERE user_id=?", (new_id,))
            if self.cur.fetchone() is None:
                return new_id

    def load(self):
        """
        Retrieves all user records from the database.

        Returns:
            sqlite3.Cursor: An iterable cursor containing tuples of (user_id, login, real_name, banned).
        """
        return self.cur.execute("SELECT user_id, login, real_name, banned, is_admin FROM users WHERE is_admin = 0")

    def user_exists(self, login):
        """
        Checks if a specific username exists in the database.

        Args:
            login (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        result = self.cur.execute("SELECT login FROM users WHERE login=?", (login,))
        return result.fetchone() is not None

    def create(self, login, password, real_name, is_admin=0):
        """
        Registers a new user with a hashed password, unique ID, and real name.

        Args:
            login (str): The new login username.
            password (str): The plain-text password.
            real_name (str): The user's real name from NameLine.

        Returns:
            bool: True if the user was successfully created.
                  False if the login already exists.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_id = self.generate_unique_id()  # Generating 10-digit unique ID

        try:
            self.cur.execute(
                "INSERT INTO users (user_id, login, password, real_name, banned, is_admin) VALUES (?, ?, ?, ?, 0, ?)",
                (user_id, login, hashed_password, real_name, is_admin)
            )
            self.con.commit()
            print(f"User {login} created with ID: {user_id}")
            return True
        except sql.IntegrityError:
            return False

    def compare(self, login, password):
        """
        Verifies login credentials.

        Hashes the provided password and compares it against the stored hash
        for the given username.

        Args:
            login (str): The username.
            password (str): The plain-text password to verify.

        Returns:
            bool: True if the credentials match, False otherwise.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        result = self.cur.execute("SELECT login FROM users WHERE login=? AND password=?", (login, hashed_password))
        return result.fetchone() is not None

    def set_ban_status(self, login, status: int):
        """
        Updates the ban status for a specific user.

        Args:
            login (str): The login username to update.
            status (int): The new status (e.g., 1 for banned, 0 for active).
        """
        self.cur.execute("UPDATE users SET banned=? WHERE login=?", (status, login))
        self.con.commit()


class NotesStorage:
    """
    A storage manager for user-specific notes using JSON files.

    This class handles loading, saving, and creating note objects, ensuring 
    data persistence across sessions for individual users.
    """

    def __init__(self, login: str):
        """
        Initialize the notes storage for a specific user.

        Args:
            login (str): The username of the current user. Used to generate 
                         a unique filename (e.g., 'username.json').
        """

        self.login = login
        self.base_path = "storage/data"
        os.makedirs(self.base_path, exist_ok=True)
        self.file_path = os.path.join(self.base_path, f"{login}.json")

    def load_notes(self) -> list[dict]:
        """
        Loads the list of notes from the user's JSON file.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents 
                        a note. Returns an empty list if the file does not exist.
        """

        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("notes", [])

    def save_notes(self, notes: list[dict]):
        """
        Saves a list of notes to the user's JSON file.

        Writes the data with UTF-8 encoding and indentation for readability.

        Args:
            notes (list[dict]): The list of note dictionaries to save.
        """

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)

    def create_note(self, title: str, content: str) -> dict:
        """
        Generates a new note dictionary with metadata.

        This method creates the note structure but does not save it to the file 
        automatically; `save_notes` must be called separately.

        Args:
            title (str): The title of the note.
            content (str): The body content of the note.

        Returns:
            dict: A dictionary containing the note's unique ID (UUID), title, 
                  content, and creation timestamp.
        """

        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }


class CourseDaysStorage:
    """
    A storage manager for persisting course schedule information.

    This class handles saving and loading the specific days associated with 
    a user's courses to a local JSON file.
    """

    def __init__(self, login):
        """
        Initialize the course days storage for a specific user.

        Args:
            login (str): The username of the current user. Used to generate 
                         a unique filename (e.g., 'course_days_username.json').
        """

        self.path = f"storage/course_days_{login}.json"

    def load(self):
        """
        Loads the course schedule data from the JSON file.

        Returns:
            dict: A dictionary containing the course-to-day mappings.
                  Returns an empty dictionary if the file does not exist.
        """

        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        """
        Saves the course schedule data to the JSON file.

        Args:
            data (dict): The dictionary containing course-to-day mappings 
                         to be stored.
        """

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
