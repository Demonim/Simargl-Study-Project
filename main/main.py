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
    QCheckBox,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize, Qt, QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout
from themes import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from dashboard.timer_bar.study_timer import Study_Timer
from dashboard.dashboard_logic import (
    get_pie_chart, get_heatmap, initialize_tracker,
    clear_all_data, stop_study_session, start_study_session,
    get_weekly_bar_chart, refresh_stacked_bar
)

import calendar
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from datetime import datetime

current_active_window = None
prelogin_window = None
weekly_schedule = defaultdict(list)
study_timer = Study_Timer()
active_timer_day = None
schedule = None
notes_storage = None
current_theme_name = "Dark"

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

HELP_TEXTS = {
    "calendar": "<h2>Calendar Help</h2><p>Here you can view your class schedule. Click on a specific day to see the detailed list of lectures.</p>",
    "courses": "<h2>Courses Help</h2><p>This section lists all your active courses from Stud.IP. You can see the title, subtitle, and status.</p>",
    "dashboard": "<h2>Dashboard Help</h2><p>Visualize your study progress! <ul><li><b>Pie chart:</b> Distribution of hours.</li><li><b>Heatmap:</b> Activity frequency.</li><li><b>Bar chart:</b> Weekly tracker.</li></ul></p>",
    "email": "<h2>Email Help</h2><p>Access your ECampus mail. You can read incoming messages and send new emails using the 'Write' button.</p>",
    "notes": "<h2>Notes Help</h2><p>Manage your personal notes. Create new ones, edit existing text, and don't forget to press 'Save'!</p>",
    "studip": "<h2>StudIP Help</h2><p>This shows your recent messages from the Stud.IP system. Click on a message to read its full content.</p>"
}


# =========================
# Helper Functions
# =========================

def load_ui(path: str):
    """A utility function that uses QUiLoader to dynamically load .ui files.
    It ensures the UI file exists and returns the loaded window object for use in the application.
    """
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

def setup_auto_logout(window):
    """
    Initializes a QTimer that monitors user inactivity.
    If the timer reaches 5 minutes without being reset,
    it triggers the universal_logout function for security.
    """
    window.auto_logout_timer = QTimer(window)
    window.auto_logout_timer.setSingleShot(True)

    window.auto_logout_timer.timeout.connect(universal_logout)

    window.auto_logout_timer.start(300000)

def save_tracker_data(dashboard_window, canvas_bar, theme):
    """
    Scrapes study hour inputs from the UI and updates the weekly study bar chart.
    """
    try:
        if dashboard_window is None or canvas_bar is None:
            return

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_inputs = []

        for day in days:
            try:
                h_line = dashboard_window.findChild(QLineEdit, f"{day}_H")
                m_line = dashboard_window.findChild(QLineEdit, f"{day}_M")

                if h_line and m_line:
                    h_text = h_line.text()
                    m_text = m_line.text()
                    day_inputs.append((day, h_text.strip() if h_text else "", m_text.strip() if m_text else ""))
            except Exception:
                continue

        refresh_stacked_bar(canvas_bar, manual_inputs=day_inputs)
        apply_bar_theme(canvas_bar, theme)
        if hasattr(canvas_bar, 'draw'):
            canvas_bar.draw()
    except Exception:
        pass  


def stop_timer_and_save(canvas_bar, current_theme):
    """
    Stops the active study session,
    calculates the elapsed time, saves the data to the tracker
    for the current day, and triggers a refresh of the visual bar chart.
    """
    global active_timer_day
    try:
        if not (study_timer.running and active_timer_day):
            return

        # Calculate session hours before reset
        try:
            # Get the time of current session before stopping
            if study_timer.start_time:
                delta = datetime.now() - study_timer.start_time
                session_hours = delta.total_seconds() / 3600.0
            else:
                session_hours = 0.0
        except Exception:
            session_hours = 0.0
        
        study_timer.stop()
        stop_study_session(active_timer_day, session_hours)
        study_timer.reset()

        if canvas_bar is not None:
            refresh_stacked_bar(canvas_bar)
            apply_bar_theme(canvas_bar, current_theme)
            if hasattr(canvas_bar, 'draw'):
                canvas_bar.draw()
        active_timer_day = None
    except Exception:
        active_timer_day = None

def apply_bar_theme(canvas_bar, theme):
    """
    Dynamically updates the Matplotlib graph styling
    (axes, ticks, and labels) to ensure visibility by switching
    between light and dark colors based on the current UI theme.
    """
    try:
        if canvas_bar is None or not hasattr(canvas_bar, 'figure') or canvas_bar.figure is None:
            return

        txt_col = 'white' if (theme and "Dark" in str(theme)) else 'black'
        fig = canvas_bar.figure
        ax = fig.gca()

        ax.tick_params(colors=txt_col)
        ax.xaxis.label.set_color(txt_col)
        ax.yaxis.label.set_color(txt_col)

        for spine in ax.spines.values():
            spine.set_edgecolor(txt_col)

        if hasattr(canvas_bar, 'draw'):
            canvas_bar.draw()
    except Exception:
        pass 


def load_ecampus_mail_data(Email_window):
    """
    Connects to the university mail server to fetch the latest 100 email headers.
    It clears the existing list in the UI and populates it with clickable subject/date items.
    """
    global ecampusmail

    messages_list = Email_window.findChild(QListWidget, "messagesList")
    if not messages_list:
        return

    messages_list.clear()

    try:
        subjects, dates = ecampusmail.show_subjects(100)

        total_emails = len(ecampusmail.email_ids)
        start_offset = total_emails - len(subjects)

        for i in range(len(subjects)-1, -1, -1):
            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(5, 2, 5, 2)

            display_text = f"{dates[i]} | {subjects[i]}"
            msg_button = QPushButton(display_text)
            msg_button.setStyleSheet("text-align: left; padding: 10px;")

            # Link the opening of a letter to index i
            global_idx = start_offset + i
            msg_button.clicked.connect(lambda ch=False, idx=global_idx: open_mail_content(idx))

            layout.addWidget(msg_button)

            # Add a widget to QListWidget
            list_item = QListWidgetItem(messages_list)
            list_item.setSizeHint(item_widget.sizeHint())
            messages_list.addItem(list_item)
            messages_list.setItemWidget(list_item, item_widget)

    except Exception as e:
        print(f"Error when getting the mail: {e}")


def open_mail_content(mail_index):
    """
    Extracts and decodes the body of a specific email.
    It handles multipart MIME messages to find plain
    text content and displays it in a dedicated pop-up dialog.
    """
    global ecampusmail

    try:
        msg = ecampusmail.open_mail(mail_index)
        content = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        dialog = QDialog()
        dialog.setWindowTitle(f"Mail: {msg['Subject']}")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(content)

        layout.addWidget(text_edit)
        dialog.exec()

    except Exception as e:
        print(f"Error: {e}")


# =========================
# Helper Classes
# =========================

class DayScheduleDialog(QDialog):
    """
    A dialog window displaying the user's class schedule for a specific day.

    This dialog takes a list of calendar entries for a selected date, sorts them 
    by their start times, and displays them in a simple list format.
    """

    def __init__(self, title, entries, parent=None):
        """
        Initializes the daily schedule dialog.

        Args:
            title (str): The title of the dialog, typically formatted as the date (e.g., "Monday 15.05.2023").
            entries (list): A list of schedule entry objects containing 'start', 'end', and 'title' attributes.
            parent (QWidget, optional): The parent widget for this dialog. Defaults to None.
        """

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
    """
    A modal dialog that prompts the user to enter a title for a new note.

    It provides a simple text input field and a confirmation button to create 
    the basic structure of a note before opening it in the editor.
    """

    def __init__(self, parent=None):
        """
        Initializes the note creation dialog and sets up the UI layout.

        Args:
            parent (QWidget, optional): The parent widget for this dialog. Defaults to None.
        """

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
        """
        Retrieves the trimmed text entered by the user in the input field.

        Returns:
            str: The sanitized string representing the new note's title.
        """

        return self.line_edit.text().strip()


class CourseDayDialog(QDialog):
    """
    A dialog window allowing the user to map their enrolled courses to specific days of the week.

    This acts as an initial configuration step for the calendar view, loading any 
    previously saved mappings and allowing the user to input abbreviations 
    (e.g., MO, TU, WE) for when each course takes place.
    """

    def __init__(self, courses, storage, parent=None):
        """
        Initializes the course day assignment dialog.

        Args:
            courses (list): A list of course objects fetched from Stud.IP.
            storage (CourseDaysStorage): The storage manager handling the persistence of course day data.
            parent (QWidget, optional): The parent widget for this dialog. Defaults to None.
        """

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
        """
        Extracts the entered day abbreviations for each course, saves them 
        to the local JSON storage via the storage manager, and closes the dialog.
        """

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

def change_theme(app, theme):
    """
    Manages the application's visual style. It maps a theme name (e.g., "Dark Theme")
    to a specific QSS (Qt Style Sheet) and applies it to the entire QApplication instance.
    """
    global current_theme_name
    current_theme_name = theme

    if theme == "Dark Theme":
        app.setStyleSheet(DARK_THEME)
    elif theme == "Dark Mini":
        app.setStyleSheet(DARK_Minimalistic)
    elif theme == "Light Theme":
        app.setStyleSheet(LIGHT_THEME)
    elif theme == "Light Mini":
        app.setStyleSheet(LIGHT_Minimalistic)


def get_plot_colors():
    """
    A helper function that returns
    'white' for dark themes and 'black' for light themes,
    ensuring that text on dashboard charts remains readable.
    """
    try:
        if current_theme_name and "Dark" in str(current_theme_name):
            return 'white'
        return 'black'
    except Exception:
        return 'black'


# =========================
# Admin Functions
# =========================

def add_user_item(username, list_widget, mode, refresh_callback):
    """
    Creates a custom UI element (button) for a specific user in the admin list.
    It links the button to the ban/unban logic and handles the refresh callback for the list.
    """
    item = QListWidgetItem(list_widget)
    item_widget = QWidget()
    layout = QHBoxLayout(item_widget)
    layout.setContentsMargins(5, 2, 5, 2)

    btn = QPushButton(f"User: {username}")
    btn.setStyleSheet("text-align: left; padding: 8px; font-size: 14px;")

    btn.clicked.connect(lambda: show_ban_dialog(username, mode, refresh_callback))

    layout.addWidget(btn)

    item.setSizeHint(item_widget.sizeHint())
    list_widget.addItem(item)
    list_widget.setItemWidget(item, item_widget)

def open_unbanned():
    """
    Loads the admin view for managing active users.
    It queries the database for users who are not
    banned and renders them into the management list.
    """
    global current_active_window
    window = load_ui("UI/Unbanned.ui")
    prev_window = current_active_window
    current_active_window = window

    user_list_widget = window.findChild(QListWidget, "User_list")
    back_button = window.findChild(QPushButton, "pushButton")
    storage = simargl.LoginStorage("users_db")

    def refresh_list():
        user_list_widget.clear()
        users_data = storage.load()
        for row in users_data.fetchall():
            if row[3] == 0:
                add_user_item(row[1], user_list_widget, "ban", refresh_list)

    refresh_list()
    back_button.clicked.connect(lambda: open_admin(window))
    window.show()
    if prev_window:
        prev_window.close()


def open_banned():
    """
    Loads the admin view for managing restricted users.
    It specifically filters the database for entries with a
    "banned" status and allows admins to lift restrictions.
    """
    global current_active_window
    window = load_ui("UI/Unbanned.ui")
    window.setWindowTitle("Banned Users")

    label = window.findChild(QLabel, "Users")
    if label:
        label.setText("Banned Users")

    prev_window = current_active_window
    current_active_window = window

    user_list_widget = window.findChild(QListWidget, "User_list")
    back_button = window.findChild(QPushButton, "pushButton")

    storage = simargl.LoginStorage("users_db")

    def refresh_list():
        user_list_widget.clear()
        users_data = storage.load()
        if users_data:
            for row in users_data.fetchall():
                if row[3] == 1:
                    add_user_item(row[1], user_list_widget, "unban", refresh_list)

    refresh_list()
    back_button.clicked.connect(lambda: open_admin(window))
    window.show()
    prev_window.close()


def show_ban_dialog(username, mode, refresh_callback):
    """
    Displays a confirmation dialog that allows an administrator
    to change a user's status. It directly interacts with the LoginStorage to update the database.
    """
    dialog = load_ui("UI/Ban_Dialogue.ui")
    ban_btn = dialog.findChild(QPushButton, "Ban")
    unban_btn = dialog.findChild(QPushButton, "Unban")

    storage = simargl.LoginStorage("users_db")

    def handle_ban():
        storage.set_ban_status(username, 1)
        dialog.accept()
        refresh_callback()

    def handle_unban():
        storage.set_ban_status(username, 0)
        dialog.accept()
        refresh_callback()

    if ban_btn:
        ban_btn.clicked.connect(handle_ban)
    if unban_btn:
        unban_btn.clicked.connect(handle_unban)

    dialog.exec()

def open_admin(main_window):
    """
    Opens the main administrator dashboard.
    It provides navigation to user management sections
    (Banned/Unbanned) and allows the admin to log out.
    """
    admin_window = load_ui("UI/Admin.ui")
    global current_active_window
    current_active_window = admin_window

    ban_button = admin_window.findChild(QPushButton, "Ban_Button")
    ban_button.clicked.connect(
        lambda: open_unbanned()
    )
    unban_button = admin_window.findChild(QPushButton, "Unban_Button")
    unban_button.clicked.connect(
        lambda: open_banned()
    )
    back_button = admin_window.findChild(QPushButton, "Back_Button")
    back_button.clicked.connect(
        lambda: universal_logout()
    )

    admin_window.show()
    main_window.close()

    main_window.courses_window = admin_window

# =========================
# Window Switch
# =========================

def open_courses(menu_window):
    """
    Displays a table populated with the user's active courses fetched from Stud.IP
    """
    global user_courses

    courses_window = load_ui("UI/courses.ui")
    exit_button = courses_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(courses_window)
    )
    help_btn = courses_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(courses_window, "courses"))
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
    """
    The initialization step for the calendar.
    It opens a dialog to verify which courses happen
    on which days before proceeding to show the graphical calendar.
    """
    storage = simargl.CourseDaysStorage(current_login)

    dialog = CourseDayDialog(
        courses=user_courses,
        storage=storage,
        parent=menu_window
    )

    if dialog.exec():
        open_calendar(menu_window)


def open_calendar(menu_window):
    """
    Generates a monthly calendar view where users can click on specific days to see their scheduled lectures.
    """
    calendar_window = load_ui("UI/calendar.ui")

    exit_button = calendar_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(calendar_window)
    )

    help_btn = calendar_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(calendar_window, "calendar"))

    storage = simargl.CourseDaysStorage(current_login)
    course_days = storage.load()  # { course_title: "MO" }

    weekly_schedule.clear()

    for entry in schedule.entries:
        day = course_days.get(entry.related_course_id)
        if day:
            weekly_schedule[day].append(entry)

    calendar_widget = calendar_window.findChild(QWidget, "Calendar")
    grid = calendar_widget.findChild(QGridLayout, "gridLayout_2")

    buttons = []
    for i in range(grid.count()):
        widget = grid.itemAt(i).widget()
        if isinstance(widget, QPushButton):
            buttons.append(widget)

    buttons_with_pos = []
    for btn in buttons:
        index = grid.indexOf(btn)
        row, col, _, _ = grid.getItemPosition(index)
        buttons_with_pos.append((row, col, btn))

    buttons_with_pos.sort(key=lambda x: (x[0], x[1]))
    buttons_sorted = [b[2] for b in buttons_with_pos]

    # ===== CURRENT DATE =====
    today = datetime.now().date()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_days = list(cal.itermonthdays(year, month))

    def on_day_clicked(day):
        clicked_date = datetime(year, month, day).date()
        weekday_code = WEEKDAY_MAP[clicked_date.weekday()]

        entries = weekly_schedule.get(weekday_code, [])

        dialog = DayScheduleDialog(
            title=clicked_date.strftime("%A %d.%m.%Y"),
            entries=entries,
            parent=calendar_window
        )
        dialog.exec()

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
    """
    Fetches private messages from the Stud.IP platform.
    It creates a list of buttons where each button
    represents a message that can be opened for reading.
    """
    StudIP_window = load_ui("UI/StudIP.ui")

    exit_button = StudIP_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(StudIP_window)
    )

    help_btn = StudIP_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(StudIP_window, "studip"))

    messages_list = StudIP_window.findChild(QListWidget, "messagesList")

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
    """
    Uses the Stud.IP API to fetch the full body and sender
    details of a selected message and displays them in a formatted window.
    """
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
    """
    Opens the inbox view, listing recent emails and providing access to the "Compose" feature.
    """
    Email_window = load_ui("UI/Email.ui")

    exit_button = Email_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(lambda: open_menu(Email_window))

    write_button = Email_window.findChild(QPushButton, "Write_Button")
    write_button.clicked.connect(lambda: open_Compose_Email(Email_window))
    load_ecampus_mail_data(Email_window)

    help_btn = Email_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(Email_window, "email"))

    Email_window.show()
    menu_window.close()
    menu_window.courses_window = Email_window


def open_Compose_Email(Email_window):
    """
    Handles the email creation UI, including logic for selecting file
    attachments and sending data via the university SMTP server.
    """
    global current_active_window
    window = load_ui("UI/Send_Email.ui")
    prev_window = current_active_window
    current_active_window = window
    mail_client = ecampusmail

    sender_line = window.findChild(QLineEdit, "Sender_line")
    receiver_line = window.findChild(QLineEdit, "Receiver_line")
    subject_line = window.findChild(QLineEdit, "Subject_line")
    email_text_edit = window.findChild(QTextEdit, "Email_text")
    send_btn = window.findChild(QPushButton, "Send_email")

    add_files_btn = window.findChild(QPushButton, "Add_files")
    selected_file = None

    if sender_line:
        sender_line.setText(f"{current_login}@stud.uni-goettingen.de")

    def handle_add_file():
        nonlocal selected_file
        file_path, _ = QFileDialog.getOpenFileName(window, "Choose File", "", "All Files (*)")
        if file_path:
            selected_file = file_path
            add_files_btn.setText(f"File: {os.path.basename(file_path)}")  # Display the file name on the button
    if add_files_btn:
        add_files_btn.clicked.connect(handle_add_file)

    def handle_send():
        try:
            text = email_text_edit.toPlainText()
            subject = subject_line.text()
            sender = sender_line.text()
            receiver = receiver_line.text()

            if not receiver or not text:
                QMessageBox.warning(window, "Error", "Fill all the fields!")
                return

            mail_client.send_email(text, subject, sender, receiver, filename=selected_file)

            QMessageBox.information(window, "Success", "Email sent!")
            open_Email(window)
            window.close()

        except Exception as e:
            QMessageBox.critical(window, "Error", f"Could not send Email: {str(e)}")

    if send_btn:
        send_btn.clicked.connect(handle_send)
    window.show()
    Email_window.close()

def open_Diagram(Dashboard_window):
    Diagram_window = load_ui("UI/Diagram.ui")

    Back_button = Diagram_window.findChild(QPushButton, "Back_Button")
    Back_button.clicked.connect(lambda: open_Dashboard(Diagram_window))

    Diagram_window.show()
    Dashboard_window.close()
    Dashboard_window.courses_window = Diagram_window

def open_Dashboard(menu_window):
    """
    Integrates Matplotlib canvases to show visual data, such as course distribution (pie chart),
    email activity (heatmap), and study time (bar chart).
    """
    try:
        Dashboard_window = load_ui("UI/dashboard_test.ui")
    except Exception as e:
        QMessageBox.warning(menu_window, "Error", f"Failed to load dashboard: {str(e)}")
        return

    # Pie chart of course distribution
    target_1 = Dashboard_window.findChild(QWidget, "Dashboard_1")
    if target_1:
        try:
            fig_pie = get_pie_chart(schedule, text_color=get_plot_colors())
            if fig_pie:
                fig_pie.patch.set_alpha(0.0)
                canvas_1 = FigureCanvasQTAgg(fig_pie)
                canvas_1.setStyleSheet("background-color: transparent;")
                layout_1 = QVBoxLayout(target_1)
                layout_1.addWidget(canvas_1)
                target_1.setLayout(layout_1)
        except Exception:
            pass  # Pie chart optional, continue without it

    # Heat map of email activity
    target_2 = Dashboard_window.findChild(QWidget, "Dashboard_2")
    if target_2:
        try:
            fig_heat = get_heatmap(ecampusmail, color=get_plot_colors())
            if fig_heat:
                fig_heat.patch.set_alpha(0.0)
                canvas_2 = FigureCanvasQTAgg(fig_heat)
                canvas_2.setStyleSheet("background-color: transparent;")
                layout_2 = QVBoxLayout(target_2)
                layout_2.addWidget(canvas_2)
                target_2.setLayout(layout_2)
        except Exception:
            pass  # Heatmap optional, continue without it

    # Bar chart of study time + timer with its buttons
    canvas_bar = None
    target_3 = Dashboard_window.findChild(QWidget, "Dashboard_3")
    if target_3:
        try:
            fig_bar = get_weekly_bar_chart()
            if fig_bar:
                canvas_bar = FigureCanvasQTAgg(fig_bar)
                canvas_bar.setStyleSheet("background-color: transparent;")

                if not target_3.layout():
                    QVBoxLayout(target_3).setContentsMargins(0, 0, 0, 0)
                target_3.layout().addWidget(canvas_bar)

                apply_bar_theme(canvas_bar, current_theme_name)

                save_btn = Dashboard_window.findChild(QPushButton, "Save_Button")
                if save_btn:
                    save_btn.clicked.connect(lambda: save_tracker_data(Dashboard_window, canvas_bar, current_theme_name))

                reset_btn = Dashboard_window.findChild(QPushButton, "Reset_Button")
                if reset_btn:
                    def run_reset():
                        try:
                            clear_all_data()
                            refresh_stacked_bar(canvas_bar)
                            apply_bar_theme(canvas_bar, current_theme_name)
                            if canvas_bar and hasattr(canvas_bar, 'draw'):
                                canvas_bar.draw()
                        except Exception:
                            pass
                    reset_btn.clicked.connect(run_reset)

                start_btn = Dashboard_window.findChild(QPushButton, "Start_Button")
                if start_btn:
                    def run_start():
                        try:
                            global active_timer_day
                            study_timer.start()
                            active_timer_day = start_study_session()
                        except Exception:
                            pass
                    start_btn.clicked.connect(run_start)

                stop_btn = Dashboard_window.findChild(QPushButton, "Stop_Button")
                if stop_btn:
                    stop_btn.clicked.connect(lambda: stop_timer_and_save(canvas_bar, current_theme_name))
        except Exception:
            pass  # Bar chart optional, continue without it

    try:
        exit_button = Dashboard_window.findChild(QPushButton, "Back_Button")
        if exit_button:
            exit_button.clicked.connect(lambda: open_menu(Dashboard_window))

        diagram_button = Dashboard_window.findChild(QPushButton, "Diagram")
        if diagram_button:
            diagram_button.clicked.connect(lambda: open_Diagram(Dashboard_window))

        help_btn = Dashboard_window.findChild(QPushButton, "Help_Button")
        if help_btn:
            help_btn.clicked.connect(lambda: show_universal_help(Dashboard_window, "dashboard"))

        Dashboard_window.show()
        menu_window.close()
        menu_window.courses_window = Dashboard_window
    except Exception as e:
        QMessageBox.warning(menu_window, "Error", f"Failed to open dashboard: {str(e)}")


def open_Notes(menu_window):
    """
    Opens the personal note manager.
    It loads all existing notes from the user's local storage
    and provides functionality to create new entries or save edits.
    """
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
    help_btn = Notes_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(Notes_window, "notes"))

    notes = notes_storage.load_notes()

    for note in notes:
        notes_list.addItem(note["title"])

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

    def load_note(item):
        title = item.text()
        for note in notes:
            if note["title"] == title:
                text_edit.setPlainText(note["content"])
                break

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
    """
    Displays a theme selection window.
    It captures the user's choice (e.g., "Dark Mini")
    and calls change_theme to update the entire application's look.
    """
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
    """
    Opens the "External Help" window accessible from the menu screen,
    providing general contact information and developer credits.
    """
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
        \n Among them you can use: 
        \n- Active user courses  \n- Current month calendar \n- List of incoming Stud.ip messages \n- Ecampusmail incoming message list \n- Ability to create and edit notes \n- Customize your settings""")
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
    """
    Opens the "External Help" window accessible from the pre-login screen,
    providing general contact information and developer credits.
    """
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

def show_universal_help(parent_window, context_key):
    """
    Displays a modal dialog containing help information.
    It fetches HTML content from the HELP_TEXTS dictionary based on the provided context_key.
    """
    help_dialog = load_ui("UI/Universal_Help.ui")
    help_text_widget = help_dialog.findChild(QTextBrowser, "Helptext")

    if help_text_widget:
        content = HELP_TEXTS.get(context_key, "No help content available for this section.")
        help_text_widget.setHtml(content)

    help_dialog.setWindowModality(Qt.WindowModal)
    help_dialog.exec()


def open_menu(main_window):
    """
    Acts as the main navigation hub.
    It initializes the dashboard menu, updates mail and Stud.IP message counters using a ThreadPoolExecutor,
    and connects all sidebar buttons to their respective views.
    """
    menu_window = load_ui("UI/menu.ui")
    mail_notifications = menu_window.findChild(QLabel, "Ecampus_Mail")
    message_notifications = menu_window.findChild(QLabel, "StudIP_Messages")
    with ThreadPoolExecutor(max_workers=2) as executor:
        def update_mail_label():
            try:
                count = ecampusmail.mail_notifications() if ecampusmail else 0
                mail_notifications.setText(f"ECampus Mail ({count})")
            except Exception:
                mail_notifications.setText("ECampus Mail (?)")
        
        def update_studip_label():
            try:
                count = studip.new_messages_counter() if studip else 0
                message_notifications.setText(f"StudIP ({count})")
            except Exception:
                message_notifications.setText("StudIP (?)")
        
        executor.submit(update_mail_label)
        executor.submit(update_studip_label)

    name_label = menu_window.findChild(QLabel, "Name_label")
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
    """
    Handles the transition from the menu back to the login/main screen.
    It cleans up active mail server connections and checks for "Remember Me" data in the local database.
    """
    main_window = load_ui("UI/main.ui")
    setup_auto_logout(main_window)
    global current_active_window
    current_active_window = main_window

    try:
        if ecampusmail.server and ecampusmail.mail:
            ecampusmail.close_conections()
            ecampusmail.server = False
            ecampusmail.mail = False
    except:
        QMessageBox.warning(prelogin_window, "Error", "Incorrect Login or Password")

    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(QApplication.instance(), text)
    )

    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/remember_database.db"
    if os.path.exists(remember_path):
        remember_database = simargl.LoginStorage("remember_database")
        db_data = remember_database.load().fetchall()
        login_box = main_window.findChild(QLineEdit, "LoginLine")
        login_box.setText(db_data[0][1])
        remember_check.click()

    remember_check.clicked.connect(
        lambda: check_box_remember(remember_check)
    )

    change_theme(QApplication.instance(), theme_box.currentText())

    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window, remember)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )

    logout_btn = main_window.findChild(QPushButton, "Logout")
    if logout_btn:
        logout_btn.clicked.connect(lambda: universal_logout())

    main_window.show()
    menu_window.close()

# =========================
# Second Login
# =========================


def login_from_enter(main_window, remember=False):
    """
    The core authentication handler.
    It collects credentials, initializes Stud.IP and ECampusMail clients,
    loads user courses/schedules, and stops the auto-logout timer upon a successful login.
    """
    global user_courses, current_login, schedule, ecampusmail, studip, messages
    login_box = main_window.findChild(QLineEdit, "LoginLine")
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    current_login = login_box.text()
    password = password_box.text()

    studip = simargl.StudIP(current_login, password)
    ecampusmail = simargl.ECampusMail(current_login, password)

    try:
        initialize_tracker(current_login)
    except Exception:
        pass 

    try:
        studip.create_client()
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(ecampusmail.read_email_init())
            executor.submit(ecampusmail.write_email_init())
    except:
        QMessageBox.warning(prelogin_window, "Error", "Incorrect Login or Password")
    else:
        if remember:
            remember_database = simargl.LoginStorage("remember_database")
            if not remember_database.user_exists(current_login):
                remember_database.create(current_login, password, " ")

        global notes_storage
        notes_storage = simargl.NotesStorage(current_login)
        if hasattr(main_window, 'auto_logout_timer'):
            main_window.auto_logout_timer.stop()
        open_menu(main_window)

        user_courses = studip.get_courses()
        schedule = studip.get_schedule()
        messages = studip.get_my_messages()

def check_box_remember(checkbox: QCheckBox):
    """
    A toggle handler for the "Remember Me" checkbox.
    It updates a global boolean flag that determines if
    login data should be persisted in the local database.
    """
    global remember
    if checkbox.isChecked():
        remember = True
    if not checkbox.isChecked():
        remember = False


def universal_logout():
    """
    Resets the application state by clearing login fields,
    closing all active windows except the pre-login screen,
    and displaying a "Thank You" message to the user.
    """
    global current_active_window, prelogin_window

    if not prelogin_window:
        prelogin_window = load_ui("UI/prelogin.ui")

    login_box = prelogin_window.findChild(QLineEdit, "LoginLine")
    pass_box = prelogin_window.findChild(QLineEdit, "PasswordLine")
    if login_box:
        login_box.clear()
    if pass_box:
        pass_box.clear()

    prelogin_window.show()

    if current_active_window and current_active_window != prelogin_window:
        current_active_window.close()

    current_active_window = prelogin_window

    QMessageBox.information(prelogin_window, "Dialogue", "Thank you for using Simargl")

# =========================
# Registration
# =========================

def open_registration(prelogin_window, storage):
    """
    Loads the user registration UI.
    It includes a sub-function create_user that validates inputs and saves
    a new user (including admin status) into the local SQLite database.
    """
    reg_window = load_ui("UI/new_user.ui")

    def create_user():
        admin_checkbox = reg_window.findChild(QCheckBox, "AdminCheck")
        login = reg_window.findChild(QLineEdit, "LoginLine").text().strip()
        password = reg_window.findChild(QLineEdit, "PasswordLine").text().strip()
        real_name = reg_window.findChild(QLineEdit, "NameLine").text().strip()

        is_admin_value = 1 if admin_checkbox and admin_checkbox.isChecked() else 0

        if not login or not password or not real_name:
            QMessageBox.warning(
                reg_window,
                "Input Error",
                "Please fill in all fields: Name, Login, and Password!"
            )
            return

        if storage.user_exists(login):
            QMessageBox.warning(
                reg_window,
                "Error",
                f"Login '{login}' is already taken. Please choose another one."
            )
            return
        success = storage.create(login, password, real_name, is_admin=is_admin_value)

        if success:
            QMessageBox.information(
                reg_window,
                "Success",
                f"User {login} successfully registered!"
            )
            reg_window.accept()

        else:
            QMessageBox.critical(
                reg_window,
                "Database Error",
                "Something went wrong while saving to the database."
            )

    create_btn = reg_window.findChild(QPushButton, "Create")
    if create_btn:
        create_btn.clicked.connect(create_user)

    reg_window.exec()

def handle_auth(prelogin_window, storage):
    """
    Validates credentials against the users_db.
    It specifically checks if a user is banned
    or if they have administrative privileges to route them
    to either the Admin panel or the standard App.
    """
    login = prelogin_window.findChild(QLineEdit, "LoginLine").text()
    password = prelogin_window.findChild(QLineEdit, "PasswordLine").text()

    if not login or not password:
        QMessageBox.warning(prelogin_window, "Caution", "Enter login and password!")
        return

    if storage.compare(login, password):
        storage.cur.execute("SELECT banned, is_admin FROM users WHERE login = ?", (login,))
        result = storage.cur.fetchone()

        if result:
            is_banned, is_admin = result

            if is_banned == 1:
                QMessageBox.critical(
                    prelogin_window,
                    "Access Denied",
                    f"User {login} was banned!"
                )
                return

            if is_admin == 1:
                print(f"Admin login: {login}")
                open_admin(prelogin_window)
            else:
                print(f"User login: {login}")
                start_main_app(prelogin_window)
    else:
        QMessageBox.critical(prelogin_window, "Error", "Login or password is incorrect!")


# =========================
# Main Start
# =========================

def start_main_app(prelogin_window):
    """
    A setup function that prepares the main.ui window after the initial pre-login phase,
    ensuring themes, logout buttons, and auto-logout logic are correctly linked.
    """
    global remember, remember_path
    remember = False
    prelogin_window.hide()

    main_window = load_ui("UI/main.ui")
    setup_auto_logout(main_window)
    app = QApplication.instance()
    global current_active_window
    current_active_window = main_window

    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    if theme_box:
        theme_box.currentTextChanged.connect(lambda t: change_theme(app, t))
        change_theme(app, theme_box.currentText())

    logout_btn = main_window.findChild(QPushButton, "Logout")
    if logout_btn:
        logout_btn.clicked.connect(lambda: universal_logout())

    enter_btn = main_window.findChild(QPushButton, "Enter")
    if enter_btn:
        enter_btn.clicked.connect(lambda: login_from_enter(main_window, remember))

    help_btn = main_window.findChild(QPushButton, "Help")
    if help_btn:
        help_btn.clicked.connect(lambda: open_Help(main_window))

    # Remember Me checkbox
    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/remember_database.db"
    if os.path.exists(remember_path):
        remember_database = simargl.LoginStorage("remember_database")
        db_data = remember_database.load().fetchall()
        login_box = main_window.findChild(QLineEdit, "LoginLine")
        login_box.setText(db_data[0][1])
        remember_check.click()

    remember_check.clicked.connect(
        lambda: check_box_remember(remember_check)
    )

    main_window.show()
    prelogin_window.main_ref = main_window


def main():
    """
    The application entry point.
    It initializes the QApplication, sets up the user database storage,
    applies the initial theme, and displays the prelogin.ui window.
    """
    global prelogin_window, current_active_window

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)


    storage = simargl.LoginStorage("users_db")

    prelogin_window = load_ui("UI/prelogin.ui")
    current_active_window = prelogin_window


    theme_box_pre = prelogin_window.findChild(QComboBox, "ThemeBox")
    if theme_box_pre:
        change_theme(app, theme_box_pre.currentText())
        theme_box_pre.currentTextChanged.connect(lambda t: change_theme(app, t))

    enter_btn = prelogin_window.findChild(QPushButton, "Enter_main")
    if enter_btn:
        enter_btn.clicked.connect(
            lambda: handle_auth(prelogin_window, storage)
        )

    new_user_btn = prelogin_window.findChild(QPushButton, "NewUser")
    if new_user_btn:
        new_user_btn.clicked.connect(
            lambda: open_registration(prelogin_window, storage)
        )

    off_button = prelogin_window.findChild(QPushButton, "Turnoff")
    if off_button:
        off_button.clicked.connect(
            lambda: app.quit()
        )

    # When quitting disconnect the ecampusmail for safety
    app.aboutToQuit.connect(lambda: ecampusmail.close_conections() if 'ecampusmail' in globals() else None)

    prelogin_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()