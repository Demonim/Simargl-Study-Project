import studipy
import imaplib
import email
import smtplib
#import getpass

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
    new_messages = clnt.Messages.get_messages(True)
    return my_messages, new_messages

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

...

