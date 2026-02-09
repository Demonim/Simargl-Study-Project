import matplotlib.pyplot as plt
from main.dashboard.pie.create_pie import create_pie
from main.simargl import ECampusMail
from main.simargl import StudIP
from main.dashboard.heatmap.messages_logic import topics_week_matrix
from main.dashboard.heatmap.create_heatmap import create_heatmap
from main.dashboard.pie.subject_hours import subject_hours

login = input('Enter your login: ')
password = input('Enter your password: ')

# PIE з matplotlib в верхньому лівому кутку
studip_handler = StudIP(login, password)
studip_handler.create_client()
user_schedule = studip_handler.get_schedule()
subject_hours = subject_hours(user_schedule)

# HEATMAP з matplotlib в верхньому правому кутку
mail_handler = ECampusMail(login, password)
mail_handler.read_email_init()
subjects, dates = mail_handler.show_subjects(last_n=200)

# об'єкти графіків
my_pie = create_pie(subject_hours)
my_heatmap = create_heatmap(subjects, dates)

# щоб matplotlib відкрило два окремих вікна 
import matplotlib.backend_bases

def show_figure(fig):
    # нове вікно через pyplot і переноситься туди вміст об'єктів
    new_manager = plt.figure().canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)


show_figure(my_pie)
show_figure(my_heatmap)

plt.show() 
mail_handler.close_conections() 