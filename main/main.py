import sys
import os
import simargl

from PySide6.QtWidgets import (
    QListWidgetItem,
    QGridLayout,
    QWidget,
    QTextBrowser,
    QComboBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QDialog,
    QListWidget,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QHBoxLayout,
    QCheckBox
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize
from PySide6.QtWidgets import QApplication, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from themes import *

import datetime
import calendar
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


weekly_schedule = defaultdict(list)
schedule = None
notes_storage = None
admin_login = "Admin"
admin_password = "Admin"


# =========================
# THEMES
# =========================

WEEKDAY_MAP = {
    0: "MO",
    1: "TU",
    2: "WE",
    3: "TH",
    4: "FR",
    5: "SA",
    6: "SU"
}

# =========================
# UI LOADER
# =========================

def load_ui(path: str):
    loader = QUiLoader()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(base_dir, path)

    ui_file = QFile(ui_path)
    if not ui_file.open(QFile.ReadOnly):
        print(f"CRITICAL ERROR: Could not find or open UI file at: {ui_path}")
        print(f"Qt Error: {ui_file.errorString()}")
        sys.exit(-1)
    
    window = loader.load(ui_file)
    ui_file.close()
    return window


class DayScheduleDialog(QDialog):
    def __init__(self, title, entries, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(450, 300)

        layout = QVBoxLayout(self)
        self.list = QListWidget()
        layout.addWidget(self.list)

        if not entries:
            self.list.addItem("No classes at this day")
            return

        for e in sorted(entries, key=lambda x: x.start):
            self.list.addItem(
                f"{e.start} – {e.end} | {e.title}"
            )

class AddNoteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add new Note")
        self.setFixedSize(300, 120)
        self.setModal(True)

        layout = QVBoxLayout(self)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Notes name")

        self.ok_button = QPushButton("Create ")
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(QLabel("Insert a name of the note:"))
        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)

    def get_name(self):
        return self.line_edit.text().strip()

class CourseDayDialog(QDialog):
    def __init__(self, courses, storage, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set course days")
        self.setMinimumSize(600, 400)

        self.storage = storage
        self.saved_days = storage.load()

        self.layout = QVBoxLayout(self)
        self.list = QListWidget()
        self.list.setSpacing(15)
        self.layout.addWidget(self.list)

        self.inputs = {}

        for course in courses:
            widget = QWidget()
            widget.setMinimumHeight(40)
            widget.setObjectName("CourseItem")
            row = QHBoxLayout(widget)

            label = QLabel(course.title)
            label.setMinimumWidth(350)
            label.setMinimumHeight(30)
            label.setStyleSheet("font-size: 12px;")

            input_day = QLineEdit()
            input_day.setPlaceholderText("MO / TU / WE ...")
            input_day.setMinimumWidth(80)
            input_day.setStyleSheet("margin-left: auto;")

            if course.title in self.saved_days:
                input_day.setText(self.saved_days[course.title])

            row.addWidget(label)
            row.addWidget(input_day)

            self.list.addItem("")
            self.list.setItemWidget(self.list.item(self.list.count() - 1), widget)

            self.inputs[course.course_id] = input_day

        save_btn = QPushButton("Save & Continue")
        save_btn.clicked.connect(self.save_and_close)
        self.layout.addWidget(save_btn)

    def save_and_close(self):
        result = {}
        for course_id, input_day in self.inputs.items():
            day = input_day.text().strip().upper()
            if day:
                result[course_id] = day

        self.storage.save(result)
        self.accept()


# =========================
# THEME HANDLING
# =========================

def change_theme(app: QApplication, theme: str):
    if theme == "Dark Theme":
        app.setStyleSheet(DARK_THEME)
    elif theme == "Dark Mini":
        app.setStyleSheet(DARK_Minimalistic)
    elif theme == "Light Theme":
        app.setStyleSheet(LIGHT_THEME)
    elif theme == "Light Mini":
        app.setStyleSheet(LIGHT_Minimalistic)


# =========================
# WINDOW SWITCH
# =========================

def open_admin(main_window):
    admin_window = load_ui("UI/Admin.ui")

    ban_button = admin_window.findChild(QPushButton, "Ban_Button")
    unban_button = admin_window.findChild(QPushButton, "Unban_Button")
    back_button = admin_window.findChild(QPushButton, "Back_Button")
    back_button.clicked.connect(
        lambda: back_to_main(admin_window)
    )

    admin_window.show()
    main_window.close()

    main_window.courses_window = admin_window


def open_courses(menu_window):
    global user_courses

    courses_window = load_ui("UI/courses.ui")
    exit_button = courses_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(courses_window)
    )
    table = courses_window.findChild(QTableWidget, "Table")

    if table is not None:
        table.setRowCount(0)
        table.setRowCount(len(user_courses))

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.verticalHeader().setVisible(False)

        for row, course in enumerate(user_courses):
            table.setItem(
                row, 0,
                QTableWidgetItem(course.title or "—")
            )
            table.setItem(
                row, 1,
                QTableWidgetItem(course.subtitle or "—")
            )
            table.setItem(
                row, 2,
                QTableWidgetItem("Active")
            )

    courses_window.show()
    menu_window.close()

    menu_window.courses_window = courses_window

def open_calendar_entry(menu_window):
    storage = simargl.CourseDaysStorage(current_login)

    dialog = CourseDayDialog(
        courses=user_courses,
        storage=storage,
        parent=menu_window
    )

    if dialog.exec():
        open_calendar(menu_window)

def open_calendar(menu_window):
    calendar_window = load_ui("UI/calendar.ui")

    # ===== BUTTON BACK =====
    exit_button = calendar_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(calendar_window)
    )

    # ===== LOADING SAVED DAYS =====
    storage = simargl.CourseDaysStorage(current_login)
    course_days = storage.load()  # { course_title: "MO" }

    # ===== FORMING WEEKLY_SCHEDULE =====
    weekly_schedule.clear()

    for entry in schedule.entries:
        day = course_days.get(entry.related_course_id)
        if day:
            weekly_schedule[day].append(entry)

    # ===== CALENDAR GRID =====
    calendar_widget = calendar_window.findChild(QWidget, "Calendar")
    grid = calendar_widget.findChild(QGridLayout, "gridLayout_2")

    # ===== BUILD BUTTONS =====
    buttons = []
    for i in range(grid.count()):
        widget = grid.itemAt(i).widget()
        if isinstance(widget, QPushButton):
            buttons.append(widget)

    # ===== SORTING BY POSITION =====
    buttons_with_pos = []
    for btn in buttons:
        index = grid.indexOf(btn)
        row, col, _, _ = grid.getItemPosition(index)
        buttons_with_pos.append((row, col, btn))

    buttons_with_pos.sort(key=lambda x: (x[0], x[1]))
    buttons_sorted = [b[2] for b in buttons_with_pos]

    # ===== CURRENT MONTH =====
    today = datetime.date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_days = list(cal.itermonthdays(year, month))

    # ===== CLICK ON DAY =====
    def on_day_clicked(day):
        clicked_date = datetime.date(year, month, day)
        weekday_code = WEEKDAY_MAP[clicked_date.weekday()]

        entries = weekly_schedule.get(weekday_code, [])

        dialog = DayScheduleDialog(
            title=clicked_date.strftime("%A %d.%m.%Y"),
            entries=entries,
            parent=calendar_window
        )
        dialog.exec()

    # ===== FILLING BUTTONS =====
    for btn, day in zip(buttons_sorted, month_days):
        try:
            btn.clicked.disconnect()
        except Exception:
            pass

        if day == 0:
            btn.setText("")
            btn.setEnabled(False)
        else:
            btn.setText(str(day))
            btn.setEnabled(True)
            btn.clicked.connect(
                lambda checked=False, d=day: on_day_clicked(d)
            )

    calendar_window.show()
    menu_window.close()
    menu_window.courses_window = calendar_window

def open_StudIP(menu_window):
    StudIP_window = load_ui("UI/StudIP.ui")

    # exit button
    exit_button = StudIP_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(StudIP_window)
    )

    # ---------- MESSAGES ----------
    messages_list = StudIP_window.findChild(QListWidget, "messagesList")

    # settback in the case of not finding the widget
    if messages_list is not None:
        messages_list.clear()
        messages_list.setSpacing(8)

        try:
            messages = studip.get_my_messages()
        except Exception as e:
            print("Failed to load messages:", e)
            messages = []

        for msg in messages:
            title = msg.subject if msg.subject else "Без темы"

            btn = QPushButton(title)
            btn.setMinimumHeight(48)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 12px;
                    font-size: 14px;
                }
            """)
            btn.clicked.connect(
                lambda checked=False, m=msg: open_message_dialog(m)
            )

            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 54))

            messages_list.addItem(item)
            messages_list.setItemWidget(item, btn)

    # --------------------------------

    StudIP_window.show()
    menu_window.close()

    menu_window.courses_window = StudIP_window


def open_message_dialog(message):
    dialog = load_ui("UI/MessageDialog.ui")

    full_msg = studip.client.Messages.view_message(message)

    sender_label = dialog.findChild(QLabel, "senderLabel")
    date_label = dialog.findChild(QLabel, "dateLabel")
    subject_label = dialog.findChild(QLabel, "subjectLabel")
    body_text = dialog.findChild(QTextEdit, "bodyText")
    close_button = dialog.findChild(QPushButton, "closeButton")

    sender_label.setText(f"From: {full_msg.sender_id}")
    date_label.setText(f"Date: {full_msg.creation_date}")
    subject_label.setText(full_msg.subject or "Без темы")
    body_text.setHtml(full_msg.body)

    close_button.clicked.connect(dialog.close)

    dialog.exec()

def open_Email(menu_window):
    Email_window = load_ui("UI/Email.ui")

    exit_button = Email_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(Email_window)
    )

    Email_window.show()
    menu_window.close()

    menu_window.courses_window = Email_window


def open_Dashboard(menu_window):
    Dashboard_window = load_ui("UI/dashboard_test.ui")

    target_widget = Dashboard_window.findChild(QWidget, "Dashboard_1")

    if target_widget:
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='none')
        canvas = FigureCanvasQTAgg(fig)
        canvas.setStyleSheet("background-color: transparent;")
        ax = fig.add_subplot(111)

        labels = ["Python", "C++", "JS", "Other"]
        values = [40, 30, 20, 10]
        ax.pie(values, labels=labels, autopct='%1.1f%%', textprops={'color': "w"})
        ax.set_title("Языки программирования", color="w")

        if target_widget.layout() is None:
            layout = QVBoxLayout(target_widget)
            target_widget.setLayout(layout)
        else:
            layout = target_widget.layout()

        layout.addWidget(canvas)

    exit_button = Dashboard_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(Dashboard_window)
    )

    Dashboard_window.show()
    menu_window.close()

    menu_window.courses_window = Dashboard_window

def open_Notes(menu_window):
    global notes_storage
    Notes_window = load_ui("UI/notes.ui")

    exit_button = Notes_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(Notes_window)
    )

    notes_list = Notes_window.findChild(QListWidget, "NotesList")
    text_edit = Notes_window.findChild(QTextEdit, "NotesText")
    add_button = Notes_window.findChild(QPushButton, "AddNoteButton")
    save_button = Notes_window.findChild(QPushButton, "SaveNoteButton")

    # Notes safe (saves while the window is open)
    notes = notes_storage.load_notes()

    for note in notes:
        notes_list.addItem(note["title"])

    # --- add note ---
    def add_note():
        dialog = AddNoteDialog(Notes_window)
        if dialog.exec():
            title = dialog.get_name()
            if not title:
                return
            new_note = notes_storage.create_note(title, "")
            notes.append(new_note)
            notes_storage.save_notes(notes)

            notes_list.addItem(title)

    # --- load note ---
    def load_note(item):
        title = item.text()
        for note in notes:
            if note["title"] == title:
                text_edit.setPlainText(note["content"])
                break

    # --- save note ---
    def save_note():
        item = notes_list.currentItem()
        if not item:
            return

        title = item.text()
        for note in notes:
            if note["title"] == title:
                note["content"] = text_edit.toPlainText()
                notes_storage.save_notes(notes)
                break

    add_button.clicked.connect(add_note)
    notes_list.itemClicked.connect(load_note)
    save_button.clicked.connect(save_note)

    Notes_window.show()
    menu_window.close()
    menu_window.courses_window = Notes_window


def open_Themes(menu_window):
    theme_dialog = load_ui("UI/Theme.ui")

    btn_dark = theme_dialog.findChild(QPushButton, "Dark")
    btn_dark_mini = theme_dialog.findChild(QPushButton, "Dark_mini")
    btn_light = theme_dialog.findChild(QPushButton, "Light")
    btn_light_mini = theme_dialog.findChild(QPushButton, "Light_mini")

    def apply_and_close(theme_name):
        change_theme(QApplication.instance(), theme_name)
        theme_dialog.accept()

    if btn_dark:
        btn_dark.clicked.connect(lambda: apply_and_close("Dark Theme"))
    if btn_dark_mini:
        btn_dark_mini.clicked.connect(lambda: apply_and_close("Dark Mini"))
    if btn_light:
        btn_light.clicked.connect(lambda: apply_and_close("Light Theme"))
    if btn_light_mini:
        btn_light_mini.clicked.connect(lambda: apply_and_close("Light Mini"))

    theme_dialog.exec()
    open_menu(menu_window)


def open_Help1(main_window):
    Help_window1 = load_ui("UI/help_1.ui")

    textBrowser = Help_window1.findChild(QTextBrowser, "textBrowser")

    exit_button = Help_window1.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(Help_window1)
    )
    FAQ_button = Help_window1.findChild(QPushButton, "FAQ")
    FAQ_button.clicked.connect(
        lambda: textBrowser.setText("""What is this app for? \n- This app is designed to help students during their university studies.
        \nIs my personal data saved?\n- Yes, but user data is encrypted and stored in a local database.
        \nHow can I change my password?\n- After logging into my account, go to the Account Settings tab.""")
    )
    Instructions_button = Help_window1.findChild(QPushButton, "Instruction")
    Instructions_button.clicked.connect(
        lambda: textBrowser.setText("""1. Enter your login details for Stud.Ip. 
        \n2. After logging in, you will have access to a menu with all the application functions. 
        \n Among them you can use: \n- Active user courses  \n- Current month calendar \n- List of incoming Stud.ip messages \n- Ecampusmail incoming message list \n- Ability to create and edit notes \n- Customize your settings""")
    )
    Support_button = Help_window1.findChild(QPushButton, "Support")
    Support_button.clicked.connect(
        lambda: textBrowser.setText("""Contact the app owner and lead developer: \n-Dmytro Kutsak. 
        \nIf you find bugs in UI, please contact: \n-Nichita Licov  \n-Diana Bardyk""")
    )
    App_button = Help_window1.findChild(QPushButton, "App")
    App_button.clicked.connect(
        lambda: textBrowser.setText("The Idea: Dmytro Kutsak.\nDesigned by: Nichita Licov and Diana Bardyk ")
    )

    Help_window1.show()
    main_window.close()

    main_window.courses_window = Help_window1

def open_Help(main_window):
    Help_window = load_ui("UI/help.ui")

    textBrowser = Help_window.findChild(QTextBrowser, "textBrowser")

    exit_button = Help_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(Help_window)
    )
    FAQ_button = Help_window.findChild(QPushButton, "FAQ")
    FAQ_button.clicked.connect(
        lambda: textBrowser.setText("""What is this app for? \n- This app is designed to help students during their university studies.
        \nIs my personal data saved?\n- Yes, but user data is encrypted and stored in a local database.
        \nHow can I change my password?\n- After logging into my account, go to the Account Settings tab.""")
    )
    Instructions_button = Help_window.findChild(QPushButton, "Instruction")
    Instructions_button.clicked.connect(
        lambda: textBrowser.setText("""1. Enter your login details for Stud.Ip. 
        \n2. After logging in, you will have access to a menu with all the application functions. 
        \nAmong them you can use: \n- Active user courses  \n- Current month calendar \n- List of incoming Stud.ip messages \n- Ecampusmail incoming message list \n- Ability to create and edit notes \n- Customize your settings""")
    )
    Support_button = Help_window.findChild(QPushButton, "Support")
    Support_button.clicked.connect(
        lambda: textBrowser.setText("""Contact the app owner and lead developer: \n-Dmytro Kutsak. 
        \nIf you find bugs in UI, please contact: \n-Nichita Licov  \n-Diana Bardyk""")
    )
    App_button = Help_window.findChild(QPushButton, "App")
    App_button.clicked.connect(
        lambda: textBrowser.setText("The Idea: Dmytro Kutsak.\nDesigned by: Nichita Licov and Diana Bardyk ")
    )

    Help_window.show()
    main_window.close()

    main_window.courses_window = Help_window

def open_menu(main_window):
    menu_window = load_ui("UI/menu.ui")
    mail_notifications = menu_window.findChild(QLabel,"Ecampus_Mail")
    message_notifications = menu_window.findChild(QLabel,"StudIP_Messages")
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(mail_notifications.setText(f"ECampus Mail ({ecampusmail.mail_notifications()})"), 1)
        executor.submit(message_notifications.setText(f"StudIP ({studip.new_messages_counter()})"), 2)

    name_label = menu_window.findChild(QLabel,"Name_label")
    name_label.setText(f"{current_login}")

    courses_button = menu_window.findChild(QPushButton, "Courses")
    courses_button.clicked.connect(
        lambda: open_courses(menu_window)
    )
    calendar_button = menu_window.findChild(QPushButton, "Calendar")
    calendar_button.clicked.connect(
        lambda: open_calendar_entry(menu_window)
    )
    StudIP_button = menu_window.findChild(QPushButton, "Messages")
    StudIP_button.clicked.connect(
        lambda: open_StudIP(menu_window)
    )
    Email_button = menu_window.findChild(QPushButton, "Email")
    Email_button.clicked.connect(
        lambda: open_Email(menu_window)
    )
    Dashboard_button = menu_window.findChild(QPushButton, "Dashboard")
    Dashboard_button.clicked.connect(
        lambda: open_Dashboard(menu_window)
    )
    Notes_button = menu_window.findChild(QPushButton, "Notes")
    Notes_button.clicked.connect(
        lambda: open_Notes(menu_window)
    )
    Theme_button = menu_window.findChild(QPushButton, "Theme")
    Theme_button.clicked.connect(
        lambda: open_Themes(menu_window)
    )
    help_button = menu_window.findChild(QPushButton, "Help1")
    help_button.clicked.connect(
        lambda: open_Help1(menu_window)
    )
    exit_button = menu_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(menu_window)
    )


    menu_window.show()
    main_window.close()

    main_window.menu_window = menu_window




def back_to_main(menu_window):
    main_window = load_ui("UI/main.ui")

    try:
        if ecampusmail.server and ecampusmail.mail:
            ecampusmail.close_conections()
            ecampusmail.server = False; ecampusmail.mail = False
    except:
        pass

    # Theme combobox
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(QApplication.instance(), text)
    )

    # Check box "Remember me"
    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/login_data.db"
    if os.path.exists(remember_path):
        login_database = simargl.LoginStorage()
        db_data = login_database.load().fetchall()
        login_box = main_window.findChild(QLineEdit, "LoginLine")
        login_box.setText(db_data[0][0])
        remember_check.click()

    remember_check.clicked.connect(
        lambda: check_box_remember(remember_check)
    )

    # Theme init
    change_theme(QApplication.instance(), theme_box.currentText())

    # Press Enter to enter the menu
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window, remember)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )

    main_window.show()
    menu_window.close()


def error_login(menu_window):
    error_window = load_ui("UI/error.ui")

    # button to exit back to the main
    exit_button = error_window.findChild(QPushButton, "Error_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(error_window)
    )

    error_window.show()
    menu_window.close()

    menu_window.courses_window = error_window


def login_from_enter(main_window,remember=False):
    global user_courses, current_login, schedule, ecampusmail, studip, messages
    login_box = main_window.findChild(QLineEdit, "LoginLine")
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    current_login = login_box.text(); password = password_box.text()

    if current_login == admin_login and password == admin_password:
        open_admin(main_window)
        return

    studip = simargl.StudIP(current_login, password)
    ecampusmail = simargl.ECampusMail(current_login, password)

    try:
        studip.create_client()
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(ecampusmail.read_email_init())
            executor.submit(ecampusmail.write_email_init())
    except:
        error_login(main_window)
    else:
        if remember:
            login_database = simargl.LoginStorage()
            result = login_database.load()
            if result is None:
                login_database.create(current_login, password)
            else:
                login_database.compare(current_login, password)
        if not remember:
            if os.path.exists(remember_path):
                os.remove(remember_path)

        global notes_storage
        notes_storage = simargl.NotesStorage(current_login)

        open_menu(main_window)

        user_courses = studip.get_courses()
        schedule = studip.get_schedule()
        messages = studip.get_my_messages()


# =========================
# MAIN
# =========================

def check_box_remember(checkbox:QCheckBox):
    global remember
    if checkbox.isChecked() == True:
        remember = True
    if checkbox.isChecked() == False:
        remember = False


def main():
    global remember, remember_path
    remember = False

    app = QApplication(sys.argv)

    # --- load main window ---
    main_window = load_ui("UI/main.ui")

    # --- theme combobox ---
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(app, text)
    )

    # --- check box "Remember me" ---
    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/login_data.db"
    if os.path.exists(remember_path):
        login_database = simargl.LoginStorage()
        db_data = login_database.load().fetchall()
        login_box = main_window.findChild(QLineEdit, "LoginLine")
        login_box.setText(db_data[0][0])
        remember_check.click()

    remember_check.clicked.connect(
        lambda: check_box_remember(remember_check)
    )

    # --- setting theme on the start ---
    change_theme(app, theme_box.currentText())

    # --- enter button ---
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window,remember)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )



    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()