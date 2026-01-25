import studipy
import imaplib
import email
import smtplib
import os
import json
import uuid


BASE_URL = "https://studip.uni-goettingen.de/"
SERVER = "email.stud.uni-goettingen.de"


def create_client(usrnm,psswrd,bsrl):
    client = studipy.Client(usrnm, psswrd, bsrl)
    return client

def get_courses(clnt):
    courses = clnt.Courses.get_courses()
    return courses

def get_my_messages(clnt):
    my_messages = clnt.Messages.get_messages()
    return my_messages

def new_messages_counter(clnt):
    new_messages = clnt.Messages.get_messages(True)
    return len(new_messages)

def get_schedule(clnt):
    schedule = clnt.Calendar.get_schedule()
    return schedule

def get_folders(clnt,crss):
    folders = []
    for f in range(len(crss)):
        folders.append(clnt.Files.get_folders(courses[f]))
    return folders

def get_files(clnt,crss):
    files = []
    for ff in range(len(crss)):
        files.append(clnt.Files.get_folders(courses[ff]))
    return files

def read_email_init(imap_srvr,usrnm,psswrd):
    mail = imaplib.IMAP4_SSL(imap_srvr, 993)
    mail.login(usrnm, psswrd)
    return mail

def mail_notifications(mail):
    mail.select("inbox")
    result, data = mail.search(None, "UNSEEN")
    return len(data[0].split())

def write_email_init(smtp_srvr,usrnm,psswrd):
    server = smtplib.SMTP(smtp_srvr, 587)
    server.ehlo() 
    server.starttls() 
    server.ehlo()
    server.login(usrnm,psswrd)
    return server

def closing_conections(server, mail):
    server.quit(); mail.close(); mail.logout()

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
