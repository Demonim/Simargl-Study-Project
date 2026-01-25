import sys
import os
from pydoc import Helper
from studipy.calendar import Calendar
import simargl
import json
import uuid
import datetime

from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
    QTextBrowser,
    QApplication,
    QComboBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QDialog,
    QListWidget,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QHBoxLayout,
)
import calendar
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


weekly_schedule = defaultdict(list)
schedule = None
user_courses = []
notes_storage = None
current_login = None
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

DARK_THEME = """
QWidget {
background-color: qlineargradient(spread:pad,x1:10, y1:0, x2:0, y2:1,
    stop:0.00 rgba(2, 7, 15, 255),

    stop:0.07 rgba(0, 255, 120, 220),
    stop:0.11 rgba(2, 7, 15, 255),

    stop:0.18 rgba(80, 255, 140, 200),
    stop:0.23 rgba(2, 7, 15, 255),

    stop:0.30 rgba(0, 220, 100, 220),
    stop:0.35 rgba(2, 7, 15, 255),

    stop:0.42 rgba(120, 255, 160, 190),
    stop:0.47 rgba(2, 7, 15, 255),

    stop:0.54 rgba(0, 255, 140, 230),
    stop:0.59 rgba(2, 7, 15, 255),

    stop:0.66 rgba(90, 255, 130, 200),
    stop:0.71 rgba(2, 7, 15, 255),

    stop:0.78 rgba(0, 230, 110, 220),
    stop:0.83 rgba(2, 7, 15, 255),

    stop:0.90 rgba(120, 255, 160, 210),
    stop:0.95 rgba(2, 7, 15, 255),

    stop:1.00 rgba(2, 7, 15, 255)
);
font-family: Unispace;
}




QLabel#Login {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Password{
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QCalendarWidget QComboBox {
    background-color: #333;
    color: white;
}

QLabel {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 20pt;
}

QLineEdit#PasswordLine {
    background-color: 255, 255, 255
}

QLineEdit#LoginLine {
    background-color: 255, 255, 255
}

QCheckBox#CheckBox_1 {
    color: rgb(102, 255, 140);
    background-color: rgb(255, 255, 255, 0);
    font-size: 10pt
}

QPushButton {
    border: 2px solid #00ff88;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(102, 255, 140);
    font-size: 15pt;
}

QPushButton:hover {
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}

QComboBox#ThemeBox {
    background-color:  #02070f;
    color: #00ff88;        
    border: 2px solid #00ff88;
    padding: 5px;
}

QComboBox#ThemeBox QAbstractItemView {
    background-color: #02070f; 
    color: white;             
    selection-background-color: #00ff88;
    selection-color: black;
}

QPushButton#Help {
    background-color: rgb(23, 130, 22);
    border: 2px solid #000000;
    border-radius: 6px;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}

QPushButton#Help:hover{
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}

QLabel#Error {
	color: rgb(0, 0, 0);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Error_2 {
	color: rgb(0, 0, 0);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QPushButton#Error_Button {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}


QPushButton#Back_Button{
    background-color: rgb(23, 130, 22);
    border: 2px solid #000000;
    border-radius: 6px;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}

QPushButton#Back_Button:hover{
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}



QLabel#Help {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 30pt;
}

QTextBrowser {
    color: rgb(102, 255, 140);
    border: 10px solid rgb(102, 255, 140);
    background-color: rgb(0, 0, 0);
    font: 15pt;
}

QLineEdit#Help_Search {
    background-color: rgba(255, 255, 255);
}



QTableWidget {
    background-color: #000000;
    color: rgb(102, 255, 140);
    gridline-color: rgb(102, 255, 140);
    font-size: 10pt;
}

QHeaderView::section {
    background-color: #02070f;
    color: #00ff88;
    padding: 8px;
    border: 1px solid #00ff88;
    font-weight: bold;
}


QCalendarWidget QWidget{
	alternate-background-color: rgb(17, 148, 28);
}

QCalendarWidget QAbstractItemView {
    background-color: rgb(33, 125, 60);
    color: white;
    selection-background-color: #00ff88;
    selection-color: black;
    gridline-color: #00ff88;
}

QCalendarWidget QToolButton {
    color: white;
    background: rgb(15, 59, 28);;
}

QCalendarWidget QToolButton:hover {
    background: #444;
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #3daee9;
    selection-color: black;
}

QCalendarWidget QAbstractItemView::item:disabled {
    color: gray;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(15, 59, 28);
}

QCalendarWidget QToolButton QMenu {
     background-color: rgb(15, 59, 28);
     color: white
}




QLabel#Ecampus{
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QTableView {
    background-color: rgba(255, 255, 255, 0);
}

QPushButton#Exit_Button {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}




QPushButton#Exit_Button1 {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}
"""

LIGHT_THEME = """
QWidget {
background-color:qlineargradient(spread:pad, x1:10, y1:0, x2:0, y2:1,
    stop:0.00 rgba(240, 247, 255, 255),

    stop:0.07 rgba(114, 163, 242, 220),
    stop:0.11 rgba(240, 247, 255, 255),

    stop:0.18 rgba(114, 163, 242, 200),
    stop:0.23 rgba(240, 247, 255, 255),

    stop:0.30 rgba(114, 163, 242, 220),
    stop:0.35 rgba(240, 247, 255, 255),

    stop:0.42 rgba(114, 163, 242, 190),
    stop:0.47 rgba(240, 247, 255, 255),

    stop:0.54 rgba(114, 163, 242, 230),
    stop:0.59 rgba(240, 247, 255, 255),

    stop:0.66 rgba(114, 163, 242, 200),
    stop:0.71 rgba(240, 247, 255, 255),

    stop:0.78 rgba(114, 163, 242, 220),
    stop:0.83 rgba(240, 247, 255, 255),

    stop:0.90 rgba(114, 163, 242, 210),
    stop:0.95 rgba(240, 247, 255, 255),

    stop:1.00 rgba(240, 247, 255, 255)
);
font-family: Unispace;
}



QLabel#Login {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Password{
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QCalendarWidget QComboBox {
    background-color: #333;
    color: white;
}

QLabel {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 20pt;
}

QLineEdit {
    background-color: 255, 255, 255
}

QCheckBox#CheckBox_1 {
    color: rgb(79, 149, 255);
    background-color: rgb(255, 255, 255, 0);
    font-size: 10pt
}

QPushButton {
    border: 2px solid #4f95ff;
    border-radius: 6px;
    background-color: transparent;
	color: rgb(79, 149, 255);
	font-size: 15pt;
}

QPushButton:hover {
    border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QComboBox#ThemeBox {
    background-color: #f0f7ff;
    color: #4f95ff;        
    border: 2px solid #4f95ff;
    padding: 5px;
}
QComboBox#ThemeBox QAbstractItemView {
    background-color: rgb(114, 163, 242);
    color: #f0f7ff;               
    selection-background-color: #00ff88;
    selection-color: white;
}

QPushButton#Help {
	border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QPushButton#Help:hover{
    border: 2px solid rgb(0,0,0);
    border-radius: 6px;
    background-color: rgb(20,111,161);
	color: rgb(79, 149, 255);
	font-size: 15pt;
}



QPushButton#Back_Button{
	border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QPushButton#Back_Button:hover{
    border: 2px solid rgb(0,0,0);
    border-radius: 6px;
    background-color: rgb(20,111,161);
	color: rgb(79, 149, 255);
	font-size: 15pt;
}

QLabel#Help {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 30pt;
}

QTextBrowser {
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
    font: 15pt;
}


QLineEdit#Help_Search {
    background-color: rgba(255, 255, 255);
}







QCalendarWidget QWidget{
	alternate-background-color: rgb(74, 222, 252);
}

QCalendarWidget QAbstractItemView {
    background-color: #ffffff;
    color: black;
    selection-background-color: #4f95ff;
    selection-color: white;
    gridline-color: #4f95ff;
}

QCalendarWidget QToolButton {
    color: rgb(46, 45, 45);
    background: rgb(79, 149, 255);
	border: 2px solid #4f95ff;
    border-radius: 6px;
}

QCalendarWidget QToolButton:hover {
    background: rgb(199, 199, 199);
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #3daee9;
    selection-color: black;
}

QCalendarWidget QAbstractItemView::item:disabled {
    color: white;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(79, 149, 255) ;
}

QCalendarWidget QToolButton QMenu {
     background-color: rgb(79, 149, 255);
     color: black
}




QLabel#Ecampus{
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QTableView {
    background-color: rgba(255, 255, 255, 0);
}

QPushButton#Exit_Button {
    border: 2px solid #ffffff;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}





QPushButton#Exit_Button1 {
    border: 2px solid #ffffff;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}
"""

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
            self.list.addItem("No classes this day")
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

        layout.addWidget(QLabel("Введите название заметки:"))
        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)

    def get_name(self):
        return self.line_edit.text().strip()

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

class CourseDayDialog(QDialog):
    def __init__(self, courses, storage, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set course days")
        self.setMinimumSize(600, 400)

        self.storage = storage
        self.saved_days = storage.load()

        self.layout = QVBoxLayout(self)
        self.list = QListWidget()
        self.layout.addWidget(self.list)

        self.inputs = {}

        for course in courses:
            widget = QWidget()
            row = QHBoxLayout(widget)

            label = QLabel(course.title)
            label.setMinimumWidth(350)

            input_day = QLineEdit()
            input_day.setPlaceholderText("MO / TU / WE ...")
            input_day.setMaximumWidth(80)

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
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

# =========================
# THEME HANDLING
# =========================

def change_theme(app: QApplication, theme: str):
    if theme == "Dark Theme":
        app.setStyleSheet(DARK_THEME)
    elif theme == "Light Theme":
        app.setStyleSheet(LIGHT_THEME)


# =========================
# WINDOW SWITCH
# =========================


def open_courses(menu_window):
    global user_courses

    courses_window = load_ui("courses.ui")
    exit_button = courses_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(courses_window)
    )
    table = courses_window.findChild(QTableWidget, "tableWidget")

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
    storage = CourseDaysStorage(current_login)

    dialog = CourseDayDialog(
        courses=user_courses,
        storage=storage,
        parent=menu_window
    )

    if dialog.exec():
        open_calendar(menu_window)

def open_calendar(menu_window):
    calendar_window = load_ui("calendar.ui")

    # ===== КНОПКА BACK =====
    exit_button = calendar_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: open_menu(calendar_window)
    )

    # ===== ЗАГРУЗКА СОХРАНЁННЫХ ДНЕЙ =====
    storage = CourseDaysStorage(current_login)
    course_days = storage.load()  # { course_title: "MO" }

    # ===== ФОРМИРОВАНИЕ WEEKLY_SCHEDULE =====
    weekly_schedule.clear()

    for entry in schedule.entries:
        day = course_days.get(entry.related_course_id)
        if day:
            weekly_schedule[day].append(entry)

    # ===== КАЛЕНДАРНАЯ СЕТКА =====
    calendar_widget = calendar_window.findChild(QWidget, "calendarWidget")
    grid = calendar_widget.findChild(QGridLayout, "gridLayout_2")

    # собрать кнопки
    buttons = []
    for i in range(grid.count()):
        widget = grid.itemAt(i).widget()
        if isinstance(widget, QPushButton):
            buttons.append(widget)

    # отсортировать по позиции
    buttons_with_pos = []
    for btn in buttons:
        index = grid.indexOf(btn)
        row, col, _, _ = grid.getItemPosition(index)
        buttons_with_pos.append((row, col, btn))

    buttons_with_pos.sort(key=lambda x: (x[0], x[1]))
    buttons_sorted = [b[2] for b in buttons_with_pos]

    # ===== ТЕКУЩИЙ МЕСЯЦ =====
    today = datetime.date.today()
    year = today.year
    month = today.month

    cal = calendar.Calendar(firstweekday=0)  # Monday
    month_days = list(cal.itermonthdays(year, month))

    # ===== КЛИК ПО ДНЮ =====
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

    # ===== ЗАПОЛНЕНИЕ КНОПОК =====
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
    StudIP_window = load_ui("StudIP.ui")

    exit_button = StudIP_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(StudIP_window)
    )

    StudIP_window.show()
    menu_window.close()

    menu_window.courses_window = StudIP_window

def open_Email(menu_window):
    Email_window = load_ui("Email.ui")

    exit_button = Email_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(Email_window)
    )

    Email_window.show()
    menu_window.close()

    menu_window.courses_window = Email_window

def open_Dashboard(menu_window):
    Dashboard_window = load_ui("Dashboard.ui")

    exit_button = Dashboard_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(Dashboard_window)
    )

    Dashboard_window.show()
    menu_window.close()

    menu_window.courses_window = Dashboard_window

def open_Notes(menu_window):
    global notes_storage
    Notes_window = load_ui("notes.ui")

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

def open_Help(main_window):
    Help_window = load_ui("help.ui")

    textBrowser = Help_window.findChild(QTextBrowser, "textBrowser")

    exit_button = Help_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(Help_window)
    )
    FAQ_button = Help_window.findChild(QPushButton, "FAQ")
    FAQ_button.clicked.connect(
        lambda: textBrowser.setText("What is this app for? \n- This app is designed to help students during their university studies.\nIs my personal data saved?\n- Yes, but user data is encrypted and stored in a local database.\nHow can I change my password?\n- After logging into my account, go to the Account Settings tab.")
    )
    Instructions_button = Help_window.findChild(QPushButton, "Instruction")
    Instructions_button.clicked.connect(
        lambda: textBrowser.setText("1. Enter your login details for Stud.Ip. \n2. After logging in, you will have access to a menu with all the application functions. \n Among them you can use: \n- Active user courses  \n- Current month calendar \n- List of incoming Stud.ip messages \n- Ecampusmail incoming message list \n- Ability to create and edit notes \n- Customize your settings")
    )
    Support_button = Help_window.findChild(QPushButton, "Support")
    Support_button.clicked.connect(
        lambda: textBrowser.setText("Contact the app owner and lead developer: \n-Dmytro Kutsak. \nIf you find bugs in UI, please contact: \n-Nichita Licov  \n-Diana Bardyk")
    )
    App_button = Help_window.findChild(QPushButton, "App")
    App_button.clicked.connect(
        lambda: textBrowser.setText("The Idea: Dmytro Kutsak.\nDesigned by: Nichita Licov and Diana Bardyk ")
    )

    Help_window.show()
    main_window.close()

    main_window.courses_window = Help_window

def open_menu(main_window):
    menu_window = load_ui("menu.ui")
    mail_notifications = menu_window.findChild(QLabel,"Ecampus_Mail")
    message_notifications = menu_window.findChild(QLabel,"StudIP_Messages")
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(mail_notifications.setText(f"ECampus Mail ({simargl.mail_notifications(mail)})"), 1)
        executor.submit(message_notifications.setText(f"StudIP ({simargl.new_messages_counter(client)})"), 2)

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
    exit_button = menu_window.findChild(QPushButton, "Exit_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(menu_window)
    )


    menu_window.show()
    main_window.close()

    main_window.menu_window = menu_window




def back_to_main(menu_window):
    main_window = load_ui("main.ui")

    # Theme combobox
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(QApplication.instance(), text)
    )

    # Theme init
    change_theme(QApplication.instance(), theme_box.currentText())

    # Press Enter to enter the menu
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )

    main_window.show()
    menu_window.close()


def error_login(menu_window):
    error_window = load_ui("error.ui")

    # button to exit back to the main
    exit_button = error_window.findChild(QPushButton, "Error_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(error_window)
    )

    error_window.show()
    menu_window.close()

    menu_window.courses_window = error_window


def login_from_enter(main_window):
    global client, mail, server, user_courses, current_login, schedule
    login_box = main_window.findChild(QLineEdit, "LoginLine")
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    login = login_box.text()
    current_login = login
    password = password_box.text()

    try:
        client = simargl.create_client(login,password,simargl.BASE_URL)
        mail = simargl.read_email_init(simargl.SERVER,str("ug-student\\"+login),password)
        server = simargl.write_email_init(simargl.SERVER,str("ug-student\\"+login),password)
    except:
        error_login(main_window)
    else:
        global notes_storage
        notes_storage = NotesStorage(login)
        open_menu(main_window)
        user_courses = simargl.get_courses(client)

# =========================
# MAIN
# =========================

def main():

    app = QApplication(sys.argv)

    # --- load main window ---
    main_window = load_ui("main.ui")

    # --- theme combobox ---
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(app, text)
    )

    # --- setting theme on the start ---
    change_theme(app, theme_box.currentText())

    # --- enter button ---
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )



    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()