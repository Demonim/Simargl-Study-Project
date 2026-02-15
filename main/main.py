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
    QMessageBox
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QSize, Qt, QTimer
from PySide6.QtWidgets import QApplication, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from themes import *
from dashboard.pie.subject_hours import subject_hours
from dashboard.pie.create_pie import create_pie
from dashboard.heatmap.create_heatmap import create_heatmap
from dashboard.timer_bar.weekly_study_tracker import WeeklyStudyTracker
from dashboard.timer_bar.create_bar import create_stacked_bar, update_stacked_bar
from dashboard.timer_bar.study_timer import Study_Timer

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
admin_login = "Admin"
admin_password = "Admin"
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


def setup_auto_logout(window):
    window.auto_logout_timer = QTimer(window)
    window.auto_logout_timer.setSingleShot(True)

    window.auto_logout_timer.timeout.connect(universal_logout)

    window.auto_logout_timer.start(300000)


def save_tracker_data(dashboard_window, canvas_bar, tracker, theme):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for day in days:
        h_line = dashboard_window.findChild(QLineEdit, f"{day}_H")
        m_line = dashboard_window.findChild(QLineEdit, f"{day}_M")

        if h_line and m_line:
            try:

                h = float(h_line.text()) if h_line.text().strip() else 0.0
                m = float(m_line.text()) if m_line.text().strip() else 0.0

                total_hours = h + (m / 60.0)
                tracker.set_day(day, total_hours)
            except ValueError:
                continue

    update_stacked_bar(canvas_bar.figure, tracker.all())
    apply_bar_theme(canvas_bar, current_theme_name)
    canvas_bar.draw()


def choose_day_and_start(parent_window):
    global active_timer_day

    loader = QUiLoader()
    ui_file = QFile("UI/Dashboard_dialogue.ui")
    if not ui_file.open(QFile.ReadOnly):
        return
    dialog = loader.load(ui_file, parent_window)
    ui_file.close()

    def handle_selection(day_code):
        global active_timer_day
        active_timer_day = day_code
        study_timer.start()
        print(f"Таймер запущен для: {day_code}")
        dialog.accept()

    days_buttons = ["Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue"]
    for day_name in days_buttons:
        btn = dialog.findChild(QPushButton, day_name)
        if btn:
            btn.clicked.connect(lambda checked, d=day_name: handle_selection(d))

    dialog.exec()


def stop_timer_and_save(canvas_bar, tracker, current_theme):
    global active_timer_day
    if study_timer.running and active_timer_day:
        study_timer.stop()
        hours = study_timer.hours()

        tracker.add_time(active_timer_day, hours)
        study_timer.reset()

        update_stacked_bar(canvas_bar.figure, tracker.all())

        apply_bar_theme(canvas_bar, current_theme)

        active_timer_day = None
        print(f"Таймер остановлен. Добавлено {hours:.2f} ч.")


def apply_bar_theme(canvas_bar, theme):
    txt_col = 'white' if "Dark" in theme else 'black'
    fig = canvas_bar.figure
    ax = fig.gca()

    ax.tick_params(colors=txt_col)
    ax.xaxis.label.set_color(txt_col)
    ax.yaxis.label.set_color(txt_col)

    for spine in ax.spines.values():
        spine.set_edgecolor(txt_col)

    canvas_bar.draw()


def load_ecampus_mail_data(Email_window):
    global ecampusmail

    # Находим список в интерфейсе
    messages_list = Email_window.findChild(QListWidget, "messagesList")
    if not messages_list:
        return

    # Очищаем список перед загрузкой
    messages_list.clear()

    try:
        # ЗАГРУЗКА: Программа остановится здесь до получения ответа от сервера
        subjects, dates = ecampusmail.show_subjects(100)
        subjects = subjects[::-1]
        dates = dates[::-1]

        for i in range(len(subjects)):
            # Создаем контейнер для строки
            item_widget = QWidget()
            layout = QHBoxLayout(item_widget)
            layout.setContentsMargins(5, 2, 5, 2)

            # Создаем кнопку как в StudIP
            display_text = f"{dates[i]} | {subjects[i]}"
            msg_button = QPushButton(display_text)
            msg_button.setStyleSheet("text-align: left; padding: 10px;")

            # Привязываем открытие письма по индексу i
            msg_button.clicked.connect(lambda ch=False, idx=i: open_mail_content(idx))

            layout.addWidget(msg_button)

            # Добавляем виджет в QListWidget
            list_item = QListWidgetItem(messages_list)
            list_item.setSizeHint(item_widget.sizeHint())
            messages_list.addItem(list_item)
            messages_list.setItemWidget(list_item, item_widget)

    except Exception as e:
        print(f"Ошибка при получении почты: {e}")


def open_mail_content(mail_index):
    global ecampusmail

    try:
        # 1. Вызываем ваш метод из simargl.py
        # Он возвращает объект email.message.Message
        msg = ecampusmail.open_mail(mail_index)

        # 2. Извлекаем текст из этого объекта
        content = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        # 3. Показываем в окне (как в StudIP)
        dialog = QDialog()
        dialog.setWindowTitle(f"Письмо: {msg['Subject']}")
        dialog.setMinimumSize(600, 400)
        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(content)

        layout.addWidget(text_edit)
        dialog.exec()

    except Exception as e:
        print(f"Ошибка: {e}")


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

def change_theme(app, theme):
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
    if "Dark" in current_theme_name:
        return 'white'  # Цвет текста для темных тем
    else:
        return 'black'  # Цвет текста для светлых тем


# =========================
# WINDOW SWITCH
# =========================
def add_user_item(username, list_widget, mode, refresh_callback):
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
    global current_active_window
    window = load_ui("UI/Unbanned.ui")
    prev_window = current_active_window
    current_active_window = window

    user_list_widget = window.findChild(QListWidget, "User_list")
    back_button = window.findChild(QPushButton, "pushButton")
    storage = simargl.LoginStorage("users_db")

    def refresh_list():
        user_list_widget.clear()
        users_data = storage.load() # Возвращает SELECT * FROM users
        for row in users_data.fetchall():
            # row[0] - name, row[2] - banned_status
            if row[2] == 0:
                add_user_item(row[0], user_list_widget, "ban", refresh_list)

    refresh_list()
    back_button.clicked.connect(lambda: open_admin(window))
    window.show()
    if prev_window: 
        prev_window.close()


def open_banned():
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
                if row[2] == 1:  # Показываем только забаненных
                    add_user_item(row[0], user_list_widget, "unban", refresh_list)

    refresh_list()
    back_button.clicked.connect(lambda: open_admin(window))
    window.show()
    prev_window.close()


def show_ban_dialog(username, mode, refresh_callback):
    dialog = load_ui("UI/Ban_Dialogue.ui")
    ban_btn = dialog.findChild(QPushButton, "Ban")
    unban_btn = dialog.findChild(QPushButton, "Unban")

    # Ссылка на ту же базу, что и в приложении
    storage = simargl.LoginStorage("users_db")

    def handle_ban():
        storage.set_ban_status(username, 1)
        dialog.accept()
        refresh_callback()

    def handle_unban():
        storage.set_ban_status(username, 0)
        dialog.accept()
        refresh_callback()

    # Привязываем действия к конкретным кнопкам
    if ban_btn: 
        ban_btn.clicked.connect(handle_ban)
    if unban_btn: 
        unban_btn.clicked.connect(handle_unban)

    dialog.exec()

def open_admin(main_window):
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


def open_courses(menu_window):
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

    help_btn = calendar_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(calendar_window, "calendar"))

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
    today = datetime.now().date()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_days = list(cal.itermonthdays(year, month))

    # ===== CLICK ON DAY =====
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

    help_btn = StudIP_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(StudIP_window, "studip"))

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
    global current_active_window
    window = load_ui("UI/Send_Email.ui")
    prev_window = current_active_window
    current_active_window = window
    mail_client = ecampusmail

    # Поиск элементов интерфейса
    sender_line = window.findChild(QLineEdit, "Sender_line")
    receiver_line = window.findChild(QLineEdit, "Receiver_line")
    subject_line = window.findChild(QLineEdit, "Subject_line")
    email_text_edit = window.findChild(QTextEdit, "Email_text")

    send_btn = window.findChild(QPushButton, "Send_email")
    if sender_line:
        sender_line.setText(f"{current_login}@stud.uni-goettingen.de")

    def handle_send():
        try:
            text = email_text_edit.toPlainText()
            subject = subject_line.text()
            sender = sender_line.text()
            receiver = receiver_line.text()

            if not receiver or not text:
                QMessageBox.warning(window, "Error", "Fill all the fields!")
                return

            mail_client.send_email(text, subject, sender, receiver)
            QMessageBox.information(window, "Success", "Email send!")

            open_Email(window)
        except Exception as e:
            QMessageBox.critical(window, "Error", f"Could not send Email: {str(e)}")

    if send_btn:
        send_btn.clicked.connect(handle_send)

    window.show()
    if prev_window:
        prev_window.close()


def open_Dashboard(menu_window):
    Dashboard_window = load_ui("UI/dashboard_test.ui")

    target_1 = Dashboard_window.findChild(QWidget, "Dashboard_1")
    if target_1 and schedule:
        data_pie = subject_hours(schedule)
        fig_pie = create_pie(data_pie, text_color=get_plot_colors())
        fig_pie.patch.set_alpha(0.0)

        canvas_1 = FigureCanvasQTAgg(fig_pie)
        canvas_1.setStyleSheet("background-color: transparent;")
        layout_1 = QVBoxLayout(target_1)
        layout_1.addWidget(canvas_1)
        target_1.setLayout(layout_1)

    target_2 = Dashboard_window.findChild(QWidget, "Dashboard_2")
    if target_2:
        subjects_data, dates_data = ecampusmail.show_subjects(last_n=200)

        fig_heat = create_heatmap(subjects_data, dates_data, color=get_plot_colors())
        fig_heat.patch.set_alpha(0.0)

        canvas_2 = FigureCanvasQTAgg(fig_heat)
        canvas_2.setStyleSheet("background-color: transparent;")
        layout_2 = QVBoxLayout(target_2)
        layout_2.addWidget(canvas_2)
        target_2.setLayout(layout_2)

    target_3 = Dashboard_window.findChild(QWidget, "Dashboard_3")

    tracker_obj = WeeklyStudyTracker(filename="storage/study_data.json")

    if target_3:
        fig_bar = create_stacked_bar(tracker_obj.all())
        canvas_bar = FigureCanvasQTAgg(fig_bar)
        canvas_bar.setStyleSheet("background-color: transparent;")

        if not target_3.layout():
            QVBoxLayout(target_3).setContentsMargins(0, 0, 0, 0)
        target_3.layout().addWidget(canvas_bar)

        apply_bar_theme(canvas_bar, current_theme_name)

        save_btn = Dashboard_window.findChild(QPushButton, "Save_Button")
        if save_btn:
            def run_save():
                save_tracker_data(Dashboard_window, canvas_bar, tracker_obj, current_theme_name)
                apply_bar_theme(canvas_bar, current_theme_name)

            save_btn.clicked.connect(run_save)

        reset_btn = Dashboard_window.findChild(QPushButton, "Reset_Button")
        if reset_btn:
            def run_reset():
                tracker_obj.reset_all()
                for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                    Dashboard_window.findChild(QLineEdit, f"{day}_H").clear()
                    Dashboard_window.findChild(QLineEdit, f"{day}_M").clear()
                update_stacked_bar(canvas_bar.figure, tracker_obj.all())
                apply_bar_theme(canvas_bar, current_theme_name)

            reset_btn.clicked.connect(run_reset)

        start_btn = Dashboard_window.findChild(QPushButton, "Start_Button")
        if start_btn:
            start_btn.clicked.connect(lambda: choose_day_and_start(Dashboard_window))

        stop_btn = Dashboard_window.findChild(QPushButton, "Stop_Button")
        if stop_btn:
            def run_stop():
                stop_timer_and_save(canvas_bar, tracker_obj, current_theme_name)
                apply_bar_theme(canvas_bar, current_theme_name)

            stop_btn.clicked.connect(run_stop)

    exit_button = Dashboard_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(lambda: open_menu(Dashboard_window))

    help_btn = Dashboard_window.findChild(QPushButton, "Help_Button")
    help_btn.clicked.connect(lambda: show_universal_help(Dashboard_window, "dashboard"))

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

def show_universal_help(parent_window, context_key):
    help_dialog = load_ui("UI/Universal_Help.ui")
    help_text_widget = help_dialog.findChild(QTextBrowser, "Helptext")

    if help_text_widget:
        content = HELP_TEXTS.get(context_key, "No help content available for this section.")
        help_text_widget.setHtml(content)

    help_dialog.setWindowModality(Qt.WindowModal)
    help_dialog.exec()


def open_menu(main_window):
    menu_window = load_ui("UI/menu.ui")
    mail_notifications = menu_window.findChild(QLabel, "Ecampus_Mail")
    message_notifications = menu_window.findChild(QLabel, "StudIP_Messages")
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(mail_notifications.setText(f"ECampus Mail ({ecampusmail.mail_notifications()})"), 1)
        executor.submit(message_notifications.setText(f"StudIP ({studip.new_messages_counter()})"), 2)

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
        raise Exception

    # Theme combobox
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(QApplication.instance(), text)
    )

    # Check box "Remember me"
    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/ecampus_login_data.db"
    if os.path.exists(remember_path):
        login_database = simargl.LoginStorage("ecampus_login_data")
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

    logout_btn = main_window.findChild(QPushButton, "Logout")
    if logout_btn:
        logout_btn.clicked.connect(lambda: universal_logout())

    main_window.show()
    menu_window.close()


def login_from_enter(main_window, remember=False):
    global user_courses, current_login, schedule, ecampusmail, studip, messages
    login_box = main_window.findChild(QLineEdit, "LoginLine")
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    current_login = login_box.text()
    password = password_box.text()

    studip = simargl.StudIP(current_login, password)
    ecampusmail = simargl.ECampusMail(current_login, password)

    tracker = WeeklyStudyTracker(filename=f"storage/{current_login}_study_data.json")

    try:
        studip.create_client()
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(ecampusmail.read_email_init())
            executor.submit(ecampusmail.write_email_init())
    except:
        QMessageBox.warning(prelogin_window, "Mistake", "Incorrect Login or Password")
    else:
        global notes_storage
        notes_storage = simargl.NotesStorage(current_login)
        if hasattr(main_window, 'auto_logout_timer'):
            main_window.auto_logout_timer.stop()

        open_menu(main_window)

        user_courses = studip.get_courses()
        schedule = studip.get_schedule()
        messages = studip.get_my_messages()

        globals()['tracker_instance'] = tracker


# =========================
# MAIN
# =========================

def check_box_remember(checkbox: QCheckBox):
    global remember
    if checkbox.isChecked():
        remember = True
    if not checkbox.isChecked():
        remember = False


def universal_logout():
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

    QMessageBox.information(prelogin_window, "Dialogue", "Thank you very much!")


def open_registration(prelogin_window, storage):
    """
    Handles the registration UI logic.
    Loads the UI, collects input, and calls storage to create a new user.
    """
    reg_window = load_ui("UI/new_user.ui")

    def create_user():
        login = reg_window.findChild(QLineEdit, "LoginLine").text().strip()
        password = reg_window.findChild(QLineEdit, "PasswordLine").text().strip()
        real_name = reg_window.findChild(QLineEdit, "NameLine").text().strip()

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
                "Mistake",
                f"Login '{login}' is already taken. Please choose another one."
            )
            return
        success = storage.create(login, password, real_name)

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

def start_main_app(prelogin_window):
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

    remember_check = main_window.findChild(QCheckBox, "Check_Remember")
    remember_path = "storage/ecampus_login_data.db"
    if os.path.exists(remember_path):
        login_database = simargl.LoginStorage("ecampus_login_data")
        db_data = login_database.load().fetchall()
        login_box = main_window.findChild(QLineEdit, "LoginLine")
        login_box.setText(db_data[0][0])
        remember_check.click()

    remember_check.clicked.connect(
        lambda: check_box_remember(remember_check)
    )

    main_window.show()
    prelogin_window.main_ref = main_window


def handle_auth(prelogin_window, storage):
    login = prelogin_window.findChild(QLineEdit, "LoginLine").text()
    password = prelogin_window.findChild(QLineEdit, "PasswordLine").text()

    if not login or not password:
        QMessageBox.warning(prelogin_window, "Caution", "Enter login and password!")
        return

    if login == "Admin" and password == "Admin":
        open_admin(prelogin_window)
        return


    if storage.compare(login, password):
        storage.cur.execute("SELECT banned FROM users WHERE login = ?", (login,))
        result = storage.cur.fetchone()

        if result and result[0] == 1:
            QMessageBox.critical(
                prelogin_window,
                "Access Denied",
                f"User {login} was banned!"
            )
            return

        start_main_app(prelogin_window)
    else:
        QMessageBox.critical(prelogin_window, "Mistake", "Login or password is incorrect!")


def main():
    global prelogin_window, current_active_window

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

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

    prelogin_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()