import studipy

#username = str(input("Enter your username(firstname.lastname)"))
#password = str(input("Enter your password"))
base_url = "https://studip.uni-goettingen.de/"

def create_client(usrnm,psswrd,bsrl):
    client = studipy.Client(usrnm, psswrd, bsrl)
    return client

def get_courses(clnt):
    courses = clnt.Courses.get_courses()
    return courses

def get_my_messages(clnt):
    my_messages = clnt.Messages.get_messages()
    return my_messages

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
