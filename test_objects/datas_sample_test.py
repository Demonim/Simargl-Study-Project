import studipy

username = "p_dmytro_kutsak"
password = "53sq8dpw"
base_url = "https://studip.uni-goettingen.de/"

# create a new client object
client = studipy.Client(username=username, password=password, base_url=base_url)

# get a list of courses 
courses = client.Courses.get_courses() # Course(title='...', subtitle=..., description=..., location=..., course_id='...')
clist = []
for c in courses:
    clist.append(c.title)
print(clist)

# get names of other users
users = client.Users.get_users() # format: User(name="...", username="...", email="...", user_id = "...")
ulist = []
for u in users:
    ulist.append(u.name)
print(ulist)

# get user's messages
my_messages = client.Messages.get_messages() # format: Message(subject = "...", message_id="...", sender_id="...", body="<!--HTML-->..." creation_date="yyyy-mm-ddThh:mm:ss+[timezone]")
mlist = []
for m in my_messages:
    mlist.append(m.subject)
print(mlist)

# get user's calendar and schedule
calendar = client.Calendar.get_calendar() # calendar isn't as useful as schedule + potentionally very hard to process
schedule = client.Calendar.get_schedule() # format: Schedule_Entry(entry_id='...', description='...', title='...', start='hh:mm', end='hh:mm', frequency=..., related_course_id='...')
print(type(calendar),type(schedule))
print(str(calendar)[:351]+"...")
print(schedule)

#WIP: get files in user's domain
try:
    pass
    #client.Files.get_folders()
    #client.Files.get_files()
except:
    print("No Files/Folder are avaible")
# simply doesn't work atm :(