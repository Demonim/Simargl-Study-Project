import studipy
import imaplib
import email
import smtplib
import os
import json
import uuid
import sqlite3 as sql

BASE_URL = "https://studip.uni-goettingen.de/"
SERVER = "email.stud.uni-goettingen.de"

class StudIP:
    def __init__(self, login, password, base_url=BASE_URL):
        self.login = login
        self.password = password
        self.base_url = base_url

    def create_client(self):
        self.client = studipy.Client(self.login, self.password, self.base_url)

    def get_courses(self):
        courses = self.client.Courses.get_courses()
        return courses

    def get_my_messages(self):
        my_messages = self.client.Messages.get_messages()
        return my_messages

    def new_messages_counter(self):
        new_messages = self.client.Messages.get_messages(True)
        return len(new_messages)

    def get_schedule(self):
        schedule = self.client.Calendar.get_schedule()
        return schedule

    def get_folders(self, clnt, crss):
        folders = []
        for f in range(len(crss)):
            folders.append(clnt.Files.get_folders(courses[f]))
        return folders

    def get_files(self, clnt, crss):
        files = []
        for ff in range(len(crss)):
            files.append(clnt.Files.get_folders(courses[ff]))
        return files

class EcampusMail:
    def __init__(self, login, password, server=SERVER):
        self.login = str("ug-student\\"+login)
        self.password = password
        self.server = server

    def read_email_init(self):
        self.mail = imaplib.IMAP4_SSL(self.server, 993)
        self.mail.login(self.login, self.password)

    def mail_notifications(self):
        self.mail.select("inbox")
        result, data = self.mail.search(None, "UNSEEN")
        return len(data[0].split())

    def write_email_init(self):
        self.server = smtplib.SMTP(self.server, 587)
        self.server.ehlo() 
        self.server.starttls() 
        self.server.ehlo()
        self.server.login(self.login, self.password)

    def close_conections(self):
        self.server.quit(); self.mail.close(); self.mail.logout()

class LoginStorage:
    pass

class NotesStorage:
    def __init__(self, login: str):
        self.login = login
        self.base_path = "storage/data"
        os.makedirs(self.base_path, exist_ok=True)
        self.file_path = os.path.join(self.base_path, f"{login}.json")

    def load_notes(self) -> list[dict]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("notes", [])

    def save_notes(self, notes: list[dict]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)

    def create_note(self, title: str, content: str) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }

class CourseDaysStorage:
    def __init__(self, login):
        self.path = f"storage/course_days_{login}.json"

    def load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
